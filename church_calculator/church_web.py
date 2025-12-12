"""
Веб-сервер для калькулятора Чёрча.
"""

import sys
import os
import re

# Добавляем путь к корневой директории для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify

try:
    from database import CalculationHistory
    db = CalculationHistory()
    DATABASE_AVAILABLE = True
except Exception as e:
    print(f"База данных недоступна: {e}")
    db = None
    DATABASE_AVAILABLE = False

try:
    from app.church import ChurchCalculator, church_to_int, int_to_church
except ImportError:
    try:
        from church import ChurchCalculator, church_to_int, int_to_church
    except ImportError:
        print("Ошибка: Не удалось найти модуль church.py")
        raise

app = Flask(__name__)
app.secret_key = 'church_calculator_secret_key_2024'

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

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор Чёрча</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #fff0f5 0%, #ffe4ec 100%);
            min-height: 100vh;
            color: #8b008b;
            padding: 20px;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.2rem;
            background: linear-gradient(135deg, #ff69b4, #ff1493);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .subtitle {
            color: #c71585;
            opacity: 0.8;
        }

        .calculator {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(255, 105, 180, 0.2);
            margin-bottom: 20px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .expression-input {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ff69b4;
            border-radius: 12px;
            background: #fffafa;
            color: #c71585;
            font-weight: 500;
        }

        .expression-input:focus {
            outline: none;
            border-color: #ff1493;
        }

        .buttons-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }

        .btn {
            height: 60px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn.number {
            background: linear-gradient(135deg, #ffb6c1, #ff91a4);
            color: #8b008b;
            border: 2px solid #ff69b4;
        }

        .btn.operation {
            background: linear-gradient(135deg, #ff85a2, #ff6b95);
            color: white;
            border: 2px solid #ff1493;
        }

        .btn.control {
            background: linear-gradient(135deg, #db7093, #c71585);
            color: white;
            border: 2px solid #8b008b;
        }

        .btn.equals {
            background: linear-gradient(135deg, #ff69b4, #ff1493);
            color: white;
            border: 2px solid #c71585;
            grid-column: span 2;
        }

        .result-group {
            margin-bottom: 20px;
        }

        .result-input {
            width: 100%;
            padding: 20px;
            font-size: 24px;
            border: 3px solid #ff69b4;
            border-radius: 12px;
            background: #fff0f5;
            color: #ff1493;
            font-weight: bold;
            text-align: center;
        }

        .error-group {
            border: 2px solid #ffb6c1;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 20px;
        }

        .error-header {
            background: linear-gradient(135deg, #ffe4ec, #ffd1dc);
            padding: 12px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            color: #c71585;
        }

        .clear-error {
            background: #ff69b4;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }

        .error-display {
            height: 80px;
            padding: 12px;
            background: #fffafa;
            overflow-y: auto;
            font-size: 13px;
            line-height: 1.4;
            color: #dc143c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Калькулятор Чёрча</h1>
            <p class="subtitle">Вычисления через λ-исчисление</p>
        </div>

        <div class="calculator">
            <div class="input-group">
                <input type="text" id="expressionInput" placeholder="Введите выражение" class="expression-input">
            </div>

            <div class="buttons-grid">
                <button class="btn number" data-value="7">7</button>
                <button class="btn number" data-value="8">8</button>
                <button class="btn number" data-value="9">9</button>
                <button class="btn operation" data-value="/">/</button>
                
                <button class="btn number" data-value="4">4</button>
                <button class="btn number" data-value="5">5</button>
                <button class="btn number" data-value="6">6</button>
                <button class="btn operation" data-value="*">×</button>
                
                <button class="btn number" data-value="1">1</button>
                <button class="btn number" data-value="2">2</button>
                <button class="btn number" data-value="3">3</button>
                <button class="btn operation" data-value="-">-</button>
                
                <button class="btn number" data-value="0">0</button>
                <button class="btn operation" data-value="^">^</button>
                <button class="btn operation" data-value="!">!</button>
                <button class="btn operation" data-value="+">+</button>
                
                <button class="btn control" id="clearBtn">C</button>
                <button class="btn control" id="backspaceBtn">←</button>
                <button class="btn equals" id="calculateBtn">=</button>
            </div>

            <div class="result-group">
                <input type="text" id="resultDisplay" readonly placeholder="Результат появится здесь..." class="result-input">
            </div>

            <div class="error-group">
                <div class="error-header">
                    <span>Сообщения об ошибках</span>
                    <button class="clear-error" id="clearErrorBtn">Очистить</button>
                </div>
                <div id="errorDisplay" class="error-display"></div>
            </div>
        </div>
    </div>

    <script>
        class CalculatorUI {
            constructor() {
                this.expressionInput = document.getElementById('expressionInput');
                this.resultDisplay = document.getElementById('resultDisplay');
                this.errorDisplay = document.getElementById('errorDisplay');
                this.initializeEventListeners();
            }

            initializeEventListeners() {
                // Кнопки цифр и операций
                document.querySelectorAll('.btn.number, .btn.operation').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        this.insertText(e.target.getAttribute('data-value'));
                    });
                });

                // Управляющие кнопки
                document.getElementById('clearBtn').addEventListener('click', () => this.clearInputs());
                document.getElementById('backspaceBtn').addEventListener('click', () => this.backspace());
                document.getElementById('calculateBtn').addEventListener('click', () => this.calculate());
                document.getElementById('clearErrorBtn').addEventListener('click', () => this.clearError());

                // Ввод с клавиатуры
                this.expressionInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.calculate();
                    }
                });
            }

            insertText(text) {
                const start = this.expressionInput.selectionStart;
                const end = this.expressionInput.selectionEnd;
                const currentValue = this.expressionInput.value;
                
                this.expressionInput.value = currentValue.substring(0, start) + text + currentValue.substring(end);
                this.expressionInput.selectionStart = this.expressionInput.selectionEnd = start + text.length;
                this.expressionInput.focus();
            }

            backspace() {
                const start = this.expressionInput.selectionStart;
                const end = this.expressionInput.selectionEnd;
                const currentValue = this.expressionInput.value;
                
                if (start === end && start > 0) {
                    this.expressionInput.value = currentValue.substring(0, start - 1) + currentValue.substring(end);
                    this.expressionInput.selectionStart = this.expressionInput.selectionEnd = start - 1;
                } else if (start !== end) {
                    this.expressionInput.value = currentValue.substring(0, start) + currentValue.substring(end);
                    this.expressionInput.selectionStart = this.expressionInput.selectionEnd = start;
                }
                this.expressionInput.focus();
            }

            clearInputs() {
                this.expressionInput.value = '';
                this.resultDisplay.value = '';
                this.errorDisplay.textContent = '';
                this.expressionInput.focus();
            }

            clearError() {
                this.errorDisplay.textContent = '';
            }

            async calculate() {
                try {
                    const expression = this.expressionInput.value.trim();
                    if (!expression) {
                        this.showError('Введите математическое выражение');
                        return;
                    }

                    // Очищаем предыдущие сообщения
                    this.errorDisplay.textContent = '';

                    const response = await fetch('/calculate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ expression: expression })
                    });

                    const data = await response.json();

                    if (data.success) {
                        this.resultDisplay.value = data.result;
                        // Показываем только предупреждения, если они есть
                        if (data.warning) {
                            this.showWarning(data.warning);
                        }
                    } else {
                        this.showError(data.error);
                    }

                } catch (error) {
                    this.showError('Ошибка соединения с сервером');
                }
            }

            showError(message) {
                this.resultDisplay.value = 'Ошибка';
                this.errorDisplay.textContent = message;
            }

            showWarning(message) {
                this.errorDisplay.textContent = message;
            }
        }

        // Инициализация при загрузке страницы
        document.addEventListener('DOMContentLoaded', () => {
            new CalculatorUI();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Главная страница."""
    return HTML

@app.route('/health')
def health_check():
    """Проверка статуса приложения и базы данных."""
    return jsonify({
        'status': 'healthy',
        'database_available': DATABASE_AVAILABLE
    })

@app.route('/calculate', methods=['POST'])
def calculate():
    """API endpoint для вычислений."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        expression = data.get('expression', '').strip()
        
        if not expression:
            return jsonify({'error': 'Введите математическое выражение'}), 400
        
        parsed = ExpressionParser.parse_expression(expression)
        operation = parsed[0]
        
        result = None
        warning = None
        
        if operation == 'factorial':
            n = parsed[1]
            
            if n != int(n):
                raise ValueError("Факториал определен только для целых чисел")
            
            church_n = int_to_church(int(n))
            result_church = ChurchCalculator.factorial(church_n)
            result = church_to_int(result_church)
            
        else:
            a, b = parsed[1], parsed[2]
            int_a, int_b = int(a), int(b)
            
            # Проверка для вычитания
            if operation == 'subtract' and int_a < int_b:
                warning = f"Внимание: уменьшаемое меньше вычитаемого. Ответ 0."
                result = 0
            else:
                church_a = int_to_church(int_a)
                church_b = int_to_church(int_b)
                
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
                    if int_b == 0:
                        raise ValueError("Деление на ноль")
                    result = int_a // int_b
                    
                elif operation == 'power':
                    result_church = ChurchCalculator.power(church_a, church_b)
                    result = church_to_int(result_church)
        
        # Сохраняем в базу данных если она доступна
        if DATABASE_AVAILABLE and db:
            db.save_calculation(
                expression=expression,
                result=result,
                operation_type=operation
            )
        
        response_data = {
            'success': True,
            'result': result,
            'database_available': DATABASE_AVAILABLE
        }
        
        if warning:
            response_data['warning'] = warning
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/history', methods=['GET'])
def get_history():
    """Получить историю вычислений."""
    if not DATABASE_AVAILABLE or not db:
        return jsonify({'error': 'База данных недоступна', 'history': []})
    
    limit = request.args.get('limit', 10, type=int)
    history = db.get_calculation_history(limit=limit)
    return jsonify({'history': history})

if __name__ == '__main__':
    print("Запуск веб-сервера калькулятора Чёрча...")
    print("Откройте в браузере: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)