import time
import logging
import concurrent.futures
from typing import Dict, List, Callable, Iterator, Any
from datetime import datetime

from .database import Database
from .exceptions import InputValidationError, DataProcessingError

logger = logging.getLogger(__name__)

class GeneratorTasks:
    """Класс для реализации всех генераторов"""
    
    def __init__(self):
        self.db = Database()
    
    # Задание 1: Генератор комбинаций трех цифр
    def task1_generator(self) -> Iterator[int]:
        """Генератор всех сочетаний из трех цифр (000-999)"""
        try:
            self.db.log_activity("GENERATOR_START", "Запуск генератора комбинаций")
            
            digits = "0123456789"
            for i in digits:
                for j in digits:
                    for k in digits:
                        try:
                            yield int(i + j + k)
                        except ValueError as e:
                            raise DataProcessingError(f"Ошибка преобразования: {e}")
            
            self.db.log_activity("GENERATOR_END", "Генератор завершен")
            
        except Exception as e:
            self.db.log_activity("ERROR", f"Ошибка в генераторе: {e}")
            raise
    
    # Задание 2: Генератор значений функции
    def task2_generator(self, a: float, b: float, func: Callable[[float], float]) -> Iterator[float]:
        """Генератор значений функции f(x) на интервале [a;b] с шагом 0.01"""
        try:
            if a > b:
                raise InputValidationError("Начало интервала a не может быть больше конца b")
            
            self.db.log_activity("FUNCTION_START", f"Генерация функции на [{a}, {b}]")
            
            x = a
            while x <= b:
                try:
                    yield func(x)
                except Exception as e:
                    raise DataProcessingError(f"Ошибка вычисления в точке x={x}: {e}")
                x = round(x + 0.01, 2)
            
            self.db.log_activity("FUNCTION_END", "Генерация функции завершена")
            
        except InputValidationError:
            raise
        except Exception as e:
            self.db.log_activity("ERROR", f"Ошибка в генераторе функции: {e}")
            raise
    
    # Задание 3: Сортировка словаря
    def get_sort(self, dictionary: Dict[str, str]) -> List[str]:
        """Сортировка словаря по убыванию ключей"""
        try:
            if not isinstance(dictionary, dict):
                raise InputValidationError("Входной параметр должен быть словарем")
            
            self.db.log_activity("SORT_START", f"Сортировка словаря ({len(dictionary)} элементов)")
            
            sorted_keys = sorted(dictionary.keys(), reverse=True)
            result = [dictionary[key] for key in sorted_keys]
            
            self.db.log_activity("SORT_END", f"Сортировка завершена")
            
            return result
            
        except Exception as e:
            self.db.log_activity("ERROR", f"Ошибка при сортировке: {e}")
            raise
    
    # ДОБАВЛЯЕМ ЭТОТ МЕТОД
    def generate_combinations(self, count: int = 50) -> List[Dict[str, Any]]:
        """Генерация указанного количества комбинаций (последовательная версия)"""
        start_time = time.time()
        result = []
        
        try:
            gen = self.task1_generator()
            for i, num in enumerate(gen):
                if i >= count:
                    break
                result.append({
                    'id': i + 1,
                    'combination': f"{num:03d}",
                    'value': num,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
            
            # Сохраняем статистику
            duration_ms = int((time.time() - start_time) * 1000)
            self.db.save_stats(
                operation="combinations",
                count=len(result),
                parameters={"requested_count": count},
                duration_ms=duration_ms
            )
            
            return result
            
        except Exception as e:
            self.db.log_activity("ERROR", f"Ошибка генерации комбинаций: {e}")
            raise
    
    # ДОБАВЛЯЕМ ЭТОТ МЕТОД
    def generate_combinations_parallel(self, count: int = 50, num_threads: int = 4) -> List[Dict[str, Any]]:
        """Параллельная генерация комбинаций с использованием ThreadPoolExecutor"""
        start_time = time.time()
        
        def generate_chunk(start_idx, end_idx, max_items):
            """Генерирует часть комбинаций в одном потоке"""
            chunk = []
            digits = "0123456789"
            
            # Вычисляем начальные цифры для этого потока
            for i in range(start_idx, min(end_idx, len(digits))):
                for j in range(len(digits)):
                    for k in range(len(digits)):
                        if len(chunk) >= max_items:
                            return chunk
                        combination = int(digits[i] + digits[j] + digits[k])
                        chunk.append({
                            'combination': f"{combination:03d}",
                            'value': combination
                        })
            return chunk
        
        try:
            digits_count = len("0123456789")
            chunk_size = max(1, digits_count // num_threads)
            items_per_thread = (count // num_threads) + 1
            
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for i in range(0, digits_count, chunk_size):
                    future = executor.submit(generate_chunk, i, i + chunk_size, items_per_thread)
                    futures.append(future)
                
                for future in concurrent.futures.as_completed(futures):
                    results.extend(future.result())
            
            # Ограничиваем до нужного количества и сортируем
            results = sorted(results, key=lambda x: x['value'])[:count]
            
            # Форматируем результат
            formatted_results = []
            for i, item in enumerate(results):
                formatted_results.append({
                    'id': i + 1,
                    'combination': item['combination'],
                    'value': item['value'],
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Сохраняем статистику
            self.db.save_stats(
                operation="combinations_parallel",
                count=len(formatted_results),
                parameters={"requested_count": count, "threads": num_threads},
                duration_ms=duration_ms
            )
            
            return formatted_results
            
        except Exception as e:
            self.db.log_activity("ERROR", f"Ошибка параллельной генерации: {e}")
            raise
    
    # ДОБАВЛЯЕМ ЭТОТ МЕТОД
    def generate_function_values(self, a: float = -20, b: float = 100, count: int = 20) -> List[Dict[str, Any]]:
        """Генерация значений функции"""
        start_time = time.time()
        result = []
        
        try:
            func = lambda x: -1.5 * x + 2
            gen = self.task2_generator(a, b, func)
            
            for i, value in enumerate(gen):
                if i >= count:
                    break
                
                x_val = a + i * 0.01
                result.append({
                    'id': i + 1,
                    'x': round(x_val, 2),
                    'f(x)': round(value, 4),
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
            
            # Сохраняем статистику
            duration_ms = int((time.time() - start_time) * 1000)
            self.db.save_stats(
                operation="function_values",
                count=len(result),
                parameters={"a": a, "b": b, "requested_count": count},
                duration_ms=duration_ms
            )
            
            return result
            
        except Exception as e:
            self.db.log_activity("ERROR", f"Ошибка генерации функции: {e}")
            raise
    
    def benchmark_performance(self, count: int = 1000) -> Dict[str, Any]:
        """Сравнение производительности последовательной и параллельной версий"""
        results = {}
        
        # Последовательная версия
        start_time = time.time()
        sequential_result = self.generate_combinations(count)
        sequential_time = time.time() - start_time
        results['sequential'] = {
            'time': sequential_time,
            'count': len(sequential_result),
            'time_per_item': sequential_time / len(sequential_result) if len(sequential_result) > 0 else 0
        }
        
        # Параллельная версия (4 потока)
        start_time = time.time()
        parallel_result = self.generate_combinations_parallel(count, num_threads=4)
        parallel_time = time.time() - start_time
        results['parallel'] = {
            'time': parallel_time,
            'count': len(parallel_result),
            'time_per_item': parallel_time / len(parallel_result) if len(parallel_result) > 0 else 0,
            'threads': 4
        }
        
        # Вычисляем ускорение
        if parallel_time > 0:
            speedup = sequential_time / parallel_time
            results['speedup'] = speedup
            results['efficiency'] = (speedup / 4) * 100  # Эффективность использования потоков
            
            # Логируем результаты
            self.db.log_activity(
                "PERFORMANCE_BENCHMARK",
                f"Sequential: {sequential_time:.3f}s, Parallel: {parallel_time:.3f}s, Speedup: {speedup:.2f}x"
            )
        
        return results