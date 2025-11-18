import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clothing.clothing_items import Jacket, Pants
from clothing.suit import ThreePieceSuit

class TestJacket:
    """Тесты для класса Jacket"""
    
    def test_jacket_creation(self):
        """Тест создания объекта пиджака"""
        jacket = Jacket(size=50)
        assert jacket.size == 50
        assert jacket.name == "Пиджак"
    
    def test_jacket_fabric_consumption(self):
        """Тест расчета расхода ткани для пиджака"""
        jacket = Jacket(size=50, has_liner=True)
        consumption = jacket.calculate_fabric_consumption()
        expected = 1.5 * 50 + 0.5  # база + подклад
        assert consumption == expected
    
    def test_jacket_sewing_cost(self):
        """Тест расчета стоимости пошива пиджака"""
        jacket = Jacket(size=50, buttons_count=3)
        cost = jacket.calculate_sewing_cost()
        assert isinstance(cost, float)
        assert cost > 0

class TestPants:
    """Тесты для класса Pants"""
    
    def test_pants_creation(self):
        """Тест создания объекта брюк"""
        pants = Pants(size=52, pants_type="slim")
        assert pants.size == 52
        assert pants.pants_type == "slim"
    
    def test_pants_fabric_consumption_different_types(self):
        """Тест расхода ткани для разных типов брюк"""
        classic_pants = Pants(size=50, pants_type="classic")
        slim_pants = Pants(size=50, pants_type="slim")
        
        classic_consumption = classic_pants.calculate_fabric_consumption()
        slim_consumption = slim_pants.calculate_fabric_consumption()
        
        assert slim_consumption < classic_consumption

class TestThreePieceSuit:
    """Тесты для класса ThreePieceSuit"""
    
    def test_suit_creation(self):
        """Тест создания костюма-тройки"""
        jacket = Jacket(size=50)
        pants = Pants(size=52)
        suit = ThreePieceSuit(jacket, pants)
        
        assert suit.jacket == jacket
        assert suit.pants == pants
    
    def test_suit_total_cost(self):
        """Тест расчета общей стоимости костюма"""
        jacket = Jacket(size=50)
        pants = Pants(size=52)
        suit = ThreePieceSuit(jacket, pants)
        
        total_cost = suit.calculate_total_cost()
        assert isinstance(total_cost, float)
        assert total_cost > 0
    
    def test_suit_cost_components(self):
        """Тест что стоимость костюма включает все компоненты"""
        jacket = Jacket(size=50)
        pants = Pants(size=52)
        suit = ThreePieceSuit(jacket, pants)
        
        jacket_cost = jacket.calculate_sewing_cost()
        pants_cost = pants.calculate_sewing_cost()
        suit_cost = suit.calculate_total_cost()
        
        # Костюм должен стоить больше суммы пиджака и брюк (из-за жилета)
        assert suit_cost > jacket_cost + pants_cost

class TestIntegration:
    """Интеграционные тесты"""
    
    def test_complete_workflow(self):
        """Тест полного рабочего процесса"""
        jacket = Jacket(size=48, has_liner=True, buttons_count=2)
        pants = Pants(size=50, pants_type="classic", has_belt_loops=True)
        suit = ThreePieceSuit(jacket, pants)
        
        # Проверяем что все методы работают без ошибок
        jacket_consumption = jacket.calculate_fabric_consumption()
        pants_consumption = pants.calculate_fabric_consumption()
        suit_cost = suit.calculate_total_cost()
        
        assert jacket_consumption > 0
        assert pants_consumption > 0
        assert suit_cost > 0