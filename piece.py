import typing as tp
from spell import *
from effect import *
import random

if tp.TYPE_CHECKING:
    from field import Square
    from field import Field

#Списки условных обозначений, являющиеся стеной
BARRIERS = [False]
FOGS = [False]
NAME_TO_IND = {'attack': 1, 'move': 0}


class Piece:

    """
    Класс для шаблона Фигуры.
    """

    def __init__(self, team: str, field: "Field", cell: "Square", max_hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):

        """
        :team: команда фигуры
        :cell: клетка на которой расположена фигура
        :field: поле, на котором расположена фигура
        :radius_fov: радиус обзора в клетках
        :radius_move: дальность перемещения в клетках
        :fovs: видимые клетки в виде координат на поле
        :moves: клетки на которые можно перейти
        :max_hp: максимальные хп персонажа
        :hp: текущие хп персонажа
        :accuracy: базовый шанс попадания при атаке от 0 до 1
        :damage: базовый урон атаки
        :spell_list: лист со скилами
        :active_turn: bool параметр хранящий может ли походить клетка в этот ход
        """

        self.team = team
        self.cell = cell
        self.field = field
        self.radius_fov = radius_fov
        self.radius_move = radius_move
        self.max_hp = max_hp
        self.hp = max_hp
        self.accuracy = accuracy
        self.damage = damage
        self.spell_list = [Piece_Move()]
        self.effect_list = []
        self.active_turn = True
        self.AP = 2

    def get_fovs(self, cell = None) -> list[tuple["Square", "Square"]]:
        """
        Функция возвращает список всех видимых клеток.
        Функция вызывает функцию прорисовки растровой линии от центра до каждой клетки границы (граница беспрерывная спутенькой).
        :cell: передаётся, если требуется найти обзор не из текущей клетки
        """
        fovs = set()

        #цикл перебирает весю границу квадрата обзора
        #вершины квадрата находятся по прямой (вверх, вниз, влево и вправо) от клетки фигуры
        r = self.radius_fov
        x = 0
        y = r
        

        if cell is None:
            start_y, start_x = self.cell.get_pos()
        else:
            start_y, start_x = cell.get_pos()

        for i in range(4 * r):

            #рисуется растровая линия от клетки с фигурой до каждой пограничной
            fovs.update(self.get_view_for_line((start_x, start_y), (start_x + x, start_y + y)))

            if i < r:
                x += 1
            elif i < 3 * r:
                x -= 1
            else:
                x += 1

            if i < 2 * r:
                y -= 1
            else:
             y += 1

        #повторный цикл с меньшим радиусом для закрытия дыр
        r = self.radius_fov - 1
        x = 0
        y = r
        for i in range(4 * r):

            #рисуется растровая линия от клетки с фигурой до каждой пограничной
            fovs.update(self.get_view_for_line((start_x, start_y), (start_x + x, start_y + y)))

            if i < r:
                x += 1
            elif i < 3 * r:
                x -= 1
            else:
                x += 1

            if i < 2 * r:
                y -= 1
            else:
             y += 1

        foving_cell = []
        for pos in list(fovs):
            cell = self.field.get_square_by_pos(pos[0], pos[1])
            if cell != self.cell:
                foving_cell.append(cell)

        return foving_cell
        

    def get_view_for_line(self, start: tuple[int], end: tuple[int])  -> list[tuple[int, int]]:
        """
        Функция вычисляет через какие точки проходит линия обзора от одной клетки до другой.
        И возвращает путь до первой стены.
        Здесь x представляет колонку (col), а y - строчку (row).
        """
        #забираем координаты стартовой клетки и конечной
        x0, y0 = start
        x1, y1 = end

        #определяем длину проекции линии на оси
        dx = x1 - x0
        dy = y1 - y0

        #определяем, в какую сторону изменяется координата, чтобы идти от начала отрезка в конец
        sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
        sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

        #Определяем большую проекцию ошибку по которой будем считать
        if abs(dx) > abs(dy):
            pdx, pdy = sign_x, 0
            es, el = abs(dy), abs(dx)

        else:
            pdx, pdy = 0, sign_y
            es, el = abs(dx), abs(dy)

        #все дробные переменные умножаются на dx или dy соответственно
        #считаем ошибку, как расстояние между реальной координатой прямой
        #изначальное значение ошибки - половина клетки, так как прямая исходит из центра клетки
        error, t = el/2, 0

        #устанавливаем переменные отслеживающие маршрут
        x, y = x0, y0


        #проверяем, что не выходим за краницы массива
        if self.field.is_into_map(y, x):
            #создаём путь, куда попадают видимые клетки
            #первая клетка всегда попадает в путь
            #если клетка - стена то клетки после неё не попадают в видимые клетки
            way = [(y, x)]
            if self.field.is_fog(y, x):
                return way
        else:
            return []
        
        #идём циклом по проекции dx или dy
        while t < el:
            t += 1
            #ошибка меняется на угловой коэфициэнт соответсвенно умноженный
            error -= es

            #если ошибка больше клетки, то мы поднимаемся по проекции, которую не обходим
            if error < 0:
                error += el
                x += sign_x
                y += sign_y

            #иначе, движимся только вдоль проекции, что обходим
            else:
                x += pdx
                y += pdy
            
            if self.field.is_into_map(y, x):
                #вновь проверяем, а не смотрим ли мы сквозь стену?
                way.append((y, x))
                if self.field.is_fog(y, x):
                    return way
            
        return way
    
    def new_turn(self) -> None:

        """
        Функция восстанавливает значение активности фигуры
        """
        
        self.AP = 2

        for spell in self.spell_list:
            if spell.cooldown_now > 0:
                spell.cooldown_now -= 1

        for effect in self.effect_list:
            effect.timer -= 1
            if effect.timer == 0:
                effect.remove_effect(self)
                self.effect_list.remove(effect)

        self.active_turn = True

    def prepare_spell(self, id_spell: str) -> list["Square"]:
        
        """
        Функция вызывается, когда пользователь нажимает на способность.
        Возвращает клетки, на которые можно использовать способность.
        :id_spell: кодовое слово способности
        """

        #Ищём способность в списке по id
        spell = None
        for i_spell in self.spell_list:
            if i_spell.id == id_spell:
                spell = i_spell
                break

        return spell.target(self)

    def cast_spell(self, id_spell: str, cell: "Square") -> None:

        """
        Функция вызывается, когда пользователь активирует способность.
        Производит эффект способности
        :id_spell: кодовое слово способности
        :cell: клетка на которую способность использовали
        """

        #Ищём способность в списке по id
        spell = None
        for i_spell in self.spell_list:
            if i_spell.id == id_spell:
                spell = i_spell
                break

        spell.cast(self, cell)
        spell.cooldown_now = spell.cooldown
        self.AP -= spell.cost
        if self.AP < 0:
            self.AP = 0
        if self.AP == 0:
            self.active_turn = False

class Pawn(Piece):

    """
    Класс пешки
    """

    def __init__(self, team: str, field: "Field", cell: "Square", max_hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):
        #инициируем фигуру
        super().__init__(team, field, cell, max_hp, accuracy, damage, radius_move, radius_fov)
        #собираем спелы специальной функцией
        self.create_spell_list()

    def create_spell_list(self) -> None:
        
        """
        Функция создаёт объекты класса Spell, прописывая для них специфичные функции выбора цели и эффекта
        !x и y инверсированны относительно обычной координатной оси
        """

        #Создаём способность Атака и добавляем её в список способностей
        self.spell_list.append(PawnAttack1())