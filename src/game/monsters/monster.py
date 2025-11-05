from ..characters.character import Character
from ..characters.stats import Stats

class Monster(Character):
  def __init__(self, name: str, pos: tuple[float, float], 
               stats: Stats, current_hp: int = 1) -> None:
    
    super().__init__(name, pos, stats, current_hp)



    """
  def __init__(self, name: str, pos: tuple[float, float], 
               stats: Stats, current_hp: int = 1,) -> None:
"""