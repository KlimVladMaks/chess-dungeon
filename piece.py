import typing as tp
from spell import *
import random

#Списки условных обозначений, являющиеся стеной
BARRIERS = [0]
FOGS = [0]

class Cell():

    """
    Какая-то заглушка
    """

    def __init__(self):
        self.x = 0
        self.y = 0
    
    def get_type_cell_to_pos(self, x, y):
        return 0
    
    def get_object_in_cell(self, x, y):
        return 0
    

class Piece():

    def __init__(self, cell, hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):
        """
        Пока что фигура хранит копию поля, чтобы обращаться к состаянию клеток
        """

        self.cell = cell #клетка на которой находится фигура
        self.radius_fov = radius_fov #радиус обзора
        self.radius_move = radius_move #дальность движения
        self.fovs = self.get_fovs()
        self.moves = self.get_moves()
        self.hp = hp
        self.accuracy = accuracy
        self.damage = damage
        self.spell_list = []
        print('HOOO')

    def is_barrier(self, x: int, y: int) -> bool:

        """
        Функция проверяет, является ли клетка непроницаемой для движения
        !!! Название Атрибутов клетки переписать
        """

        if self.cell.get_type_cell_to_pos(x, y) in BARRIERS:
            return True
    
        return False
    
    def is_fog(self, x: int, y: int) -> bool:

        """
        Функция проверяет, является ли клетка непроницаемой для обзора
        !!! Название Атрибутов клетки переписать
        """

        if self.cell.get_type_cell_to_pos(x, y) in FOGS:
            return True
    
        return False

    def is_into_map(self, x: int, y: int) -> bool:
        """
        Проверяет, существует ли клетка по данной координате
        !!! Название Атрибутов клетки переписать
        """

        if self.cell.get_type_cell_to_pos(x, y) is None:
            return False
        
        return True


    def get_moves(self) -> list[tuple[int]]:
        """
        Функция возвращает все клетки до которых можно дойти
        Работает это через обход в ширину со стартовой клетки
        """

        #храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        # и ещё один массив, чтобы узнавать длину и при этом спокойно узнавать, были ли мы уже в этой клетке
        i = 0
        moves = []
        len_way = []

        #проверим о выходе за пределы массива
        if self.is_into_map(self.cell.x, self.cell.y):
            moves.append((self.cell.x, self.cell.y))
            len_way.append(0)

        while i < len(moves):

            #проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива
            if (not (moves[i][0] + 1, moves[i][1]) in moves #ещё не посетили
                    and len_way[i] < self.radius_move #не дальше, чем движение клетки
                        and self.is_into_map(moves[i][1], moves[i][0] + 1) #в пределах поля
                            and not self.is_barrier(moves[i][0] + 1, moves[i][1])): #можно пройти
                moves.append((moves[i][0] + 1, moves[i][1]))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                    and len_way[i] < self.radius_move
                        and self.is_into_map(moves[i][1], moves[i][0] - 1)
                            and not self.is_barrier(moves[i][0] - 1, moves[i][1])):
                moves.append((moves[i][0] - 1, moves[i][1]))
                len_way.append(len_way[i] + 1)
            
            if (not (moves[i][0], moves[i][1] + 1) in moves
                    and len_way[i] < self.radius_move
                        and self.is_into_map(moves[i][1] + 1, moves[i][0])
                            and not self.is_barrier(moves[i][0], moves[i][1] + 1)):
                moves.append((moves[i][0], moves[i][1] + 1))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0], moves[i][1] - 1) in moves
                    and len_way[i] < self.radius_move
                        and self.is_into_map(moves[i][1] - 1, moves[i][0])
                            and not self.is_barrier(moves[i][0], moves[i][1] - 1)):
                moves.append((moves[i][0], moves[i][1] - 1))
                len_way.append(len_way[i] + 1)

            #переходим к следующему элементу
            i += 1

        return moves
    

    def get_fovs(self) -> list:
        """
        Функция возвращает список всех видимых клеток.
        Функция вызывает функцию прорисовки растровой линии от центра до каждой клетки границы (граница беспрерывная спутенькой)
        """
        fovs = set()

        #цикл перебирает весю границу квадрата обзора
        #вершины квадрата находятся по прямой (вверх, вниз, влево и вправо) от клетки фигуры
        r = self.radius_fov
        x = 0
        y = r
        for i in range(4 * r):

            #рисуется растровая линия от клетки с фигурой до каждой пограничной
            fovs.update(self.get_view_for_line((self.cell.x, self.cell.y), (self.cell.x + x, self.cell.y + y)))

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
            fovs.update(self.get_view_for_line((self.cell.x, self.cell.y), (self.cell.x + x, self.cell.y + y)))

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

        return list(fovs)
        

    def get_view_for_line(self, start: tuple[int], end: tuple[int])  -> list[tuple[int]]:
        """
        Функция вычисляет через какие точки проходит линия обзора от одной клетки до другой.
        И возвращает путь до первой стены
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


        #проверяем, что не выходим за краницы массивав
        if self.is_into_map(x, y):
            #создаём путь, куда попадают видимые клетки
            #первая клетка всегда попадает в путь
            #если клетка - стена то клетки после неё не попадают в видимые клетки
            way = [(y,x)]
            if self.is_fog(y, x):
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
            
            if self.is_into_map(x, y):
                #вновь проверяем, а не смотрим ли мы сквозь стену?
                way.append((y,x))
                if self.fog(y, x):
                    return way
            
        return way
    
    def moving(self, new_cell) -> None:
        """
        Функция переставляет фигуру на новую клетку
        """

        self.cell = new_cell
        self.fovs = self.get_fovs()
        self.moves = self.get_moves()

    def prepare_spell(self, ind_spell: int):
        """
        Функция вызывается, когда пользователь нажимает на способность.
        Возвращает клетки, на которые можно использовать способность
        """

        return self.spell_list[ind_spell].target(self)

    def use_spell(self, ind_spell: int, object: Cell):
        """
        Функция вызывается, когда пользователь активирует способность.
        Производит эффект способности
        """
        self.spell_list[ind_spell].cast(self, object)

class Pawn(Piece):

    def __init__(self, cell, hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):
        super().__init__(cell, hp, accuracy, damage, radius_move, radius_fov)
        self.create_spell_list()

    def create_spell_list(self):
        
        """
        Функция создаёт объекты класса Spell, прописывая для них специфичные функции выбора цели и эффекта
        """

        def first_spell_target(self) -> list:
            x, y = self.cell.x, self.cell.y

            #Пешка атакует на одну клетку вокруг себя
            potential = [
                (x - 1, y - 1)
                (x - 1, y)
                (x - 1, y + 1)
                (x + 1, y - 1),
                (x + 1, y + 1),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
                         ]
            target_list = []
            
            #Среди этих клеток можно атаковать только те, на которых стоят фигуры (система свой-чужой не работает хе)
            for cell in potential:
                if not self.cell.get_type_cell_to_pos(cell[1], cell[0]) is None and type(self.cell.get_object_in_cell(cell[1], cell[0])) == Piece:
                    target_list.append(self.cell.get_cell_to_pos())

            return target_list
        
        def first_spell_cast(self, other):
            #Если фигура попала, она наносит урон равный своим хп
            if random.random() < self.accuracy:
                other.hp -= self.damage

        #Создаём способность Атака и добавляем её в список способностей
        Atacke = Spell(1, "Атака", "Атакуйте выбранную цель", first_spell_target, first_spell_cast)
        self.spell_list.append(Atacke)

if __name__ == '__main__':
    
    b = Pawn(Cell(), 10, 0.5, 2, 3, 1)
    a = Pawn(Cell(), 10, 0.5, 2, 3, 1)

    for i in range(10):
        a.spell_list[0].cast(a, b)
        print(b.hp)