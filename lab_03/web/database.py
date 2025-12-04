import sqlite3
from pathlib import Path
from datetime import datetime

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица для мемов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_image TEXT NOT NULL,
                    final_image TEXT NOT NULL,
                    top_text TEXT,
                    bottom_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица для статистики
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meme_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meme_id INTEGER,
                    action_type TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (meme_id) REFERENCES memes (id)
                )
            ''')
            
            conn.commit()
    
    def save_meme(self, original_image: str, final_image: str, top_text: str = "", bottom_text: str = "") -> int:
        """Сохраняет мем в базу данных."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO memes (original_image, final_image, top_text, bottom_text)
                VALUES (?, ?, ?, ?)
            ''', (original_image, final_image, top_text, bottom_text))
            meme_id = cursor.lastrowid
            
            # Логируем создание
            cursor.execute('''
                INSERT INTO meme_stats (meme_id, action_type)
                VALUES (?, ?)
            ''', (meme_id, 'создано'))
            
            conn.commit()
            return meme_id
    
    def log_action(self, meme_id: int, action_type: str):
        """Логирует действие с мемом."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO meme_stats (meme_id, action_type)
                VALUES (?, ?)
            ''', (meme_id, action_type))
            conn.commit()
    
    def get_meme_by_id(self, meme_id: int):
        """Возвращает мем по ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM memes WHERE id = ?
            ''', (meme_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def get_stats(self):
        """Возвращает статистику."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Общее количество мемов
            cursor.execute('SELECT COUNT(*) FROM memes')
            total_memes = cursor.fetchone()[0]
            
            # Общее количество действий
            cursor.execute('SELECT COUNT(*) FROM meme_stats')
            total_actions = cursor.fetchone()[0]
            
            # Статистика по типам действий
            cursor.execute('''
                SELECT action_type, COUNT(*) as count
                FROM meme_stats
                GROUP BY action_type
                ORDER BY count DESC
            ''')
            actions = cursor.fetchall()
            
            return {
                'total_memes': total_memes,
                'total_actions': total_actions,
                'actions': actions
            }