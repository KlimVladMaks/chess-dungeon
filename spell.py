import typing as tp
from random import random, randrange
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

    def zone(spell, self: "Piece", host_cell: "Square" = None) -> list[tuple[int, int]]:

        """
        Воспомогательная функция, возвращающая набор координат потенциальных клеток.
        Требуется отдельная фильтрация и перевод в объекты класса Square
        """

        pass

    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        """
        Фильтрует клетки из Zone оставляя только те, которые могут быть целевыми
        """
        
        pass
        
    def cast(spell, self: "Piece", other: "Square") -> None:

        """
        Производит действие способности и вернёт способность, которая должна заменить данную на интерфейсе
        """

        pass

    def draw_rhomb(self, r_start, r_end, x0, y0) -> list[tuple[int, int]]:
        """
        Одно из правил выделения зоны, что встречается часто
        """

        #Хранилище
        rhomb = []

        #Перебераем радиусы
        for r in range(r_start, r_end + 1):
            x = x0
            y = y0 + r

            #выполняем обход по "ромбу" сетки основа которого - крест с дальностью r
            for i in range(4 * r):
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

                rhomb.append((x, y))

        return rhomb

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
        super().__init__("attack", "Атака", "Обычная атака (ближний бой)", 1, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, 1, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell
        
        potential = spell.zone(self, host_cell = host_cell)

        target_list = []
            
        #cреди этих клеток можно атаковать только противников
        for cell_coor in potential:
            x, y = cell_coor[0], cell_coor[1]
            cell = self.field.get_square_by_pos(y, x)
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
        
    def cast(spell, self: "Piece", other: "Square"):
        
        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #Если фигура попала, она наносит урон
        if random() < self.accuracy:
            damage = randrange(self.min_damage, self.max_damage + 1)
            other_piece.give_damage(damage)
            
        else:
            print(f"Атакующая фигура промахнулась")

class PawnAttack2_Move(Spell):

    def __init__(self):
        super().__init__("lunge_move", "Выпад", "подойдите к противнику, чтобы потом атаковать (ближний бой)", 2, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):
        
        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, 1, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell
        
        potential = spell.zone(self, host_cell = host_cell)

        target_list = []
        
        #cреди этих клеток можно шагнуть только в соответсвие с правилом движения и оттуда можно атаковать
        for cell_coor in potential:
            x, y = cell_coor[0], cell_coor[1]
            cell = self.field.get_square_by_pos(y, x)
            if not cell is None and not self.field.get_way(self.cell, cell, piece_is_barrier=True) is None:
                if PawnAttack2_Attack().target(self, host_cell = cell):
                    target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square"):
        
        self.spell_list[0].cast(self, other)
        self.spell_list[self.spell_list.index(spell)] = PawnAttack2_Attack()

class PawnAttack2_Attack(Spell):

    def __init__(self):
        super().__init__("lunge_attack", "Выпад", "Атакуйте противника! (ближний бой)", 0, 0)

    def zone(spell, self: "Piece", host_cell: "Square" = None):
        #Дальность выпада
        lunge_range = 1 

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, lunge_range, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell
        
        potential = spell.zone(self, host_cell = host_cell)

        target_list = []
            
        #cреди этих клеток можно атаковать только противников
        for cell_coor in potential:
            x, y = cell_coor[0], cell_coor[1]
            cell = self.field.get_square_by_pos(y, x)
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square"):
        
        PawnAttack1().cast(self, other)
        self.spell_list[self.spell_list.index(spell)] = PawnAttack2_Move()


class PawnUtility(Spell):

    def __init__(self):
        super().__init__("just_pawn", "Всего лишь пешка", "Фигура делает сильную атаку и  наносит себе 50% от нанесенного урона (ближний бой)", 3, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, 1, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell
        
        potential = spell.zone(self, host_cell = host_cell)

        target_list = []
            
        #cреди этих клеток можно атаковать только противников
        for cell_coor in potential:
            x, y = cell_coor[0], cell_coor[1]
            cell = self.field.get_square_by_pos(y, x)
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square"):
        
        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #Фигура попала и она наносит урон*1.5
        if random() < self.accuracy + 1:
            damage = randrange(self.min_damage, self.max_damage + 1)
            damage *= 2
            print("Урон по врагу:")
            other_piece.give_damage(damage)
            print("Урон по себе:")
            self.give_damage(damage // 2)
            
        else:
            print(f"Атакующая фигура промахнулась")

class BishopAttack1(Spell):

    def __init__(self):
        super().__init__('shot', "Выстрел", "Обычная атака (дальний бой)", 1, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_shot = 6
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_shot, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем обзор
        radius_fov = self.radius_fov

        #определяем дальность атаки
        range_shot = 6
        self.radius_fov = range_shot

        #стреляем во всё, что видим
        potential = self.get_fovs()

        #восстановим обзор
        self.radius_fov = radius_fov

        #фильтруем
        target_list = []

        #cреди этих клеток можно атаковать только противников
        for cell in potential:
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square") -> None:
        
        #определяем дальность выстрела

        #для этого возмём координаты клетки с врагом
        coordinates_other = self.field.get_pos_by_square(other)
        coordinates_self = self.field.get_pos_by_square(self.cell)
        #и проложим линию обзора
        range_shot = len(self.get_view_for_line(False, coordinates_self[::-1], coordinates_other[::-1])) - 1

        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #снижаем меткость за дальность
        accuracy_coefficient = 0.4
        accuracy = self.accuracy * (1 / range_shot) ** (accuracy_coefficient)

        #Если фигура попала, она наносит урон
        if random() < accuracy:
            damage = randrange(self.min_damage, self.max_damage + 1)
            other_piece.give_damage(damage)
            
        else:
            print(f"Атакующая фигура промахнулась")

class BishopAttack2(Spell):

    def __init__(self):
        super().__init__('poisoned_arrow', "Отравленная стрела", "Атакует и снижает меткость противника (дальний бой)", 2, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_shot = 5
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_shot, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем обзор
        radius_fov = self.radius_fov

        #определяем дальность атаки
        range_shot = 5
        self.radius_fov = range_shot

        #стреляем во всё, что видим
        potential = self.get_fovs()

        #восстановим обзор
        self.radius_fov = radius_fov

        #фильтруем
        target_list = []

        #cреди этих клеток можно атаковать только противников
        for cell in potential:
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square") -> None:
        
        #определяем дальность выстрела

        #для этого возмём координаты клетки с врагом
        coordinates_other = self.field.get_pos_by_square(other)
        coordinates_self = self.field.get_pos_by_square(self.cell)
        #и проложим линию обзора
        range_shot = len(self.get_view_for_line(False, coordinates_self[::-1], coordinates_other[::-1])) - 1

        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #снижаем меткость за дальность
        accuracy_coefficient = 0.4
        accuracy = self.accuracy * (1 / range_shot) ** (accuracy_coefficient)
        print(f"Точность: {accuracy}")

        #Если фигура попала, она наносит урон
        if random() < accuracy:
            damage = randrange(self.min_damage, self.max_damage + 1)
            other_piece.give_damage(damage)
            other_piece.give_effect(Speed_reduction(2, 2))
            
        else:
            print(f"Атакующая фигура промахнулась")

class BishopUtility(Spell):

    def __init__(self):
        super().__init__("emergency_care", "Неотложная помощь", "Восстанавливает здоровье себе или союзнику", 3, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_shot = 4
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_shot, x0, y0)
        potential.append(x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем обзор
        radius_fov = self.radius_fov

        #определяем дальность атаки
        range_shot = 4
        self.radius_fov = range_shot

        #хилим, всё что видим
        potential = self.get_fovs()
        potential.append(self.cell)

        #восстановим обзор
        self.radius_fov = radius_fov

        #фильтруем
        target_list = []

        #хилим только союзиков
        for cell in potential:
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team == self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square") -> None:
        
        #забираем фигуру из клетки
        other = other.inner_piece

        hill = randrange(int(self.min_damage*1.5), int(self.max_damage*1.5) + 1)

        print(f"Лечение восстановило {hill} хп!")
        other.hp += hill
        if other.hp > other.max_hp:
            other.hp = other.max_hp
        print(f"Хп цели: {other.hp}/{other.max_hp}")

class KnightAttack1_Move(Spell):

    def __init__(self):
        super().__init__("swift_attack_move", "Стремительная атака", "Стремительно приближается для атаки чтобы потом атаковать противника", 1, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_move = 5
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_move, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем движение
        radius_move = self.radius_move

        #определяем дальность атаки
        range_move = 5
        self.radius_move = range_move

        #идём куда дойдём
        potential = self.spell_list[0].target(self)

        #восстановим движение
        self.radius_move = radius_move

        #фильтруем
        target_list = []

        #только клетки откуда можно использовать вторую часть способности
        for cell in potential:
            if not cell is None and not self.field.get_way(self.cell, cell, piece_is_barrier=True) is None:
                if KnightAttack1_Attack().target(self, host_cell = cell):
                    target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square") -> None:
        
        self.spell_list[0].cast(self, other)
        self.spell_list[self.spell_list.index(spell)] = KnightAttack1_Attack()

class KnightAttack1_Attack(Spell):

    def __init__(self):
        super().__init__("swift_attack_attack", "Стремительная атака", "Атакуйте противника и снизьте ему меткость", 0, 0)

    def zone(spell, self: "Piece", host_cell: "Square" = None):
        #Дальность удара
        lunge_range = 1 

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, lunge_range, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell
        
        potential = spell.zone(self, host_cell = host_cell)

        target_list = []
            
        #cреди этих клеток можно атаковать только противников
        for cell_coor in potential:
            x, y = cell_coor[0], cell_coor[1]
            cell = self.field.get_square_by_pos(y, x)
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square"):

        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #Если фигура попала, она наносит урон
        if random() < self.accuracy:
            damage = randrange(self.min_damage, self.max_damage + 1)
            other_piece.give_damage(damage)
            other_piece.give_effect(Accuracy_reduction(2, 0.2))
            
        else:
            print(f"Атакующая фигура промахнулась")

        self.spell_list[self.spell_list.index(spell)] = KnightAttack1_Move()

class KnightAttack2(Spell):

    def __init__(self):
        super().__init__("tactical_retreat", "Тактическое отступление", "Делает дальнее перемещение и восстанавливает себе небольшое количество здоровья", 2, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_move = 5
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_move, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем движение
        radius_move = self.radius_move

        #определяем дальность атаки
        range_move = 8
        self.radius_move = range_move

        #идём куда дойдём
        potential = self.spell_list[0].target(self)

        #восстановим движение
        self.radius_move = radius_move

        #фильтруем
        target_list = []

        #ступать можно куда угодно
        for cell in potential:
            if not cell is None and not self.field.get_way(self.cell, cell, piece_is_barrier=True) is None:
                target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square") -> None:
        
        Piece_Move().cast(self, other)

        hill = randrange(int(self.min_damage*0.5), int(self.max_damage*0.5) + 1)

        print(f"Лечение восстановило {hill} хп!")
        self.hp += hill
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"Хп: {self.hp}/{self.max_hp}")

class KnightUtility(Spell):

    def __init__(self):
        super().__init__("sabotage", "Диверсия", "Стремительно приближается для атаки, наносит урон по области, если цель одна, то наносит повышенный урон", 3, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_move = 5
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_move, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем движение
        radius_move = self.radius_move

        #определяем дальность атаки
        range_move = 6
        self.radius_move = range_move

        #идём куда дойдём
        potential = self.spell_list[0].target(self)

        #восстановим движение
        self.radius_move = radius_move

        #фильтруем
        target_list = []

        #только клетки, рядом с коими есть враг
        for cell in potential:
            if not cell is None and not self.field.get_way(self.cell, cell, piece_is_barrier=True) is None:
                if spell.give_enemies_in_area(self, cell):
                    target_list.append(cell)

        return target_list

    def cast(spell, self: "Piece", other: "Square") -> None:
        
        Piece_Move().cast(self, other)

        enemies = spell.give_enemies_in_area(self, other)

        if len(enemies) == 1:
            damage = randrange(int(self.min_damage*1.5), int(self.max_damage*1.5) + 1)
        else:
            damage = randrange(self.min_damage, self.max_damage + 1)

        for enemy in enemies:

            #забираем фигуру из клетки
            enemy = enemy.inner_piece

            #Если фигура попала, она наносит урон
            if random() < self.accuracy + 1:
                damage = randrange(self.min_damage, self.max_damage + 1)
                enemy.give_damage(damage)

            else:
                print(f"Атакующая фигура промахнулась")

    def give_enemies_in_area(spell, self, host_cell):

        """
        Воспомогательная функция для target
        """

        area = 2
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, area, x0, y0)

        enemies_list = []
        for cell_coor in potential:
            x, y = cell_coor[0], cell_coor[1]
            cell = self.field.get_square_by_pos(y, x)
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                enemies_list.append(cell)

        return enemies_list
    

class RookAttack1(Spell):

    def __init__(self):
        super().__init__("tactical_offensive", "Тактическое наступление", "Стремительно приближается для атаки и прибавляет себе небольшое количество защиты (ближний бой)", 1, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_ram = 4
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_ram, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем обзор
        radius_fov = self.radius_fov

        #определяем дальность атаки
        range_ram = 4
        self.radius_fov = range_ram

        #таранем всё, что видим
        potential = self.get_fovs(opaque_piece = True)

        #восстановим обзор
        self.radius_fov = radius_fov

        #фильтруем
        target_list = []

        #cреди этих клеток можно атаковать только противников
        for cell in potential:
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list

    def cast(spell, self: "Piece", other: "Square") -> None:

        #определим клетку перед врагом

        #для этого возмём координаты клетки с врагом
        coordinates_other = self.field.get_pos_by_square(other)
        coordinates_self = self.field.get_pos_by_square(self.cell)
        #и проложим линию обзора
        pos_cell_for_move = self.get_view_for_line(False, coordinates_self[::-1], coordinates_other[::-1])[-2]

        #и вот наша клетка!
        cell_for_move = self.field.get_square_by_pos(pos_cell_for_move[0], pos_cell_for_move[1])
        
        #ставим туда фигуру
        Piece_Move().cast(self, cell_for_move)

        #даём себе щит
        shield = randrange(int(self.min_damage*0.5), int(self.max_damage*0.5) + 1)
        self.shield += shield
        print(f"Ладья получила {shield} щита! Теперь у неё {self.shield} щита.")

        #и атакуем

        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #Если фигура попала, она наносит урон
        if random() < self.accuracy:
            damage = randrange(self.min_damage, self.max_damage + 1)
            other_piece.give_damage(damage)
            
        else:
            print(f"Атакующая фигура промахнулась")

class RookAttack2(Spell):

    def __init__(self):
        super().__init__("shield_strike", "Удар щитом", "Наносит удар расходуя всю свою защиту нанося с её помощью урон (ближний бой)", 2, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, 1, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell
        
        potential = spell.zone(self, host_cell = host_cell)

        target_list = []
            
        #cреди этих клеток можно атаковать только противников
        for cell_coor in potential:
            x, y = cell_coor[0], cell_coor[1]
            cell = self.field.get_square_by_pos(y, x)
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
        
    def cast(spell, self: "Piece", other: "Square"):
        
        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #Если фигура попала, она наносит урон
        if random() < self.accuracy:
            damage = randrange(self.min_damage, self.max_damage + 1) + self.shield
            other_piece.give_damage(damage)
            
        else:
            print(f"Атакующая фигура промахнулась")

class RookUtility(Spell):

    def __init__(self):
        super().__init__("fortress", "Крепость", "Добавляет большое количество  защиты себе или союзнику", 3, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_shot = 6
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_shot, x0, y0)
        potential.append(x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем обзор
        radius_fov = self.radius_fov

        #определяем дальность атаки
        range_shot = 6
        self.radius_fov = range_shot

        #щитуем, всё что видим
        potential = self.get_fovs()
        potential.append(self.cell)

        #восстановим обзор
        self.radius_fov = radius_fov

        #фильтруем
        target_list = []

        #щитуем только союзиков
        for cell in potential:
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team == self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square") -> None:
        
        #забираем фигуру из клетки
        other = other.inner_piece

        shield = randrange(int(self.min_damage*1.5), int(self.max_damage*1.5) + 1)

        print(f"Цель получила щит прочностью {shield}")
        other.shield += shield
        print(f"Прочность щита цели: {other.shield}")

class QueenAttack1(Spell):
    
    def __init__(self):
        super().__init__('into_the_heart', "В самое сердце", "Наносит урон игнорируя защиту (дальний бой)", 1, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_shot = 6
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_shot, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем обзор
        radius_fov = self.radius_fov

        #определяем дальность атаки
        range_shot = 6
        self.radius_fov = range_shot

        #стреляем во всё, что видим
        potential = self.get_fovs()

        #восстановим обзор
        self.radius_fov = radius_fov

        #фильтруем
        target_list = []

        #cреди этих клеток можно атаковать только противников
        for cell in potential:
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list
    
    def cast(spell, self: "Piece", other: "Square") -> None:

        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #Если фигура попала, она наносит урон
        if random() < 1:
            damage = randrange(self.min_damage, self.max_damage + 1)
            other_shield = other_piece.shield
            other_piece.shield = 0
            other_piece.give_damage(damage)
            other_piece.shield = other_shield
            
        else:
            print(f"Атакующая фигура промахнулась")

class QueenAttack2(Spell):

    def __init__(self):
        super().__init__("bitchiness", "Стервозность", "Стремительно приближается для атаки и наносит дополнительный урон за пройденный путь до врага", 1, 2)

    def zone(spell, self: "Piece", host_cell: "Square" = None):

        #Берём исходныю клетку, если не сказано иначе
        if host_cell is None:
            host_cell = self.cell

        range_ram = 7
        y0, x0 = host_cell.get_pos()
        potential = spell.draw_rhomb(1, range_ram, x0, y0)

        return potential
    
    def target(spell, self: "Piece", host_cell: "Square" = None) -> list["Square"]:

        if host_cell is None:
            host_cell = self.cell
        
        #сохраняем обзор
        radius_fov = self.radius_fov

        #определяем дальность атаки
        range_ram = 7
        self.radius_fov = range_ram

        #таранем всё, что видим
        potential = self.get_fovs(opaque_piece = True)

        #восстановим обзор
        self.radius_fov = radius_fov

        #фильтруем
        target_list = []

        #cреди этих клеток можно атаковать только противников
        for cell in potential:
            if not cell is None and not cell.inner_piece is None and cell.inner_piece.team != self.team:
                 target_list.append(cell)

        return target_list

    def cast(spell, self: "Piece", other: "Square") -> None:

        #определим клетку перед врагом

        #для этого возмём координаты клетки с врагом
        coordinates_other = self.field.get_pos_by_square(other)
        coordinates_self = self.field.get_pos_by_square(self.cell)
        #и проложим линию обзора
        pos_cell_for_move = self.get_view_for_line(False, coordinates_self[::-1], coordinates_other[::-1])[-2]

        #и вот наша клетка!
        cell_for_move = self.field.get_square_by_pos(pos_cell_for_move[0], pos_cell_for_move[1])

        #Теперь определим дальность
        range_run = len(self.field.get_way(self.cell, cell_for_move)) - 1
        
        #ставим туда фигуру
        Piece_Move().cast(self, cell_for_move)

        #и атакуем

        #забираем фигуру из клетки
        other_piece = other.inner_piece

        #Если фигура попала, она наносит урон
        if random() < self.accuracy:
            print(f"Дальность пробежки составила {range_run}")
            damage = randrange(self.min_damage, self.max_damage + 1) + range_run
            other_piece.give_damage(damage)
            
        else:
            print(f"Атакующая фигура промахнулась")