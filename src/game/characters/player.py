from .character import Character
from .stats import Stats
from ..items.inventory import Inventory

class Player(Character):
  def __init__(self, name: str, hp: int, pos: tuple[float, float], stats: Stats, 
               exp: int, money: int, level: int, inventory: Inventory) -> None:
    super().__init__(name, hp, pos, stats)
    self.exp = exp
    self.money = money
    self.level = level
    self.inventory = inventory
