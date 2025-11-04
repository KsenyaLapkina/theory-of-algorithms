from .clothing_items import Jacket, Pants

class ThreePieceSuit:
    def __init__(self, jacket, pants, waistcoat_consumption=0.8):
        self.jacket = jacket
        self.pants = pants
        self.waistcoat_consumption = waistcoat_consumption

    def calculate_total_cost(self):
        jacket_cost = self.jacket.calculate_sewing_cost()
        pants_cost = self.pants.calculate_sewing_cost()
        waistcoat_fabric_cost = self.waistcoat_consumption * self.jacket.fabric_cost_per_m2
        waistcoat_sewing_cost = 800 
        waistcoat_total_cost = waistcoat_fabric_cost + waistcoat_sewing_cost

        total_cost = jacket_cost + pants_cost + waistcoat_total_cost
        return total_cost

    def __str__(self):
        total_cost = self.calculate_total_cost()
        return f"Костюм-тройка:\n  - {self.jacket}\n  - {self.pants}\n  - Жилет (расход: {self.waistcoat_consumption} м²)\nИтоговая стоимость: {total_cost:.2f} руб."

    def __repr__(self):
        return f"ThreePieceSuit({repr(self.jacket)}, {repr(self.pants)})"