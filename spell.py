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

    def target(spell, self: "Piece") -> list["Square"]:

        """
        Фильтрует клетки из Zone оставляя только те, которые могут быть целевыми
        """
        
        pass
        
    def cast(spell, self: "Piece", other: "Square") -> tp.Union["Spell", None]:

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
        other = other.inner_piece

        #Если фигура попала, она наносит урон равный своим хп
        if random() < self.accuracy:
            damage = randrange(self.min_damage, self.max_damage + 1)
            print(f"Атакующая фигура попала и нанесла {damage} урона!")
            other.hp -= damage
            print(f"Оставшиеся хп жертвы: {other.hp}/{other.max_hp}")

            if [effect.id for effect in other.effect_list].count('speed_reduction') == 0:
                print('Также на фигуру наложен дебафф!')
                effect = Speed_reduction(2, 1)
                other.effect_list.append(effect)
                effect.get_effect(other)

            #Если фигуры хп падают до 0 и ниже, удаляем её с поля
            if other.hp <= 0:
                print("Сильный удар разбивает жертву в каменную крошку!")
                other.cell.del_inner_piece()
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
            if not cell is None and not self.field.get_way(self.cell, cell) is None:
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
        other = other.inner_piece

        #Фигура попала и она наносит урон*1.5
        damage = randrange(self.min_damage, self.max_damage + 1)
        damage *= 2
        print(f"Атакующая фигура попала и нанесла {damage} урона!")
        other.hp -= damage
        self.hp -= damage // 2
        print(f"Оставшиеся хп жертвы: {other.hp}/{other.max_hp}")
        print(f"Оставшиеся хп свои: {self.hp}/{self.max_hp}")

        #Если фигуры хп падают до 0 и ниже, удаляем её с поля
        if other.hp <= 0:
            print("Сильный удар разбивает жертву в каменную крошку!")
            other.cell.del_inner_piece()

        if self.hp <= 0:
            print("Эта жертва не будет напрасной...")
            self.cell.del_inner_piece()