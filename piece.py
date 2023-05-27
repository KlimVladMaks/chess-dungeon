import typing as tp
from spell import *
from effect import *
import random

#Списки условных обозначений, являющиеся стеной
BARRIERS = [False]
FOGS = [False]
NAME_TO_IND = {'attack': 1, 'move': 0}

class _Square:

    """
    Фиктивный класс шахматной клетки.
    (Используется для задания типа данных).
    Функции прописаны для возможности тестового запуска.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.is_exist = True
        self.inner_piece = None
        
    def get_inner_piece(self, x, y):
        return 0
    
    def del_inner_piece(self):
        return 0
    
    def add_inner_piece(self):
        return 0
    
    def get_pos(self):
        return 0, 0

class _Field:

    """
    Фиктивный класс шахматной доски.
    (Используется для задания типа данных).
    Функции прописаны для возможности тестового запуска.
    """
    
    def get_square_by_pos(self, x, y):
        return _Square()
    

class Piece:

    """
    Класс для шаблона Фигуры.
    """

    def __init__(self, team: str, field: _Field, cell: _Square, max_hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):

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
        Moving = Spell('move', "Перемещение", "Переместитесь на клетку в зоне движения", 0, 1, lambda: None, self.get_moves, self.moving)
        self.spell_list = [Moving]
        self.effect_list = []
        self.active_turn = True
        self.AP = 2

    def get_moves(self) -> list[tuple[_Square, _Square]]:
        
        """
        Функция возвращает все клетки до которых можно дойти.
        Работает это через обход в ширину со стартовой клетки.
        """

        #храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        # и ещё один массив, чтобы узнавать длину и при этом спокойно узнавать, были ли мы уже в этой клетке
        i = 0
        moves = []
        len_way = []

        #проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = self.cell.get_pos()
        if self.field.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))
            len_way.append(0)

        while i < len(moves):

            #проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if (not (moves[i][0] + 1, moves[i][1]) in moves #ещё не посетили
                    and len_way[i] < self.radius_move #не дальше, чем движение клетки
                        and self.field.is_into_map(moves[i][0] + 1, moves[i][1]) #в пределах поля
                            and not self.field.is_barrier(moves[i][0] + 1, moves[i][1]) #можно пройти
                                and self.field.get_square_by_pos(moves[i][0] + 1, moves[i][1]).inner_piece is None): #нет фигуры
                moves.append((moves[i][0] + 1, moves[i][1]))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                    and len_way[i] < self.radius_move
                        and self.field.is_into_map(moves[i][0] - 1, moves[i][1])
                            and not self.field.is_barrier(moves[i][0] - 1, moves[i][1])
                                and self.field.get_square_by_pos(moves[i][0] - 1, moves[i][1]).inner_piece is None):
                moves.append((moves[i][0] - 1, moves[i][1]))
                len_way.append(len_way[i] + 1)
            
            if (not (moves[i][0], moves[i][1] + 1) in moves
                    and len_way[i] < self.radius_move
                        and self.field.is_into_map(moves[i][0], moves[i][1] + 1)
                            and not self.field.is_barrier(moves[i][0], moves[i][1] + 1)
                                and self.field.get_square_by_pos(moves[i][0], moves[i][1] + 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] + 1))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0], moves[i][1] - 1) in moves
                    and len_way[i] < self.radius_move
                        and self.field.is_into_map(moves[i][0], moves[i][1] - 1)
                            and not self.field.is_barrier(moves[i][0], moves[i][1] - 1)
                                and self.field.get_square_by_pos(moves[i][0], moves[i][1] - 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] - 1))
                len_way.append(len_way[i] + 1)

            #переходим к следующему элементу
            i += 1


        #переводим позиции в клетки
        moving_cell = []
        for pos in moves:
            cell = self.field.get_square_by_pos(pos[0], pos[1])
            if cell != self.cell:
                moving_cell.append(cell)

        return moving_cell
    
    def moving(self, new_cell: _Square) -> None:

        """
        Функция переставляет фигуру на новую клетку.
        Возвращает пару - клетку с которой ушла и клетку на которую пришла фигура.
        """

        old_cell = self.cell
        self.cell = new_cell
        old_cell.del_inner_piece()
        new_cell.add_inner_piece(self)

    def get_fovs(self, cell = None) -> list[tuple[_Square, _Square]]:
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
                effect.remove_effect(self, effect.strength)
                self.effect_list.remove(effect)

        self.active_turn = True

    def prepare_spell(self, id_spell: str) -> list[_Square]:
        
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

        return spell.target()

    def cast_spell(self, id_spell: str, cell: _Square) -> None:

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

        spell.cast(cell)
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

    def __init__(self, team: str, field: _Field, cell: _Square, max_hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):
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
        Attack = Spell('attack', "Атака", "Атакуйте выбранную цель", 1, 2, self.attack_spell_zone, self.attack_spell_target, self.attack_spell_cast)
        self.spell_list.append(Attack)


    """
    Способности фигуры:
    """

    def attack_spell_zone(self, host_cell: _Square = None) -> list[tuple[int, int]]:

        """
        Воспомогательная функция, возвращающая набор координат потенциальных клеток.
        Требуется отдельная фильтрация и перевод в объекты класса Square
        """

        if host_cell is None:
            host_cell = self.cell

        row_pos, col_pos = host_cell.get_pos()
        x, y = row_pos, col_pos
            
        #задаём список возможных целей для атаки
        #пешка атакует на одну клетку вокруг себя
        potential = [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x + 1, y + 1),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]

        return potential

    def attack_spell_target(self) -> list[_Square]:

        potential = self.attack_spell_zone()

        target_list = []
            
        #cреди этих клеток можно атаковать только те, на которых стоят фигуры (система свой-чужой не работает хе)
        for cell in potential:
            piece = self.field.get_square_by_pos(cell[0], cell[1]).inner_piece
            if self.field.is_into_map(cell[0], cell[1]) and isinstance(piece, Piece) and piece.team != self.team:
                 target_list.append(self.field.get_square_by_pos(cell[0], cell[1]))

        return target_list
        
    def attack_spell_cast(self, other: _Square) -> None:

        #забираем фигуру из клетки
        other = other.inner_piece

        #Если фигура попала, она наносит урон равный своим хп
        if random.random() < self.accuracy:
            print(f"Атакующая фигура попала и нанесла {self.damage} урона!")
            other.hp -= self.damage
            print(f"Оставшиеся хп жертвы: {other.hp}/{other.max_hp}")

            if [effect.id for effect in other.effect_list].count('speed_reduction') == 0:
                print('Также на фигуру наложен дебафф!')
                effect = speed_reduction
                effect.timer = 2
                effect.strength = 1
                other.effect_list.append(effect)
                effect.get_effect(other, effect.strength)

            #Если фигуры хп падают до 0 и ниже, удаляем её с поля
            if other.hp <= 0:
                print("Сильный удар разбивает жертву в каменную крошку!")
                other.cell.del_inner_piece()
        else:
            print(f"Атакующая фигура промахнулась")

if __name__ == '__main__':
    
    b = Pawn('p', _Field(), _Square(), 10, 0.5, 2, 3, 1)
    a = Pawn('p', _Field(), _Square(), 10, 0.5, 2, 3, 1)

    print(isinstance(a, Piece))