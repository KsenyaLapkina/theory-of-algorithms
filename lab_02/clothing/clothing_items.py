from .garments import Garment

class Jacket(Garment):
    def __init__(self, size, has_liner=False, buttons_count=3, fabric_cost_per_m2=300.0):  # было 500
        super().__init__("Пиджак", size, fabric_cost_per_m2)
        self.has_liner = has_liner
        self.buttons_count = buttons_count
        self.calculate_fabric_consumption()

    def calculate_fabric_consumption(self):
        base_consumption = 1.5 * self.size
        liner_consumption = 0.5 if self.has_liner else 0
        self._fabric_consumption = base_consumption + liner_consumption
        return self._fabric_consumption

    def calculate_sewing_cost(self, labor_cost=1500.0):  # было 2000
        fabric_cost = self.calculate_fabric_cost()
        buttons_cost = self.buttons_count * 50  # было 100
        return fabric_cost + labor_cost + buttons_cost

    def __str__(self):
        return f"{super().__str__()}, расход ткани: {self._fabric_consumption:.2f} м², подклад: {'да' if self.has_liner else 'нет'}"

class Pants(Garment):
    def __init__(self, size, pants_type="classic", has_belt_loops=True, fabric_cost_per_m2=250.0):  # было 400
        super().__init__("Брюки", size, fabric_cost_per_m2)
        self.pants_type = pants_type
        self.has_belt_loops = has_belt_loops
        self.calculate_fabric_consumption()

    def calculate_fabric_consumption(self):
        base_consumption = 1.2 * self.size
        
        # Модификаторы расхода для разных типов брюк
        type_modifiers = {
            "classic": 1.0,      # классические
            "slim": 0.9,         # зауженные
            "wide": 1.3,         # широкие
            "sport": 0.8         # спортивные
        }
        
        modifier = type_modifiers.get(self.pants_type, 1.0)
        self._fabric_consumption = base_consumption * modifier
        return self._fabric_consumption

    def calculate_sewing_cost(self, labor_cost=1200.0):  # было 1500
        fabric_cost = self.calculate_fabric_cost()
        loops_cost = 200 if self.has_belt_loops else 0  # было 300
        return fabric_cost + labor_cost + loops_cost

    def __str__(self):
        type_names = {
            "classic": "классические",
            "slim": "зауженные", 
            "wide": "широкие",
            "sport": "спортивные"
        }
        pants_type_name = type_names.get(self.pants_type, self.pants_type)
        return f"{super().__str__()}, тип: {pants_type_name}, расход ткани: {self._fabric_consumption:.2f} м²"