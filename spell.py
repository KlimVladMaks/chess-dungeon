import typing as tp


class Spell:
    
    """
    Этот класс хранит информацию о способности фигуры
    """

    def __init__(self, cooldown: int, name: str, description: str, zone = None, target = None, cast = None):

        """
        :cooldown: время перезарядки способности в ходах
        :cooldown_now: время, которое осталось до конца перезарядки в ходах
        :name: название способности
        :description: описание способности
        :zone: функция, возвращающая зону активации способности, может принимать в качестве аргумента исходную клетку
        :target: функция, возвращающая целевые клетки
        :cast: функция, вносящая изменения соответсвующие способности
        """

        self.cooldown = cooldown
        self.cooldown_now = 0
        self.name = name
        self.description = description
        self.zone = zone
        self.target = target
        self.cast = cast