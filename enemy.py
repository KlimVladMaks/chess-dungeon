from field import *
from piece import Piece
from piece import _Field
from piece import _Square
from piece import Spell
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
        way = self.field.get_way(self.cell, end)

        #зацикливаем путь, когда дошли до конца идём назад
        way = way[:-1] + way[:0:-1]

        return way

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

    def get_enemies_in_range(self, spell: Spell, host_cell: _Square = None) -> list[Piece]:

        """
        Возвращает клетки с противниками в зоне действия способности
        :spell: заклинание для которого определяются враги в зоне
        :host_cell: исходная клетка, по умолчанию - собственная клетка фигуры
        :return: лист потенциальных целей (может быть пуст)
        """

        if host_cell is None:
            host_cell = self.cell

        #получаем обзор от данной клетки
        range = spell.target()
        enemies_in_range = []

        #просматриваем все клетки в области атаки на наличие фигур игрока
        for cell in range:
            if isinstance(cell.inner_piece, Piece) and not isinstance(cell.inner_piece, EnemyPiece):
                enemies_in_range.append(cell.inner_piece)

        return enemies_in_range

    def choice_enemy(self, enemies: list[Piece]) -> tp.Union[Piece, None]:

        """
        Функция выбирает предпочитаемого противника исходя из системы приоритетов, учитывающей несколько параметров
        На данном этапе выбор делается рандомно
        """

        if not enemies:
            return None

        return random.choice(enemies)

    def patrul_step(self) -> None:

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

    def get_nearest_enemy(self) -> tp.Union[Piece, None]:

        """
        Функция использует тот же алгоритм, что и функции field.get_way() и piece.get_movies()
        Изменено условие прерывание обхода и возврат функции
        """

        #храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        i = 0
        moves = []

        # и создаём переменную для ближайшей фигуры
        nearest_enemy = None

        #проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = self.cell.get_pos()
        if self.field.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))

        while i < len(moves):

            #проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if (not (moves[i][0] + 1, moves[i][1]) in moves #ещё не посетили
                    and self.field.is_into_map(moves[i][0] + 1, moves[i][1]) #в пределах поля
                        and not self.field.is_barrier(moves[i][0] + 1, moves[i][1])): #можно пройти
                #если нет фигуры, то обрабатываем как в обычном обходе
                this_cell = self.field.get_square_by_pos(moves[i][0] + 1, moves[i][1])
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0] + 1, moves[i][1]))
                #если видим фигуру игрока, то отмечаем как ближающую
                elif isinstance(this_cell.inner_piece, Piece) and not isinstance(this_cell.inner_piece, EnemyPiece):
                    nearest_enemy = this_cell.inner_piece
                    break

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                        and self.field.is_into_map(moves[i][0] - 1, moves[i][1])
                            and not self.field.is_barrier(moves[i][0] - 1, moves[i][1])):
                this_cell = self.field.get_square_by_pos(moves[i][0] - 1, moves[i][1])
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0] - 1, moves[i][1]))
                elif isinstance(this_cell.inner_piece, Piece) and not isinstance(this_cell.inner_piece, EnemyPiece):
                    nearest_enemy = this_cell.inner_piece
                    break
            
            if (not (moves[i][0], moves[i][1] + 1) in moves
                        and self.field.is_into_map(moves[i][0], moves[i][1] + 1)
                            and not self.field.is_barrier(moves[i][0], moves[i][1] + 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] + 1)
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] + 1))
                elif isinstance(this_cell.inner_piece, Piece) and not isinstance(this_cell.inner_piece, EnemyPiece):
                    nearest_enemy = this_cell.inner_piece
                    break

            if (not (moves[i][0], moves[i][1] - 1) in moves
                        and self.field.is_into_map(moves[i][0], moves[i][1] - 1)
                            and not self.field.is_barrier(moves[i][0], moves[i][1] - 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] - 1)
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] - 1))
                elif isinstance(this_cell.inner_piece, Piece) and not isinstance(this_cell.inner_piece, EnemyPiece):
                    nearest_enemy = this_cell.inner_piece
                    break

            #переходим к следующему элементу
            i += 1

        return nearest_enemy
    
    def get_desirable_position(self, spell: Spell, target: _Square) -> tp.Union[_Square, None]:

        """
        Вернёт ближайшую клетку на которую надо перейти для возможности активировать способность
        """

        potential_positions = self.get_potential_positions(spell, target)

        if not potential_positions:
            return None

        #опять обход в ширину со своими условиями

        #храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        i = 0
        moves = []

        # и создаём переменную для ближайшей клетки
        desirable_position = None

        #проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = self.cell.get_pos()
        if self.field.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))

        while i < len(moves):

            #проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if (not (moves[i][0] + 1, moves[i][1]) in moves #ещё не посетили
                    and self.field.is_into_map(moves[i][0] + 1, moves[i][1]) #в пределах поля
                        and not self.field.is_barrier(moves[i][0] + 1, moves[i][1])): #можно пройти
                #если нет фигуры, то обрабатываем как в обычном обходе
                this_cell = self.field.get_square_by_pos(moves[i][0] + 1, moves[i][1])
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0] + 1, moves[i][1]))
                #если клетка из потенциальной позиции - то это нужная клетка
                elif this_cell in potential_positions:
                    desirable_position = this_cell
                    break

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                        and self.field.is_into_map(moves[i][0] - 1, moves[i][1])
                            and not self.field.is_barrier(moves[i][0] - 1, moves[i][1])):
                this_cell = self.field.get_square_by_pos(moves[i][0] - 1, moves[i][1])
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0] - 1, moves[i][1]))
                elif this_cell in potential_positions:
                    desirable_position= this_cell
                    break
            
            if (not (moves[i][0], moves[i][1] + 1) in moves
                        and self.field.is_into_map(moves[i][0], moves[i][1] + 1)
                            and not self.field.is_barrier(moves[i][0], moves[i][1] + 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] + 1)
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] + 1))
                elif this_cell in potential_positions:
                    desirable_position = this_cell
                    break

            if (not (moves[i][0], moves[i][1] - 1) in moves
                        and self.field.is_into_map(moves[i][0], moves[i][1] - 1)
                            and not self.field.is_barrier(moves[i][0], moves[i][1] - 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] - 1)
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] - 1))
                elif this_cell in potential_positions:
                    desirable_position = this_cell
                    break

        return desirable_position

    def get_potential_positions(self, spell: Spell, target: _Square) -> list[_Square]:

        """
        Возвращает клетки из которых можно атаковать цель способностью
        :spell: Способность
        :target: Цель
        """
        
        potential = spell.zone(host_cell = target)
        potential_positions = []

        for cell in potential:
            if self.field.is_into_map(cell[0], cell[1]):
                potential_positions.append(self.field.get_square_by_pos(cell[0], cell[1]))

        return potential_positions

    def go_to_position(self, pos: _Square) -> None:

        """
        Функция передвинет фигуру на нужную клетку или ближайщую возможную к ней
        """

        way = self.field.get_way(self.cell, pos)

        if len(way) <= self.radius_move + 1:
            self.moving(pos)
        else:
            self.moving(way[self.radius_move])

    def alarm(self):

        """
        Поведение при обнаружении фигур игрока
        Реализовано только для одной способности
        """

        #опеределяется по очереди в приоритете способностей
        enemies_in_range = self.get_enemies_in_range(self.spell_list[1])
        if enemies_in_range:
            target = self.choice_enemy(enemies_in_range)
            if not target is None:
                self.cast_spell('atack', target)

        #если ни одна из способностей не может быть использована
        else:
            #определяет потенциальную цель
            target = self.get_nearest_enemy()
            if not target is None:
                #далее блок для каждой способности
                desirable_position = self.get_desirable_position(self.spell_list[1], target.cell)
                if not desirable_position is None:
                    self.go_to_position(desirable_position) # передвигает фигуру на позицию или максимально близко к ней

    def new_turn(self) -> None:

        """
        Функция дополняет действия фигуры при начале нового хода
        """

        if self.action == 'patrul':
            self.patrul_step()

        elif self.action == 'atack':
            self.alarm()


        super().new_turn()