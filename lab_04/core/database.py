import sqlite3
import os
import json
from contextlib import contextmanager
from datetime import datetime
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class Database:
    """Менеджер базы данных SQLite3"""
    
    def __init__(self, db_path="generator_app.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        with self.get_connection() as conn:
            # Таблица статистики
            conn.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    count INTEGER NOT NULL,
                    parameters TEXT,
                    duration_ms INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица логов
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT NOT NULL,
                    details TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для соединения с БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def log_activity(self, activity: str, details: str = ""):
        """Логирование активности"""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO logs (activity, details) VALUES (?, ?)",
                    (activity, details)
                )
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
    
    def save_stats(self, operation: str, count: int, parameters: dict = None, duration_ms: int = 0):
        """Сохранение статистики"""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO stats (operation, count, parameters, duration_ms) VALUES (?, ?, ?, ?)",
                    (operation, count, json.dumps(parameters) if parameters else None, duration_ms)
                )
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")