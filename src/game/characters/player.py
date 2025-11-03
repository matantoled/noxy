from .character import Character
from .stats import Stats

class Player(Character):
  def __init__(self, name: str, hp: int, pos: tuple[float, float], stats: Stats, 
               exp: int, inventory_size: int) -> None:
    super().__init__(name, hp, pos, stats)
    self.exp = exp
    self.inventory_size = inventory_size
    
