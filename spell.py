import typing as tp

class Spell:
    
    """
    Этот класс хранит информацию о способности фигуры
    """

    def __init__(self, cooldown: int, name: str, description: str, target = None, cast = None):

        """
        :cooldown: время перезарядки способности в ходах
        :cooldown_now: время, которое осталось до конца перезарядки в ходах
        :name: название способности
        :description: описание способности
        :target: функция, возвращающая целевые клетки
        :cast: функция, вносящая изменения соответсвующие способности
        """

        self.cooldown = cooldown
        self.cooldown_now = 0
        self.name = name
        self.description = description
        self.target = target
        self.cast = cast