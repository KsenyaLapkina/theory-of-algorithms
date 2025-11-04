import sqlite3
from datetime import datetime

class ClothingDatabase:
    def __init__(self, db_name='clothing_calculator.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица для расчетов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                jacket_size REAL NOT NULL,
                pants_size REAL NOT NULL,
                total_cost REAL NOT NULL,
                export_format TEXT NOT NULL
            )
        ''')
        
        # Таблица для изделий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS garments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                calculation_id INTEGER,
                garment_type TEXT NOT NULL,
                size REAL NOT NULL,
                fabric_consumption REAL NOT NULL,
                cost REAL NOT NULL,
                parameters TEXT NOT NULL,
                FOREIGN KEY (calculation_id) REFERENCES calculations (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Получение соединения с базой данных"""
        return sqlite3.connect(self.db_name)
    
    def save_calculation(self, jacket, pants, suit, export_format):
        """Сохранение расчета в базу данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Сохраняем основной расчет
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO calculations (timestamp, jacket_size, pants_size, total_cost, export_format)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, jacket.size, pants.size, suit.calculate_total_cost(), export_format))
        
        calculation_id = cursor.lastrowid
        
        # Сохраняем информацию о пиджаке
        jacket_params = f"Пуговицы: {jacket.buttons_count}, Подклад: {'да' if jacket.has_liner else 'нет'}"
        cursor.execute('''
            INSERT INTO garments (calculation_id, garment_type, size, fabric_consumption, cost, parameters)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (calculation_id, 'Пиджак', jacket.size, jacket.calculate_fabric_consumption(), 
              jacket.calculate_sewing_cost(), jacket_params))
        
        # Сохраняем информацию о брюках
        pants_params = f"Тип: {pants.pants_type}, Шлёвки: {'да' if pants.has_belt_loops else 'нет'}"
        cursor.execute('''
            INSERT INTO garments (calculation_id, garment_type, size, fabric_consumption, cost, parameters)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (calculation_id, 'Брюки', pants.size, pants.calculate_fabric_consumption(), 
              pants.calculate_sewing_cost(), pants_params))
        
        # Сохраняем информацию о костюме
        cursor.execute('''
            INSERT INTO garments (calculation_id, garment_type, size, fabric_consumption, cost, parameters)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (calculation_id, 'Костюм-тройка', 0, 0, suit.calculate_total_cost(), 'Полный комплект'))
        
        conn.commit()
        conn.close()
        
        return calculation_id
    
    def get_calculation_history(self):
        """Получение истории расчетов"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.id, c.timestamp, c.jacket_size, c.pants_size, c.total_cost, c.export_format
            FROM calculations c
            ORDER BY c.timestamp DESC
        ''')
        
        history = cursor.fetchall()
        conn.close()
        return history
    
    def get_calculation_details(self, calculation_id):
        """Получение деталей конкретного расчета"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT garment_type, size, fabric_consumption, cost, parameters
            FROM garments
            WHERE calculation_id = ?
            ORDER BY id
        ''', (calculation_id,))
        
        details = cursor.fetchall()
        conn.close()
        return details