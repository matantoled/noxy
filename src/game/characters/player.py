from .character import Character
from .stats import Stats
from ..items.inventory import Inventory

class Player(Character):
  def __init__(self, name: str, pos: tuple[float, float], 
               stats: Stats, inventory: Inventory, current_hp: int = 0,
                exp: int = 0, money: int = 0, level: int = 1) -> None:
    
    super().__init__(name, pos, stats, current_hp)
    self.exp = exp
    self.money = money
    self.level = level
    self.inventory = inventory

