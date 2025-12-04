from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import sqlite3
from pathlib import Path
import uuid
import re
from datetime import datetime

app = FastAPI(title="Генератор мемов")

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = BASE_DIR / "memes.db"

UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT NOT NULL,
                    top_text TEXT,
                    bottom_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meme_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def save_meme(self, image_path: str, top_text: str = "", bottom_text: str = "") -> int:
        """Сохраняет мем в базу данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO memes (image_path, top_text, bottom_text)
                VALUES (?, ?, ?)
            ''', (image_path, top_text, bottom_text))
            meme_id = cursor.lastrowid
            
            # Логируем создание на русском
            cursor.execute('INSERT INTO meme_stats (action_type) VALUES (?)', ('создано',))
            
            conn.commit()
            return meme_id
    
    def log_action(self, action_type: str):
        """Логирует действие с мемом на русском."""
        # Только русские действия
        russian_actions = ['создано', 'скачано', 'просмотрено']
        if action_type in russian_actions:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO meme_stats (action_type) VALUES (?)', (action_type,))
                conn.commit()
    
    def get_stats(self):
        """Возвращает статистику только с русскими действиями."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Общее количество мемов
            cursor.execute('SELECT COUNT(*) FROM memes')
            total_memes = cursor.fetchone()[0] or 0
            
            # Общее количество действий (только русских)
            cursor.execute('''
                SELECT COUNT(*) FROM meme_stats 
                WHERE action_type IN ('создано', 'скачано', 'просмотрено')
            ''')
            total_actions = cursor.fetchone()[0] or 0
            
            # Статистика по типам действий (только русские)
            cursor.execute('''
                SELECT action_type, COUNT(*) as count
                FROM meme_stats
                WHERE action_type IN ('создано', 'скачано', 'просмотрено')
                GROUP BY action_type
                ORDER BY count DESC
            ''')
            actions = cursor.fetchall()
            
            # Если нет действий, показываем пустой список
            if not actions:
                actions = [('создано', 0), ('скачано', 0), ('просмотрено', 0)]
            
            return {
                'total_memes': total_memes,
                'total_actions': total_actions,
                'actions': actions
            }
    
    def reset_stats(self):
        """Очищает статистику (только для отладки)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM meme_stats')
            conn.commit()

db = Database(DB_PATH)

# ========== СОЗДАНИЕ МЕМОВ ==========
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def create_meme_with_text(image_path: Path, top_text: str, bottom_text: str) -> Path:
    """Создает мем с текстом поверх изображения."""
    if not HAS_PIL:
        return image_path
    
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size
        font_size = max(30, min(img_height // 15, 60))
        
        # Пробуем найти шрифт
        try:
            font_paths = ["C:\\Windows\\Fonts\\arial.ttf"]
            font = None
            for path in font_paths:
                if os.path.exists(path):
                    font = ImageFont.truetype(path, font_size)
                    break
            if font is None:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Функция для добавления текста
        def add_text(text, y_position):
            if not text:
                return
            
            # Получаем размер текста
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
            except:
                text_width = draw.textsize(text, font=font)[0]
            
            # Центрируем текст
            x = (img_width - text_width) / 2
            
            # Добавляем черную обводку для читаемости
            stroke_width = 3
            for dx in [-stroke_width, 0, stroke_width]:
                for dy in [-stroke_width, 0, stroke_width]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y_position + dy), text, font=font, fill="black")
            
            # Белый текст поверх
            draw.text((x, y_position), text, font=font, fill="white")
        
        # Добавляем верхний текст
        if top_text:
            add_text(top_text, 20)
        
        # Добавляем нижний текст
        if bottom_text:
            try:
                bbox = draw.textbbox((0, 0), bottom_text, font=font)
                text_height = bbox[3] - bbox[1]
            except:
                text_height = font_size
            
            add_text(bottom_text, img_height - text_height - 20)
        
        # Сохраняем мем
        output_filename = f"meme_{uuid.uuid4().hex}{image_path.suffix}"
        output_path = UPLOAD_DIR / output_filename
        img.save(output_path, quality=95)
        
        return output_path
        
    except Exception as e:
        print(f"Ошибка при создании мема: {e}")
        return image_path

# ========== РОУТЫ ==========
@app.get("/")
async def home_page(request: Request):
    """Главная страница."""
    html_path = BASE_DIR / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    stats = db.get_stats()
    
    # Вставляем статистику в HTML
    html_content = re.sub(r'\{\{\s*total_memes\s*\}\}', str(stats['total_memes']), html_content)
    html_content = re.sub(r'\{\{\s*total_actions\s*\}\}', str(stats['total_actions']), html_content)
    
    # Вставляем список действий на русском
    actions_html = ""
    for action_type, count in stats['actions']:
        actions_html += f'''
        <div class="action-item">
            <span class="action-name">{action_type}</span>
            <span class="action-count">{count}</span>
        </div>
        '''
    
    html_content = html_content.replace('<!-- ACTIONS_PLACEHOLDER -->', actions_html)
    
    return HTMLResponse(html_content)

@app.post("/create-meme")
async def create_meme(
    image: UploadFile = File(...),
    top_text: str = Form(""),
    bottom_text: str = Form("")
):
    """Создает новый мем."""
    # Проверка типа файла
    if not image.content_type.startswith('image/'):
        raise HTTPException(400, "Разрешены только изображения")
    
    # Проверка размера
    content = await image.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, "Файл слишком большой (макс. 5MB)")
    
    # Определяем расширение файла
    file_ext = Path(image.filename).suffix.lower()
    if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        file_ext = '.jpg'
    
    # Сохраняем оригинальное изображение
    original_filename = f"original_{uuid.uuid4().hex}{file_ext}"
    original_path = UPLOAD_DIR / original_filename
    
    with open(original_path, "wb") as f:
        f.write(content)
    
    # Создаем мем с текстом
    meme_path = create_meme_with_text(original_path, top_text, bottom_text)
    
    # Сохраняем в базу данных
    meme_id = db.save_meme(str(meme_path), top_text, bottom_text)
    
    # Логируем загрузку на русском
    db.log_action("скачано")
    
    return JSONResponse({
        "success": True,
        "meme_id": meme_id,
        "image_url": f"/uploads/{meme_path.name}",
        "download_url": f"/download/{meme_id}"
    })

@app.get("/download/{meme_id}")
async def download_meme(meme_id: int):
    """Скачивает созданный мем."""
    # Находим мем в базе данных
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT image_path FROM memes WHERE id = ?', (meme_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        meme_path = Path(result[0])
        if meme_path.exists():
            # Логируем скачивание на русском
            db.log_action("скачано")
            
            # Имя файла для скачивания
            filename = f"мем_{meme_id}{meme_path.suffix}"
            
            return FileResponse(
                meme_path,
                filename=filename,
                media_type='image/*'
            )
    
    raise HTTPException(404, "Мем не найден")

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    """Отдает загруженные файлы."""
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "Файл не найден")
    
    # Логируем просмотр на русском
    db.log_action("просмотрено")
    
    return FileResponse(file_path)

@app.get("/stats")
async def get_stats_api():
    """API для получения статистики (только русские записи)."""
    stats = db.get_stats()
    return JSONResponse(stats)

# Разрешаем доступ к папке uploads
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("Генератор мемов")
    print(f"Директория: {BASE_DIR}")
    print(f"Адрес: http://127.0.0.1:3471")
    print("=" * 50)
    
    if not HAS_PIL:
        print("ВНИМАНИЕ: Библиотека Pillow не установлена!")
        print("Установите её командой: pip install pillow")
        print("Без неё текст не будет накладываться на изображения")
        print("=" * 50)
    
    # Запускаем сервер
    uvicorn.run(app, host="127.0.0.1", port=3471)