from piece import Piece
from field import *
from piece import _Field
from piece import _Square
import random

class EnemyPiece(Piece):
    
    def __init__(self, field: _Field, cell: _Square, max_hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):
        super().__init__(field, cell, max_hp, accuracy, damage, radius_move, radius_fov)
        self.action = "patrol"
        self.way_patrol = []
        self.pos_patrol = 0

    def set_way_patrol(self, end: _Square) -> list[_Square]:

        """
        Функция определяет путь патрулирования от текущей точки до конечной
        :end: конечная точка маршрута, после которой следует поворот до начальной
        """

        #получаем кратчайший маршрут до целевой клетки
        way = self.get_way(self.cell, end)

        #зацикливаем путь, когда дошли до конца идём назад
        way = way[:-1] + way[:0:-1]

        return way
    
    def patrul_step(self):

        """
        Функция сдвигает фигуру по маршруту патрулирования и сменяет поведение фигуры, при обнаружении врага
        """

        #проверяем не видно ли на маршруте фигуру игрока
        for i in range(self.radius_move):

            #идём по маршруту
            pos = (i + self.pos_patrol) % len(self.way_patrol)

            #сменяем метку
            self.pos_patrol = pos

            #если увидили фигуру игрока, то сменяем поведение и переходим на ту клетку, на которой увидели
            if self.is_see_player_piece(pos):
                self.action = "atack"
                break

        #фактически сдвигаем фигуру
        self.cast_spell("moving", self.way_patrol[self.pos_patrol])

    def get_way(self, start: _Square, end: _Square) -> list[_Square]:

        """
        Функция возвращает кратчайший маршрут между двумя клетками
        """

        #храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        # и ещё один массив, чтобы узнавать длину и при этом спокойно узнавать, были ли мы уже в этой клетке
        # и массив с сылкой на обратную клетку пришли для восстановления пути
        i = 0
        moves = []
        len_way = []
        preview_cell = []

        #проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = start.get_pos()
        end_row_pos, end_col_pos = end.get_pos()
        if self.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))
            len_way.append(0)
            preview_cell.append(-1)

        #переменная чтобы убедиться, что мы вообще можем дойти
        way_is_find = True

        while i < len(moves):

            #проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if moves[i] == (end_row_pos, end_col_pos):
                way_is_find = True
                break

            if (not (moves[i][0] + 1, moves[i][1]) in moves #ещё не посетили
                        and self.is_into_map(moves[i][0] + 1, moves[i][1]) #в пределах поля
                            and not self.is_barrier(moves[i][0] + 1, moves[i][1]) #можно пройти
                                and self.field.get_square_by_pos(moves[i][0] + 1, moves[i][1]).inner_piece is None): #нет фигуры
                moves.append((moves[i][0] + 1, moves[i][1]))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                        and self.is_into_map(moves[i][0] - 1, moves[i][1])
                            and not self.is_barrier(moves[i][0] - 1, moves[i][1])
                                and self.field.get_square_by_pos(moves[i][0] - 1, moves[i][1]).inner_piece is None):
                moves.append((moves[i][0] - 1, moves[i][1]))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)
            
            if (not (moves[i][0], moves[i][1] + 1) in moves
                        and self.is_into_map(moves[i][0], moves[i][1] + 1)
                            and not self.is_barrier(moves[i][0], moves[i][1] + 1)
                                and self.field.get_square_by_pos(moves[i][0], moves[i][1] + 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] + 1))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)

            if (not (moves[i][0], moves[i][1] - 1) in moves
                        and self.is_into_map(moves[i][0], moves[i][1] - 1)
                            and not self.is_barrier(moves[i][0], moves[i][1] - 1)
                                and self.field.get_square_by_pos(moves[i][0], moves[i][1] - 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] - 1))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)

            #переходим к следующему элементу
            i += 1

        way = [self.field.get_square_by_pos(moves[i][0], moves[i][1])]

        while i != -1:
            i = preview_cell[i]
            way.append(self.field.get_square_by_pos(moves[i][0], moves[i][1]))

        return way[::-1]

    def is_see_player_piece(self, cell: _Square) -> bool:

        """
        Функция проверяет видна ли с данной позиции фигура игрока
        """

        #получаем обзор от данной клетки
        fov = self.get_fovs(cell = cell)

        #проходим по всем видимым клеткам и узнаём есть ли там фигура игрока
        for c in fov:
            if isinstance(c.inner_piece, Piece) and not isinstance(c.inner_piece, EnemyPiece):
                return True
            
        return False

    def alarm(self):

        """
        Поведение при обнаружении фигур игрока
        """

        enemies_in_range = self.enemies_in_range()
        if self.get_enemies_in_range():
            target = self.choice_enemy(enemies_in_range)
            self.cast_spell('atack', target)

        else:
            target = self.get_nearest_enemy()
            self.get_desirable_position() #внутри self.get_potential_positions()
            self.go_to_position() # передвигает фигуру на позицию или максимально близко к ней


        pass

    def new_turn(self) -> None:

        """
        Функция дополняет действия при новом ходе
        """

        if self.action == 'patrul':
            self.patrul_step()

        elif self.action == 'atack':
            self.alarm()


        super().new_turn()