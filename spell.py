import typing as tp


class Spell:
    
    """
    Этот класс хранит информацию о способности фигуры
    """

    def __init__(self, id: str, name: str, description: str, cooldown: int, cost: int, zone = lambda: None, target = lambda: None, cast = lambda: None):

        """
        :cooldown: время перезарядки способности в ходах
        :cooldown_now: время, которое осталось до конца перезарядки в ходах
        :name: название способности
        :description: описание способности
        :zone: функция, возвращающая зону активации способности, может принимать в качестве аргумента исходную клетку
        :target: функция, возвращающая целевые клетки
        :cast: функция, вносящая изменения соответсвующие способности
        """

        self.id = id
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.cooldown_now = 0
        self.cost = cost
        self.zone = zone
        self.target = target
        self.cast = cast