from abc import ABC, abstractmethod

class Garment(ABC):
    def __init__(self, name, size, fabric_cost_per_m2=10.0):
        self.name = name
        self.size = size
        self.fabric_cost_per_m2 = fabric_cost_per_m2
        self._fabric_consumption = 0.0

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Размер должен быть положительным числом.")
        self._size = value

    @abstractmethod
    def calculate_fabric_consumption(self):
        pass

    @abstractmethod
    def calculate_sewing_cost(self, labor_cost=50.0):
        pass

    def calculate_fabric_cost(self):
        self.calculate_fabric_consumption()
        return self._fabric_consumption * self.fabric_cost_per_m2

    def __str__(self):
        return f"{self.name} (размер: {self.size})"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.size})"