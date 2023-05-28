import typing as tp
from random import random
from effect import *

if tp.TYPE_CHECKING:
    from piece import Piece
    from field import Square

class Spell:
    
    """
    Этот класс хранит информацию о способности фигуры
    """

    def __init__(self, id: str, name: str, description: str, cooldown: int, cost: int):

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

        def zone(spell, self: "Piece", host_cell: "Square" = None):
            pass

        def target(spell, self: "Piece"):
            pass
        
        def cast(spell, self: "Piece", other: "Square"):
            pass

class Piece_Move(Spell):

    def __init__(self):
        super().__init__('move', "Перемещение", "Переместитесь на клетку в зоне движения", 0, 1)

    def target(spell, self: "Piece") -> list[tuple["Square", "Square"]]:
        
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
    
    def cast(spell, self: "Piece", new_cell: "Square") -> None:

        """
        Функция переставляет фигуру на новую клетку.
        Возвращает пару - клетку с которой ушла и клетку на которую пришла фигура.
        """

        old_cell = self.cell
        self.cell = new_cell
        old_cell.del_inner_piece()
        new_cell.add_inner_piece(self)

class PawnAttack1(Spell):
  
    def __init__(self):
        super().__init__("attack", "Атака", "Атакуйте выбранную цель", 1, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

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

    def target(spell, self: "Piece"):
        
        potential = spell.zone(self)

        target_list = []
            
        #cреди этих клеток можно атаковать только те, на которых стоят фигуры (система свой-чужой не работает хе)
        for cell in potential:
            piece = self.field.get_square_by_pos(cell[0], cell[1]).inner_piece
            if self.field.is_into_map(cell[0], cell[1]) and not piece is None and piece.team != self.team:
                 target_list.append(self.field.get_square_by_pos(cell[0], cell[1]))

        return target_list
        
    def cast(spell, self: "Piece", other: "Square"):
        
        #забираем фигуру из клетки
        other = other.inner_piece

        #Если фигура попала, она наносит урон равный своим хп
        if random() < self.accuracy:
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