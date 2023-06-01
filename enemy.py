from piece import *
import random

import typing as tp
if tp.TYPE_CHECKING:
    from field import Field, Square


class EnemyPiece(Piece):

    def __init__(self, team: str, field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)
        self.action = "patrol"
        self.way_patrol = []
        self.pos_patrol = 0

    def set_way_patrol(self, end: "Square") -> None:

        """
        Функция определяет путь патрулирования от текущей точки до конечной
        :end: конечная точка маршрута, после которой следует поворот до начальной
        """

        print('Установка маршрута патрулирования...')

        # получаем кратчайший маршрут до целевой клетки
        way = self.field.get_way(self.cell, end)

        # зацикливаем путь, когда дошли до конца идём назад
        way = way[:-1] + way[:0:-1]

        self.way_patrol = way

        for c in way:
            print(c.get_pos(), end=' ')
        print()

    def is_see_player_piece(self, cell: "Square") -> bool:

        """
        Функция проверяет видна ли с данной позиции фигура игрока
        """

        print('Враг осматривает клетку на наличие фигуры игрока')

        # получаем обзор от данной клетки
        fov = self.get_fovs(cell=cell)

        # проходим по всем видимым клеткам и узнаём есть ли там фигура игрока
        for c in fov:
            if isinstance(c.inner_piece, Piece) and not isinstance(c.inner_piece, EnemyPiece):
                print('Враг увидел игрока!')
                return True

        return False

    def get_enemies_in_range(self, spell: Spell, host_cell: "Square" = None) -> list[Piece]:

        """
        Возвращает клетки с противниками в зоне действия способности
        :spell: заклинание для которого определяются враги в зоне
        :host_cell: исходная клетка, по умолчанию - собственная клетка фигуры
        :return: лист потенциальных целей (может быть пуст)
        """

        print('Враг определяет, может ли он кого атаковать')

        if host_cell is None:
            host_cell = self.cell

        # получаем обзор от данной клетки
        range = spell.target(self)
        enemies_in_range = []

        # просматриваем все клетки в области атаки на наличие фигур игрока
        for cell in range:
            if isinstance(cell.inner_piece, Piece) and not isinstance(cell.inner_piece, EnemyPiece):
                enemies_in_range.append(cell.inner_piece)

        return enemies_in_range

    def choice_enemy(self, enemies: list[Piece]) -> tp.Union[Piece, None]:

        """
        Функция выбирает предпочитаемого противника исходя из системы приоритетов, учитывающей несколько параметров
        На данном этапе выбор делается рандомно
        """

        print('Враг определяет, кого он может атаковать')

        if not enemies:
            return None

        return random.choice(enemies)

    def get_nearest_enemy(self) -> tp.Union[Piece, None]:

        """
        Функция использует тот же алгоритм, что и функции field.get_way() и piece.get_movies()
        Изменено условие прерывание обхода и возврат функции
        """

        print('Враг определяет ближайщую цель')

        # храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        i = 0
        moves = []

        # и создаём переменную для ближайшей фигуры
        nearest_enemy = None

        # проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = self.cell.get_pos()
        if self.field.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))

        while i < len(moves):

            # проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if (not (moves[i][0] + 1, moves[i][1]) in moves  # ещё не посетили
                    and self.field.is_into_map(moves[i][0] + 1, moves[i][1])  # в пределах поля
                    and not self.field.is_barrier(moves[i][0] + 1, moves[i][1])):  # можно пройти
                # если нет фигуры, то обрабатываем как в обычном обходе
                this_cell = self.field.get_square_by_pos(moves[i][0] + 1, moves[i][1])
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0] + 1, moves[i][1]))
                # если видим фигуру игрока, то отмечаем как ближающую
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

            # переходим к следующему элементу
            i += 1

        return nearest_enemy

    def get_desirable_position(self, spell: Spell, target: "Square") -> tp.Union["Square", None]:

        """
        Вернёт ближайшую клетку на которую надо перейти для возможности активировать способность
        """

        potential_positions = self.get_potential_positions(spell, target)

        if not potential_positions:
            return None

        print('Враг думает, куда идти для атаки')
        print('Потенциальные позиции:')
        for c in potential_positions:
            print(c.get_pos(), end=' ')
        print()

        # опять обход в ширину со своими условиями

        # храним индекс рассматриваемого элемента, симмулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        i = 0
        moves = []

        # и создаём переменную для ближайшей клетки
        desirable_position = None

        # проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = self.cell.get_pos()
        if self.field.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))

        while i < len(moves):

            # проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if (not (moves[i][0] + 1, moves[i][1]) in moves  # ещё не посетили
                    and self.field.is_into_map(moves[i][0] + 1, moves[i][1])  # в пределах поля
                    and not self.field.is_barrier(moves[i][0] + 1, moves[i][1])):  # можно пройти
                # если нет фигуры, то обрабатываем как в обычном обходе
                this_cell = self.field.get_square_by_pos(moves[i][0] + 1, moves[i][1])
                # если клетка из потенциальной позиции - то это нужная клетка
                if this_cell in potential_positions:
                    desirable_position = this_cell
                    break
                elif this_cell.inner_piece is None:
                    moves.append((moves[i][0] + 1, moves[i][1]))

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                    and self.field.is_into_map(moves[i][0] - 1, moves[i][1])
                    and not self.field.is_barrier(moves[i][0] - 1, moves[i][1])):
                this_cell = self.field.get_square_by_pos(moves[i][0] - 1, moves[i][1])
                if this_cell in potential_positions:
                    desirable_position = this_cell
                    break
                elif this_cell.inner_piece is None:
                    moves.append((moves[i][0] - 1, moves[i][1]))

            if (not (moves[i][0], moves[i][1] + 1) in moves
                    and self.field.is_into_map(moves[i][0], moves[i][1] + 1)
                    and not self.field.is_barrier(moves[i][0], moves[i][1] + 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] + 1)
                if this_cell in potential_positions:
                    desirable_position = this_cell
                    break
                elif this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] + 1))

            if (not (moves[i][0], moves[i][1] - 1) in moves
                    and self.field.is_into_map(moves[i][0], moves[i][1] - 1)
                    and not self.field.is_barrier(moves[i][0], moves[i][1] - 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] - 1)
                if this_cell in potential_positions:
                    desirable_position = this_cell
                    break
                elif this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] - 1))

            # переходим к следующему элементу
            i += 1

        return desirable_position

    def get_potential_positions(self, spell: Spell, target: "Square") -> list["Square"]:

        """
        Возвращает клетки из которых можно атаковать цель способностью
        :spell: Способность
        :target: Цель
        """

        potential = spell.zone(self, host_cell=target)
        print(potential)
        potential_positions = []

        for cell in potential:
            x, y = cell[0], cell[1]
            if self.field.is_into_map(y, x):
                square = self.field.get_square_by_pos(y, x)
                if square.inner_piece is None and not self.field.is_barrier(y, x):
                    potential_positions.append(self.field.get_square_by_pos(y, x))

        return potential_positions

    def go_to_position(self, pos: "Square") -> None:

        """
        Функция передвинет фигуру на нужную клетку или ближайщую возможную к ней
        Или не сдвинет вовсе
        """

        way = self.field.get_way(self.cell, pos)

        if len(way) <= self.radius_move + 1:
            self.cast_spell(self.spell_list[0], pos)
        else:
            self.cast_spell(self.spell_list[0], way[self.radius_move])

    def patrol_step(self) -> None:

        """
        Функция сдвигает фигуру по маршруту патрулирования и сменяет поведение фигуры, при обнаружении врага
        """

        # проверяем не видно ли на маршруте фигуру игрока
        for i in range(self.radius_move + 1):

            #проверяем не загородил ли кто дорогу

            # идём по маршруту
            pos = (i + self.pos_patrol) % len(self.way_patrol)

            #Если дорога загорожена, то ждём (если мы не на исходной клекте)
            if not self.way_patrol[pos].inner_piece is None and i != 0:
                self.AP = 0
                break

            print(f'Враг передвинулся на {self.way_patrol[pos].get_pos()}')

            # если увидили фигуру игрока, то сменяем поведение и переходим на ту клетку, на которой увидели
            if self.is_see_player_piece(self.way_patrol[pos]):
                self.action = "attack"
                break
        
        # сменяем метку
        self.pos_patrol = pos

        # фактически сдвигаем фигуру, если не хотим остаться на этой же клетке
        if self.way_patrol[self.pos_patrol] != self.cell:
            self.cast_spell(self.spell_list[0], self.way_patrol[self.pos_patrol])

    def alarm(self):

        """
        Поведение при обнаружении фигур игрока
        Реализовано только для одной способности
        """

        # опеределяется по очереди в приоритете способностей
        enemies_in_range = self.get_enemies_in_range(self.spell_list[1])
        if enemies_in_range:
            print('Враг обнаружил цель в зоне атаки')
            target = self.choice_enemy(enemies_in_range)
            if not target is None:
                self.cast_spell(self.spell_list[1], target.cell)
            else:
                #не делаем ничего
                self.AP = 0
                pass

        # если ни одна из способностей не может быть использована
        else:
            # определяет потенциальную цель
            target = self.get_nearest_enemy()
            print('Враг определил ближайшую цель')
            if not target is None:
                # далее блок для каждой способности
                desirable_position = self.get_desirable_position(self.spell_list[1], target.cell)
                if not desirable_position is None:
                    print('Враг движется к цели')
                    self.go_to_position(desirable_position)  # передвигает фигуру на позицию или максимально близко к ней
                else:
                    #не делаем ничего
                    self.AP = 0
                    pass
            else:
                #не делаем ничего
                self.AP = 0
                pass

    def new_turn(self) -> None:

        """
        Функция дополняет действия фигуры при начале нового хода
        """

        print('Новый ход')

        super().new_turn()

        while self.AP > 0:

            if self.action == 'patrol':
                print('Новый ход', self.action)
                self.patrol_step()

            elif self.action == 'attack':
                print('Новый ход', self.action)
                self.alarm()


class EnemyPawn(EnemyPiece, Pawn):

    def __init__(self, team: str, field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)