"""
fix me
get_potential_positions должна быть изменена вместе с spell.zone
"""

from piece import *
from time import sleep
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


    def is_see_player_piece(self, cell: "Square") -> bool:

        """
        Функция проверяет видна ли с данной позиции фигура игрока
        """

        print('Враг осматривает клетку на наличие фигуры игрока')

        # получаем обзор от данной клетки
        fov = self.get_fovs(cell=cell)

        # проходим по всем видимым клеткам и узнаём нет ли фигур другой команды
        for c in fov:
            if isinstance(c.inner_piece, Piece) and c.inner_piece.team != self.team:
                print('Враг увидел игрока!')
                return True

        return False
    
    def choice_square(self, squares: list[Piece], spell: Spell) -> tp.Union[Piece, None]:

        """
        Функция выбирает предпочитаемую клетку для использования способности
        На данном этапе выбор делается рандомно
        """

        print(f'Враг определяет, на кого он может использовать {spell.name}')

        if not squares:
            return None

        return random.choice(squares)

    def get_nearest_enemy(self) -> tp.Union["Square", None]:

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
                elif isinstance(this_cell.inner_piece, Piece) and this_cell.inner_piece.team != self.team:
                    nearest_enemy = this_cell
                    break

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                    and self.field.is_into_map(moves[i][0] - 1, moves[i][1])
                    and not self.field.is_barrier(moves[i][0] - 1, moves[i][1])):
                this_cell = self.field.get_square_by_pos(moves[i][0] - 1, moves[i][1])
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0] - 1, moves[i][1]))
                elif isinstance(this_cell.inner_piece, Piece) and this_cell.inner_piece.team != self.team:
                    nearest_enemy = this_cell
                    break

            if (not (moves[i][0], moves[i][1] + 1) in moves
                    and self.field.is_into_map(moves[i][0], moves[i][1] + 1)
                    and not self.field.is_barrier(moves[i][0], moves[i][1] + 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] + 1)
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] + 1))
                elif isinstance(this_cell.inner_piece, Piece) and this_cell.inner_piece.team != self.team:
                    nearest_enemy = this_cell
                    break

            if (not (moves[i][0], moves[i][1] - 1) in moves
                    and self.field.is_into_map(moves[i][0], moves[i][1] - 1)
                    and not self.field.is_barrier(moves[i][0], moves[i][1] - 1)):
                this_cell = self.field.get_square_by_pos(moves[i][0], moves[i][1] - 1)
                if this_cell.inner_piece is None:
                    moves.append((moves[i][0], moves[i][1] - 1))
                elif isinstance(this_cell.inner_piece, Piece) and this_cell.inner_piece.team != self.team:
                    nearest_enemy = this_cell
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

        print(f'Враг думает, куда идти для использования способности {spell.name}')

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

        way = self.field.get_way(self.cell, pos, piece_is_barrier=True)

        if len(way) <= self.radius_move + 1:
            self.cast_spell(self.spell_list[0], pos)
        else:
            self.cast_spell(self.spell_list[0], way[self.radius_move])

    def try_cast_spell(self, spell: Spell) -> bool:

        """
        Функция пытается использовать способность и
        :return: В случае успеха - True, провала - False
        """

        square_for_cast = spell.target(self)

        if square_for_cast:
            print(f'Враг обнаружил цель в зоне способности {spell.name}')
            target = self.choice_square(square_for_cast, spell)
            if not target is None:
                self.cast_spell(spell, target)
                return True
            else:
                #не делаем ничего
                print(f'Вражеская фигура неопределилась с выбором цели и пропустила ход')
                self.AP = 0
        
        return False


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
                print('!')
                #И откатываем позицию
                pos -= 1
                if pos < 0:
                    pos = len(self.way_patrol) - 1
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
        Определяется отдельно для каждой фигуры
        """

        pass

    def new_turn(self) -> None:

        """
        Функция дополняет действия фигуры при начале нового хода
        """

        print()
        print('Новый ход', f"ХП фигуры = {self.hp} | положение = {self.field.get_pos_by_square(self.cell)}, пешка {self}")

        super().new_turn()

        while self.AP > 0:

            if self.action == 'patrol':
                print('Поведение:', self.action)
                self.patrol_step()

            elif self.action == 'attack':
                print('Поведение:', self.action)
                self.alarm()

            #Пока нет анимации
            sleep(0.2)
            self.field.update()


class EnemyPawn(EnemyPiece, Pawn):

    def __init__(self, team: str, field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)

    def alarm(self):

        """
        Поведение при обнаружении фигур игрока пешкой
        self.spell_list[0] - PieceMove()
        self.spell_list[1] - PawnAttack1()
        self.spell_list[2] - PawnAttack2_Attack() / PawnAttack2_Move()
        self.spell_list[3] - PawnUtility()
        """

        #Переменная для отследивания было ли совершено действие
        is_cast = False

        #Пытаемся использовать ульту!
        spell = self.spell_list[3]

        if spell.cooldown_now == 0 and self.hp <= 3:   
            is_cast = self.try_cast_spell(spell)

        #Завершаем действие, если способность использована
        if is_cast:
            return


        #Если способность не использовали, то пробуем обычную атаку
        spell = self.spell_list[1]

        if spell.cooldown_now == 0:   
            is_cast = self.try_cast_spell(spell)

        #Завершаем действие, если способность использована
        if is_cast:
            return


        #Если мы всё ещё в функции, то пробуем атаку с рывка
        spell = self.spell_list[2]
        if spell.cooldown_now == 0:   
            is_cast = self.try_cast_spell(spell)
        
        #После рывка атакуем
        if is_cast:
            spell = self.spell_list[2]
            is_cast = self.try_cast_spell(spell)
            if is_cast:
                return

        #если ни одна из способностей не может быть использована

        #то пробуем подойти для использования рывка

        #Идём к ближнему противнику
        target = self.get_nearest_enemy()
        print('Враг определил ближайшую цель')

        #Коль он найден, то
        if not target is None:
            
            if (self.spell_list[2].cooldown_now == 1 and self.AP <= 1) or (self.spell_list[2].cooldown_now == 0):
                #Пытаемся идти для рывка
                #Для обработки рывков немного инверсируем
                #Сначала ищем клетку из которой можно атаковать
                spell = PawnAttack2_Move()
                desirable_position = self.get_desirable_position(spell, target)
                if not desirable_position is None:
                    #Потом откуда к ней можно перейти
                    spell = PawnAttack2_Attack()
                    desirable_position = self.get_desirable_position(spell, desirable_position)

                if not desirable_position is None:
                    print('Враг движется к цели')
                    #передвигает фигуру на позицию или максимально близко к ней
                    self.go_to_position(desirable_position)
                    return
            
                else:
                    #не делаем ничего
                    print(f"Враг не может найти позицию для использования {spell.name}")
                    self.AP = 0
                    pass
            
            #Теперь ищем позицию для Атаки (или ульты, так как у них одинаковые зоны)
            spell = self.spell_list[1]
            if spell.cooldown_now <= 1:
                desirable_position = self.get_desirable_position(spell, target)

                if not desirable_position is None:
                    print('Враг движется к цели')
                    #передвигает фигуру на позицию или максимально близко к ней
                    self.go_to_position(desirable_position)
                    return
            
                else:
                    #не делаем ничего
                    print(f"Враг не может найти позицию для использования {spell.name}")
                    self.AP = 0
                    pass


        else:
            #не делаем ничего
            print(f"Ближайщей цели нет, враг бездействует")
            self.AP = 0
            pass

class EnemyKing(King):
    def __init__(self, team: str, field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)