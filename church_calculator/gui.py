import sys
import re
import os
import sqlite3
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLineEdit, QPushButton, QComboBox, 
                               QLabel, QMessageBox, QGroupBox, QTextEdit, QGridLayout,
                               QTableWidget, QTableWidgetItem, QTabWidget, QDialog,
                               QHeaderView, QSplitter, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QTextCursor, QColor, QBrush

from church import ChurchCalculator, church_to_int, int_to_church


class ExpressionParser:
    @staticmethod
    def parse_expression(expression: str) -> tuple:
        expression = expression.strip().replace(' ', '').replace(',', '.')
        
        patterns = {
            'factorial': r'^([0-9]+\.?[0-9]*)!$',
            'power': r'^([0-9]+\.?[0-9]*)\^([0-9]+\.?[0-9]*)$',
            'multiply': r'^([0-9]+\.?[0-9]*)\*([0-9]+\.?[0-9]*)$',
            'divide': r'^([0-9]+\.?[0-9]*)/([0-9]+\.?[0-9]*)$',
            'add': r'^([0-9]+\.?[0-9]*)\+([0-9]+\.?[0-9]*)$',
            'subtract': r'^([0-9]+\.?[0-9]*)-([0-9]+\.?[0-9]*)$'
        }
        
        for operation, pattern in patterns.items():
            match = re.match(pattern, expression)
            if match:
                if operation == 'factorial':
                    return operation, float(match.group(1)), None
                else:
                    return operation, float(match.group(1)), float(match.group(2))
        
        raise ValueError("Неподдерживаемое выражение или некорректный формат")


class DatabaseManager:
    """Менеджер базы данных для истории вычислений."""
    
    def __init__(self, db_path="calculator.db"):
        self.db_path = db_path
        self._ensure_database()
    
    def _ensure_database(self):
        """Создает базу данных и таблицы при необходимости."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS calculations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expression TEXT NOT NULL,
                    result TEXT NOT NULL,
                    operation_type TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица статистики
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    count INTEGER DEFAULT 0,
                    last_used DATETIME
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
    
    def save_calculation(self, expression: str, result: str, operation_type: str):
        """Сохраняет вычисление в базу данных."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Сохраняем вычисление
            cursor.execute('''
                INSERT INTO calculations (expression, result, operation_type)
                VALUES (?, ?, ?)
            ''', (expression, str(result), operation_type))
            
            # Обновляем статистику
            cursor.execute('''
                INSERT OR REPLACE INTO statistics (operation_type, count, last_used)
                VALUES (?, 
                    COALESCE((SELECT count + 1 FROM statistics WHERE operation_type = ?), 1),
                    CURRENT_TIMESTAMP)
            ''', (operation_type, operation_type))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.Error as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def get_calculation_history(self, limit: int = 50):
        """Получает историю вычислений."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM calculations 
                ORDER BY id DESC 
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error:
            return []
    
    def get_statistics(self):
        """Получает статистику операций."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT operation_type, COUNT(*) as count 
                FROM calculations 
                GROUP BY operation_type 
                ORDER BY count DESC
            ''')
            stats = cursor.fetchall()
            
            cursor.execute('SELECT COUNT(*) as total FROM calculations')
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT operation_type) as types FROM calculations')
            types = cursor.fetchone()[0]
            
            conn.close()
            return {
                'stats': stats,
                'total_calculations': total,
                'operation_types': types
            }
        except sqlite3.Error:
            return {'stats': [], 'total_calculations': 0, 'operation_types': 0}
    
    def clear_history(self):
        """Очищает историю вычислений."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM calculations')
            cursor.execute('DELETE FROM statistics')
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error:
            return False


class DatabaseViewerDialog(QDialog):
    """Диалоговое окно для просмотра базы данных."""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("База данных калькулятора")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background: #f8f9fa;
            }
            QTableWidget {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                gridline-color: #e9ecef;
            }
            QHeaderView::section {
                background: #ff69b4;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Верхняя панель с информацией
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #ffb6c1;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        info_layout = QHBoxLayout(info_frame)
        
        self.db_info_label = QLabel("Загрузка информации...")
        self.db_info_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        info_layout.addWidget(self.db_info_label)
        
        clear_btn = QPushButton("Очистить историю")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff69b4, stop: 1 #ff1493);
                border: 2px solid #c71585;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff1493, stop: 1 #dc143c);
            }
            QPushButton:pressed {
                background: #c71585;
            }
        """)
        clear_btn.clicked.connect(self.clear_history)
        info_layout.addWidget(clear_btn)
        
        refresh_btn = QPushButton("Обновить")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff85a2, stop: 1 #ff6b95);
                border: 2px solid #ff1493;
                border-radius: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff6b95, stop: 1 #ff1493);
            }
            QPushButton:pressed {
                background: #c71585;
            }
        """)
        refresh_btn.clicked.connect(self.load_data)
        info_layout.addWidget(refresh_btn)
        
        layout.addWidget(info_frame)
        
        # Таблица с историей вычислений
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "Выражение", "Результат", "Операция", "Время"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.history_table)
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff69b4, stop: 1 #ff1493);
                border: 2px solid #c71585;
                border-radius: 6px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff1493, stop: 1 #dc143c);
            }
            QPushButton:pressed {
                background: #c71585;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)
    
    def load_data(self):
        """Загружает данные из базы."""
        # Загрузка истории
        history = self.db_manager.get_calculation_history()
        self.history_table.setRowCount(len(history))
        
        for row_idx, record in enumerate(history):
            self.history_table.setItem(row_idx, 0, QTableWidgetItem(str(record['id'])))
            self.history_table.setItem(row_idx, 1, QTableWidgetItem(record['expression']))
            self.history_table.setItem(row_idx, 2, QTableWidgetItem(record['result']))
            self.history_table.setItem(row_idx, 3, QTableWidgetItem(record['operation_type']))
            self.history_table.setItem(row_idx, 4, QTableWidgetItem(record['timestamp']))
        
        # Загрузка статистики для информации
        stats_data = self.db_manager.get_statistics()
        
        # Обновляем информацию
        file_size = os.path.getsize("calculator.db") if os.path.exists("calculator.db") else 0
        self.db_info_label.setText(
            f"База данных: {len(history)} записей | "
            f"{stats_data['total_calculations']} всего вычислений | "
            f"{stats_data['operation_types']} типов операций | "
            f"{file_size} байт"
        )
    
    def clear_history(self):
        """Очищает историю вычислений."""
        reply = QMessageBox.question(
            self, 'Очистка истории',
            'Вы уверены, что хотите очистить всю историю вычислений?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db_manager.clear_history():
                QMessageBox.information(self, 'Успех', 'История вычислений очищена.')
                self.load_data()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось очистить историю.')


class CalculatorWindow(QMainWindow):
    """Главное окно калькулятора с графическим интерфейсом."""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()  # Создаем менеджер БД
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowTitle("Калькулятор Чёрча")
        self.setFixedSize(550, 700)
        
        # Установка фона
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #fff0f5, stop: 1 #ffe4ec);
            }
        """)
        
        # Центральный виджет
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)  # Уменьшили отступы между элементами
        layout.setContentsMargins(15, 15, 15, 15)  # Уменьшили внешние отступы
        
        # Заголовок с кнопкой базы данных
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5)
        
        title_label = QLabel("Калькулятор Чёрча")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: bold;
                color: #ff1493;
                background: linear-gradient(135deg, #ff69b4, #ff1493);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
        """)
        header_layout.addWidget(title_label)
        
        # Кнопка просмотра базы данных
        self.db_button = QPushButton("База данных")
        self.db_button.setFixedSize(100, 35)  # Уменьшили размер
        self.db_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff69b4, stop: 1 #ff1493);
                border: 2px solid #c71585;
                border-radius: 6px;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 3px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff1493, stop: 1 #dc143c);
            }
            QPushButton:pressed {
                background: #c71585;
            }
        """)
        self.db_button.clicked.connect(self.show_database)
        header_layout.addWidget(self.db_button, alignment=Qt.AlignRight)
        
        layout.addWidget(header_widget)
        
        # Поле ввода выражения
        self.expression_input = QLineEdit()
        self.expression_input.setPlaceholderText("Введите выражение")
        self.expression_input.setStyleSheet("""
            QLineEdit {
                background: white;
                border: 2px solid #ff69b4;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                color: #c71585;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 2px solid #ff1493;
                background: #fffafa;
                box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.1);
            }
        """)
        self.expression_input.setFixedHeight(45)
        layout.addWidget(self.expression_input)
        
        # Панель кнопок операций
        operations_widget = QWidget()
        operations_layout = QGridLayout(operations_widget)
        operations_layout.setSpacing(6)  # Уменьшили отступы между кнопками
        operations_layout.setContentsMargins(0, 0, 0, 0)
        
        # Кнопки цифр и операций - уменьшили размер
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('!', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('←', 4, 1), ('=', 4, 2, 2)
        ]
        
        for button_info in buttons:
            if len(button_info) == 4:
                text, row, col, colspan = button_info
            else:
                text, row, col = button_info
                colspan = 1
                
            btn = QPushButton(text)
            btn.setFixedSize(65, 55)  # Уменьшили размер кнопок
            if text == '=':
                # Кнопка вычисления
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #ff69b4, stop: 1 #ff1493);
                        border: 2px solid #c71585;
                        border-radius: 8px;
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #ff1493, stop: 1 #dc143c);
                    }
                    QPushButton:pressed {
                        background: #c71585;
                    }
                """)
                btn.clicked.connect(self.calculate)
            elif text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:           
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #ffb6c1, stop: 1 #ff91a4);
                        border: 2px solid #ff69b4;
                        border-radius: 8px;
                        color: #8b008b;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #ff91a4, stop: 1 #ff69b4);
                    }
                    QPushButton:pressed {
                        background: #ff1493;
                        color: white;
                    }
                """)
                btn.clicked.connect(lambda checked, t=text: self.insert_text(t))
            elif text in ['+', '-', '*', '/', '^', '!']:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #ff85a2, stop: 1 #ff6b95);
                        border: 2px solid #ff1493;
                        border-radius: 8px;
                        color: white;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #ff6b95, stop: 1 #ff1493);
                    }
                    QPushButton:pressed {
                        background: #c71585;
                    }
                """)
                btn.clicked.connect(lambda checked, t=text: self.insert_text(t))
            else:
                # Управляющие кнопки
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #db7093, stop: 1 #c71585);
                        border: 2px solid #8b008b;
                        border-radius: 8px;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #c71585, stop: 1 #8b008b);
                    }
                    QPushButton:pressed {
                        background: #800080;
                    }
                """)
                if text == 'C':
                    btn.clicked.connect(self.clear_inputs)
                elif text == '←':
                    btn.clicked.connect(self.backspace)
            
            operations_layout.addWidget(btn, row, col, 1, colspan)
        
        # Кнопка степени
        power_btn = QPushButton('^')
        power_btn.setFixedSize(65, 55)
        power_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff85a2, stop: 1 #ff6b95);
                border: 2px solid #ff1493;
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ff6b95, stop: 1 #ff1493);
            }
            QPushButton:pressed {
                background: #c71585;
            }
        """)
        power_btn.clicked.connect(lambda: self.insert_text('^'))
        operations_layout.addWidget(power_btn, 3, 1)
        
        layout.addWidget(operations_widget)
        
        # Поле результата
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setPlaceholderText("Результат появится здесь...")
        self.result_display.setStyleSheet("""
            QLineEdit {
                background: #fffafa;
                border: 3px solid #ff69b4;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                color: #ff1493;
                font-weight: bold;
                text-align: center;
            }
        """)
        self.result_display.setFixedHeight(60)
        layout.addWidget(self.result_display)
        
        # Поле для отображения ошибок
        self.error_display = QTextEdit()
        self.error_display.setReadOnly(True)
        self.error_display.setMaximumHeight(80)
        self.error_display.setPlaceholderText("Здесь будут отображаться ошибки и информация...")
        self.error_display.setStyleSheet("""
            QTextEdit {
                background: #fffafa;
                border: 2px solid #ffb6c1;
                border-radius: 8px;
                padding: 8px;
                font-size: 11px;
                color: #6c757d;
                font-family: Arial;
            }
        """)
        layout.addWidget(self.error_display)
        
        # Таймер для обновления (оставил для совместимости)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_db_counter)
        self.timer.start(5000)
        
    def insert_text(self, text: str):
        current_text = self.expression_input.text()
        cursor_position = self.expression_input.cursorPosition()
        
        new_text = current_text[:cursor_position] + text + current_text[cursor_position:]
        self.expression_input.setText(new_text)
        
        # Устанавливаем курсор после вставленного текста
        self.expression_input.setCursorPosition(cursor_position + len(text))
        
    def backspace(self):
        """Удаляет последний символ в поле ввода."""
        current_text = self.expression_input.text()
        cursor_position = self.expression_input.cursorPosition()
        
        if current_text and cursor_position > 0:
            new_text = current_text[:cursor_position-1] + current_text[cursor_position:]
            self.expression_input.setText(new_text)
            self.expression_input.setCursorPosition(cursor_position - 1)
    
    def calculate(self):
        """Выполняет вычисление на основе введенного выражения."""
        try:
            expression = self.expression_input.text().strip()
            if not expression:
                self.show_error("Введите математическое выражение")
                return
            
            # Очищаем предыдущие сообщения
            self.error_display.clear()
            
            # Парсинг выражения
            parsed = ExpressionParser.parse_expression(expression)
            operation = parsed[0]
            
            result = None
            
            if operation == 'factorial':
                n = parsed[1]
                
                # Для факториала - только целые числа
                if n != int(n):
                    raise ValueError("Факториал определен только для целых чисел")
                
                # Преобразование в церковное число
                church_n = int_to_church(int(n))
                
                # Вычисление факториала
                result_church = ChurchCalculator.factorial(church_n)
                result = church_to_int(result_church)
                
            else:
                a, b = parsed[1], parsed[2]
                
                # Для церковных чисел - только целые части
                int_a, int_b = int(a), int(b)
                
                # Проверка для вычитания
                if operation == 'subtract' and int_a < int_b:
                    self.show_info(f"Внимание: уменьшаемое меньше вычитаемого. Результат будет 0.")
                    result = 0
                else:
                    # Преобразование в церковные числа
                    church_a = int_to_church(int_a)
                    church_b = int_to_church(int_b)
                    
                    # Выполнение операции
                    if operation == 'add':
                        result_church = ChurchCalculator.add(church_a, church_b)
                        result = church_to_int(result_church)
                        
                    elif operation == 'subtract':
                        result_church = ChurchCalculator.subtract(church_a, church_b)
                        result = church_to_int(result_church)
                        
                    elif operation == 'multiply':
                        result_church = ChurchCalculator.multiply(church_a, church_b)
                        result = church_to_int(result_church)
                        
                    elif operation == 'divide':
                        # Целочисленное деление
                        if int_b == 0:
                            raise ValueError("Деление на ноль")
                        result = int_a // int_b
                        
                    elif operation == 'power':
                        result_church = ChurchCalculator.power(church_a, church_b)
                        result = church_to_int(result_church)
            
            # Отображение финального результата
            self.result_display.setText(str(result))
            
            # Сохраняем в базу данных
            if result is not None:
                success = self.db_manager.save_calculation(expression, str(result), operation)
                if success:
                    self.show_info(f"Вычисление сохранено в базу данных")
                else:
                    self.show_info(f"Не удалось сохранить в базу данных")
            
        except ValueError as e:
            error_msg = str(e)
            self.show_error(f"Некорректное выражение: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            self.show_error(f"Ошибка вычисления: {error_msg}")
    
    def show_error(self, message: str):
        """Показывает сообщение об ошибке."""
        self.result_display.setText("Ошибка")
        self.error_display.setText(f" {message}")
        self.error_display.setStyleSheet("""
            QTextEdit {
                background: #fff5f5;
                border: 2px solid #dc143c;
                border-radius: 8px;
                padding: 8px;
                font-size: 11px;
                color: #dc143c;
                font-weight: bold;
            }
        """)
    
    def show_info(self, message: str):
        """Показывает информационное сообщение."""
        self.error_display.setText(message)
        self.error_display.setStyleSheet("""
            QTextEdit {
                background: #f0fff4;
                border: 2px solid #28a745;
                border-radius: 8px;
                padding: 8px;
                font-size: 11px;
                color: #155724;
            }
        """)
    
    def clear_inputs(self):
        """Очищает поле ввода выражения."""
        self.expression_input.clear()
        self.result_display.clear()
        self.error_display.clear()
    
    def show_database(self):
        """Показывает окно базы данных."""
        dialog = DatabaseViewerDialog(self.db_manager, self)
        dialog.exec()
    
    def update_db_counter(self):
        """Оставлен для совместимости, но не используется."""
        pass


def main():
    """Функция запуска приложения."""
    app = QApplication(sys.argv)
    
    # Установка стиля приложения
    app.setStyle('Fusion')
    
    window = CalculatorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()