"""
Модуль реализует кодирование Чёрча для представления натуральных чисел и арифметических операций в рамках λ-исчисления
"""

from typing import Callable, Any


class ChurchNumeral:
    """
    Класс, представляющий церковные числа.
    """
    
    def __init__(self, numeral: Callable[[Callable], Callable]) -> None:
        self.numeral = numeral
    
    def __call__(self, f: Callable) -> Callable:
        return self.numeral(f)
    
    def __str__(self) -> str:
        return str(self.to_int())
    
    def to_int(self) -> int:
        return self.numeral(lambda x: x + 1)(0)


class ChurchCalculator:
    """
    Класс-калькулятор для выполнения арифметических операций над церковными числами.
    """
    
    @staticmethod
    def zero() -> ChurchNumeral:
        return ChurchNumeral(lambda f: lambda x: x)
    
    @staticmethod
    def one() -> ChurchNumeral:
        return ChurchNumeral(lambda f: lambda x: f(x))
    
    @staticmethod
    def succ(n: ChurchNumeral) -> ChurchNumeral:
        return ChurchNumeral(lambda f: lambda x: f(n(f)(x)))
    
    @staticmethod
    def pred(n: ChurchNumeral) -> ChurchNumeral:
        """функция предшествования."""
        if n.to_int() == 0:
            return ChurchCalculator.zero()
        
        def predecessor(f: Callable) -> Callable:
            def inner(x: Any) -> Any:
                counter = [0]
                result = [x]
                
                def wrapper(y: Any) -> Any:
                    counter[0] += 1
                    if counter[0] <= n.to_int() - 1:
                        result[0] = f(y)
                    return result[0]
                
                n(wrapper)(x)
                return result[0]
            return inner
        return ChurchNumeral(predecessor)
    
    @staticmethod
    def add(m: ChurchNumeral, n: ChurchNumeral) -> ChurchNumeral:
        return ChurchNumeral(lambda f: lambda x: m(f)(n(f)(x)))
    
    @staticmethod
    def subtract(m: ChurchNumeral, n: ChurchNumeral) -> ChurchNumeral:
        """Исправленное вычитание."""
        n_int = n.to_int()
        result = m
        
        for _ in range(n_int):
            if result.to_int() > 0:
                result = ChurchCalculator.pred(result)
            else:
                break
        return result
    
    @staticmethod
    def multiply(m: ChurchNumeral, n: ChurchNumeral) -> ChurchNumeral:
        return ChurchNumeral(lambda f: m(n(f)))
    
    @staticmethod
    def power(m: ChurchNumeral, n: ChurchNumeral) -> ChurchNumeral:
        return ChurchNumeral(n(m))
    
    @staticmethod
    def factorial(n: ChurchNumeral) -> ChurchNumeral:
        def fact_rec(num: ChurchNumeral, acc: ChurchNumeral) -> ChurchNumeral:
            if num.to_int() <= 1:
                return acc
            return fact_rec(
                ChurchCalculator.pred(num),
                ChurchCalculator.multiply(acc, num)
            )
        
        return fact_rec(n, ChurchCalculator.one())
    
    @staticmethod
    def from_int(n: int) -> ChurchNumeral:
        if n < 0:
            raise ValueError("Church numerals can only represent non-negative integers")
        
        church_num = ChurchCalculator.zero()
        for _ in range(n):
            church_num = ChurchCalculator.succ(church_num)
        return church_num


def church_to_int(church_num: ChurchNumeral) -> int:
    return church_num.to_int()


def int_to_church(n: int) -> ChurchNumeral:
    return ChurchCalculator.from_int(n)