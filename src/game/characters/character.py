from .stats import Stats

class Character:
  def __init__(self, name: str, hp: int, pos: tuple[float, float], stats: Stats) -> None:
    self.name = name
    self.max_hp = hp
    self.current_hp = hp
    self.pos = pos
    self.stats = stats