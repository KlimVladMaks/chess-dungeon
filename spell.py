import typing as tp

class Spell():
    
    """
    Этот класс хранит информацию о способности определённой фигуры
    """

    def __init__(self, cooldown: int, name: str, description: str, target = None, cast = None):

        self.cooldown = cooldown
        self.cooldown_now = cooldown
        self.name = name
        self.description = description
        self.target = target
        self.cast = cast