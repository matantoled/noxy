from .stats import Stats

class Character:
  def __init__(self, name: str, pos: tuple[float, float], 
               stats: Stats, current_hp: int = 0) -> None:
    self.name = name
    self.current_hp = current_hp
    self.pos = pos
    self.stats = stats
    self.is_alive = True

  
  """
  function : move_to, update hp, update position, take_damage, heal
  """