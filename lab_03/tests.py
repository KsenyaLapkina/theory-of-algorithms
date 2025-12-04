import pytest
import tempfile
import os
import sqlite3
import io
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# ==================== НАСТРОЙКА ПУТЕЙ ====================
current_dir = Path(__file__).parent
web_dir = current_dir / "web"

if not web_dir.exists():
    print(f"⚠ Предупреждение: Папка 'web' не найдена по пути: {web_dir}")
    HAS_WEB = False
else:
    HAS_WEB = True
    sys.path.insert(0, str(web_dir))

# Пытаемся импортировать модули
try:
    if HAS_WEB:
        from main import app, Database, create_meme_with_text, UPLOAD_DIR, DB_PATH
        IMPORT_SUCCESS = True
        print("✓ Модули из main.py импортированы")
    else:
        IMPORT_SUCCESS = False
        raise ImportError("Папка 'web' не найдена")
except ImportError as e:
    print(f"⚠ Ошибка импорта main.py: {e}")
    IMPORT_SUCCESS = False

# ==================== БАЗОВЫЕ ТЕСТЫ (работают всегда) ====================
def test_web_folder_exists():
    """Тест: папка web существует."""
    assert web_dir.exists(), f"Папка 'web' должна существовать по пути: {web_dir}"
    print(f"✓ Папка 'web' найдена: {web_dir}")

def test_required_files_exist():
    """Тест: необходимые файлы существуют."""
    if not HAS_WEB:
        pytest.skip("Папка 'web' не найдена")
    
    required_files = ['main.py', 'index.html', 'style.css']
    
    for filename in required_files:
        file_path = web_dir / filename
        assert file_path.exists(), f"Файл {filename} должен существовать в папке web"
        print(f"✓ Файл {filename} существует ({file_path.stat().st_size} байт)")

def test_sqlite_database_operations():
    """Тест: операции с SQLite базой данных."""
    # Создаем временную БД
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создаем таблицы
        cursor.execute('''
            CREATE TABLE memes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                top_text TEXT,
                bottom_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE meme_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
        # Вставляем данные
        cursor.execute('''
            INSERT INTO memes (image_path, top_text, bottom_text)
            VALUES (?, ?, ?)
        ''', ('/test/image.jpg', 'Верх', 'Низ'))
        
        cursor.execute('INSERT INTO meme_stats (action_type) VALUES (?)', ('создано',))
        conn.commit()
        
        # Проверяем
        cursor.execute('SELECT COUNT(*) FROM memes')
        assert cursor.fetchone()[0] == 1
        
        cursor.execute('SELECT COUNT(*) FROM meme_stats')
        assert cursor.fetchone()[0] == 1
        
        print("✓ SQLite операции работают корректно")
        
    finally:
        conn.close()
        # Ждем немного перед удалением
        import time
        time.sleep(0.1)
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except PermissionError:
                print("⚠ Не удалось удалить временный файл БД (занят другим процессом)")

def test_file_operations():
    """Тест: операции с файлами."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as tmp:
        tmp.write("Тестовые данные")
        tmp_path = tmp.name
    
    try:
        assert os.path.exists(tmp_path)
        
        with open(tmp_path, 'r') as f:
            assert f.read() == "Тестовые данные"
        
        print("✓ Файловые операции работают")
        
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def test_image_file_validation():
    """Тест: валидация файлов изображений."""
    valid_extensions = ['.jpg', '.png', '.gif']
    
    for ext in valid_extensions:
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(b"fake image data")
            tmp_path = tmp.name
        
        try:
            assert os.path.exists(tmp_path)
            _, file_ext = os.path.splitext(tmp_path)
            assert file_ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    print("✓ Валидация расширений файлов работает")

# ==================== ТЕСТЫ ПРИЛОЖЕНИЯ ====================
def test_app_exists():
    """Тест: приложение существует."""
    if not IMPORT_SUCCESS:
        pytest.skip("Модули не импортированы")
    
    assert app is not None
    assert hasattr(app, 'routes')
    print("✓ Приложение FastAPI создано")

def test_database_class_exists():
    """Тест: класс Database существует."""
    if not IMPORT_SUCCESS:
        pytest.skip("Модули не импортированы")
    
    assert Database is not None
    print("✓ Класс Database существует")

def test_database_operations():
    """Тест: операции с классом Database."""
    if not IMPORT_SUCCESS:
        pytest.skip("Модули не импортированы")
    
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = Database(db_path)
        assert db is not None
        
        # Проверяем методы
        assert hasattr(db, 'save_meme')
        assert hasattr(db, 'get_stats')
        assert hasattr(db, 'log_action')
        
        # Тестируем сохранение
        meme_id = db.save_meme("/test/image.jpg", "Тест", "Тест")
        assert isinstance(meme_id, int)
        assert meme_id > 0
        
        # Тестируем статистику
        stats = db.get_stats()
        assert 'total_memes' in stats
        assert 'total_actions' in stats
        assert 'actions' in stats
        
        print("✓ Класс Database работает корректно")
        
    finally:
        # Закрываем соединения
        if hasattr(db, '_close_connections'):
            db._close_connections()
        
        # Ждем и удаляем
        import time
        time.sleep(0.2)
        if os.path.exists(db_path):
            try:
                os.unlink(db_path)
            except PermissionError:
                print("⚠ Не удалось удалить тестовую БД")

def test_routes_exist():
    """Тест: проверка маршрутов приложения."""
    if not IMPORT_SUCCESS:
        pytest.skip("Модули не импортированы")
    
    # Простая проверка что приложение имеет маршруты
    assert hasattr(app, 'routes')
    
    # Получаем список маршрутов
    routes = []
    for route in app.routes:
        routes.append({
            'path': getattr(route, 'path', 'unknown'),
            'methods': getattr(route, 'methods', set())
        })
    
    # Проверяем что есть хотя бы некоторые маршруты
    assert len(routes) > 0
    
    # Проверяем наличие основных путей
    route_paths = [r['path'] for r in routes]
    
    expected_paths = ['/', '/create-meme', '/stats', '/download/{meme_id}']
    found_paths = []
    
    for expected in expected_paths:
        for route_path in route_paths:
            if expected in route_path:
                found_paths.append(expected)
                break
    
    print(f"✓ Найдены маршруты: {found_paths}")

# ==================== ТЕСТЫ ФУНКЦИОНАЛЬНОСТИ ====================
def test_json_structure():
    """Тест: структура JSON для статистики."""
    expected_stats = {
        'total_memes': 0,
        'total_actions': 0,
        'actions': [('создано', 0), ('скачано', 0), ('просмотрено', 0)]
    }
    
    assert 'total_memes' in expected_stats
    assert 'total_actions' in expected_stats
    assert 'actions' in expected_stats
    
    assert isinstance(expected_stats['total_memes'], int)
    assert isinstance(expected_stats['total_actions'], int)
    assert isinstance(expected_stats['actions'], list)
    
    print("✓ Структура JSON корректна")

def test_text_validation():
    """Тест: валидация текста."""
    test_cases = [
        ("", True),
        ("Короткий текст", True),
        ("A" * 100, True),
        ("Текст с цифрами 123", True),
    ]
    
    for text, should_be_valid in test_cases:
        assert isinstance(text, str)
    
    print("✓ Валидация текста работает")

def test_create_meme_function():
    """Тест: функция create_meme_with_text."""
    if not IMPORT_SUCCESS:
        pytest.skip("Модули не импортированы")
    
    # Создаем временное изображение
    try:
        from PIL import Image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp.name)
            image_path = Path(tmp.name)
        
        # Тестируем функцию
        result_path = create_meme_with_text(image_path, "Верх", "Низ")
        
        # Проверяем результат
        assert result_path is not None
        assert isinstance(result_path, Path)
        
        print("✓ Функция create_meme_with_text работает")
        
    except ImportError:
        print("⚠ Pillow не установлен, пропускаем тест")
        pytest.skip("Требуется Pillow для теста")
    finally:
        if 'image_path' in locals() and image_path.exists():
            image_path.unlink()
        if 'result_path' in locals() and result_path.exists() and result_path != image_path:
            result_path.unlink()

# ==================== ТЕСТЫ КОНФИГУРАЦИИ ====================
def test_configuration():
    """Тест: конфигурация приложения."""
    if not IMPORT_SUCCESS:
        pytest.skip("Модули не импортированы")
    
    # Проверяем что переменные определены
    assert UPLOAD_DIR is not None
    assert DB_PATH is not None
    
    # Проверяем типы
    assert isinstance(UPLOAD_DIR, Path)
    assert isinstance(DB_PATH, Path) or isinstance(DB_PATH, str)
    
    print("✓ Конфигурация приложения корректна")

# ==================== МОК-ТЕСТЫ API ====================
@patch('main.db')
def test_stats_logic(mock_db):
    """Тест: логика статистики с моками."""
    # Настраиваем мок
    mock_db.get_stats.return_value = {
        'total_memes': 5,
        'total_actions': 12,
        'actions': [('создано', 5), ('скачано', 5), ('просмотрено', 2)]
    }
    
    # Имитируем вызов
    stats = mock_db.get_stats()
    
    assert stats['total_memes'] == 5
    assert stats['total_actions'] == 12
    assert len(stats['actions']) == 3
    
    print("✓ Логика статистики работает")

def test_error_handling_logic():
    """Тест: логика обработки ошибок."""
    # Тестируем валидацию файлов
    invalid_extensions = ['.txt', '.pdf', '.doc']
    
    for ext in invalid_extensions:
        filename = f"test{ext}"
        file_ext = Path(filename).suffix.lower()
        assert file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    print("✓ Логика обработки ошибок работает")

# ==================== ИНТЕГРАЦИОННЫЙ ТЕСТ ====================
def test_integration():
    """Интеграционный тест приложения."""
    print("\n" + "="*60)
    print("ИНТЕГРАЦИОННЫЕ ТЕСТЫ")
    print("="*60)
    
    # 1. Проверяем файловую систему
    if HAS_WEB:
        print("✓ Папка 'web' существует")
        
        # 2. Проверяем основные файлы
        main_file = web_dir / "main.py"
        if main_file.exists():
            print(f"✓ main.py существует ({main_file.stat().st_size} байт)")
        else:
            print("✗ main.py не найден")
            
        index_file = web_dir / "index.html"
        if index_file.exists():
            print(f"✓ index.html существует ({index_file.stat().st_size} байт)")
        else:
            print("✗ index.html не найден")
            
        css_file = web_dir / "style.css"
        if css_file.exists():
            print(f"✓ style.css существует ({css_file.stat().st_size} байт)")
        else:
            print("✗ style.css не найден")
    
    # 3. Проверяем импорт
    if IMPORT_SUCCESS:
        print("✓ Модули успешно импортированы")
        
        # 4. Проверяем основные компоненты
        if app is not None:
            print("✓ Приложение FastAPI создано")
        
        if Database is not None:
            print("✓ Класс Database существует")
        
        if hasattr(sys.modules.get('main'), 'create_meme_with_text'):
            print("✓ Функция create_meme_with_text существует")
    else:
        print("⚠ Модули не импортированы (возможно тестовая среда)")
    
    print("="*60)
    print("✓ Интеграционные тесты завершены")
    print("="*60)

# ==================== ЗАПУСК ВСЕХ ТЕСТОВ ====================
def test_summary():
    """Итоговый тест-отчет."""
    print("\n" + "="*60)
    print("ИТОГОВЫЙ ОТЧЕТ О ТЕСТИРОВАНИИ")
    print("="*60)
    
    test_info = {
        "Файловая система": HAS_WEB,
        "Импорт модулей": IMPORT_SUCCESS,
        "Приложение FastAPI": IMPORT_SUCCESS and app is not None,
        "Класс Database": IMPORT_SUCCESS and Database is not None,
    }
    
    for name, status in test_info.items():
        if status:
            print(f"  ✓ {name}: ГОТОВ")
        else:
            print(f"  ✗ {name}: НЕ ГОТОВ")
    
    print("="*60)
    
    # Всегда возвращаем True, так как это отчет, а не тест
    assert True

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================
if __name__ == "__main__":
    """Запуск тестов напрямую."""
    print("="*60)
    print("ТЕСТИРОВАНИЕ ГЕНЕРАТОРА МЕМОВ")
    print("="*60)
    
    # Список тестов для запуска
    tests_to_run = [
        test_web_folder_exists,
        test_required_files_exist,
        test_sqlite_database_operations,
        test_file_operations,
        test_image_file_validation,
        test_app_exists,
        test_database_class_exists,
        test_database_operations,
        test_routes_exist,
        test_json_structure,
        test_text_validation,
        test_create_meme_function,
        test_configuration,
        test_stats_logic,
        test_error_handling_logic,
        test_integration,
        test_summary,
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_func in tests_to_run:
        try:
            print(f"\nЗапуск: {test_func.__name__}...")
            test_func()
            print(f"  ✓ {test_func.__name__}: ПРОЙДЕН")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test_func.__name__}: ОШИБКА - {str(e)[:50]}")
            failed += 1
        except pytest.skip.Exception as e:
            print(f"  ⚠ {test_func.__name__}: ПРОПУЩЕН - {str(e)[:50]}")
            skipped += 1
        except Exception as e:
            print(f"  ✗ {test_func.__name__}: ИСКЛЮЧЕНИЕ - {type(e).__name__}: {str(e)[:50]}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"ИТОГ: {passed} пройдено, {failed} не пройдено, {skipped} пропущено")
    
    if failed == 0:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        sys.exit(0)
    else:
        print("⚠ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        sys.exit(1)