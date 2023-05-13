from piece import Piece
from field import *
from piece import _Field
from piece import _Square

class EnemyPiece(Piece):
    
    def __init__(self, field: _Field, cell: _Square, max_hp: int, accuracy: float, damage: int, radius_move: int, radius_fov: int):
        super().__init__(field, cell, max_hp, accuracy, damage, radius_move, radius_fov)
        self.action = "patrol"
        self.way_patrol = self.set_way_patrol()
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

        #self.field.field_map

        pass

    def is_see_player_piece(self, pos: _Square) -> bool:

        """
        Функция проверяет видна ли с данной позиции фигура игрока
        """

        pass

    def alarm(self):

        """
        Поведение при обнаружении фигур игрока
        """

        pass

    def new_turn(self) -> None:

        """
        Функция дополняет действия при новом ходе
        """

        super().new_turn()
