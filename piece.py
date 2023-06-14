import typing as tp
from spell import *

if tp.TYPE_CHECKING:
    from field import Square, Field
    from game import Game


class Piece:

    """
    Класс для шаблона Фигуры.
    """

    def __init__(self, team: str, game: "Game", field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):

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
        :min_damage: минимальный базовый урон атаки
        :max_damage: базовый урон атаки
        :spell_list: лист со скилами
        :active_turn: bool параметр хранящий может ли походить клетка в этот ход
        """

        self.team = team
        self.cell = cell
        self.game = game
        self.field = field
        self.radius_fov = radius_fov
        self.radius_move = radius_move
        self.max_hp = max_hp
        self.hp = max_hp
        self.accuracy = accuracy
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.spell_list = [Piece_Move()]
        self.effect_list = []
        self.active_turn = True
        self.AP = 2
        self.shield = 0

    def get_fovs(self, cell = None, opaque_piece = False) -> list["Square"]:
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
            fovs.update(self.get_view_for_line(opaque_piece, (start_x, start_y), (start_x + x, start_y + y)))

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
            fovs.update(self.get_view_for_line(opaque_piece, (start_x, start_y), (start_x + x, start_y + y)))

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

        foving_cell = [self.cell]
        for pos in list(fovs):
            cell = self.field.get_square_by_pos(pos[0], pos[1])
            if cell != self.cell:
                foving_cell.append(cell)

        return foving_cell
        

    def get_view_for_line(self, opaque_piece: bool, start: tuple[int], end: tuple[int])  -> list[tuple[int, int]]:
        """
        Функция вычисляет через какие точки проходит линия обзора от одной клетки до другой.
        И возвращает путь до первой стены.
        Приём - (x, y)
        Возврат идёт как (y, x)
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
            #если клетка - стена то клетки после неё не попадают в видимые клетки
            if self.field.is_fog(y, x):
                return way
            way = [(y, x)]

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
                if self.field.is_fog(y, x):
                    return way
                #если мы в режиме непрозрачных фигур
                if opaque_piece:
                    if not self.field.get_square_by_pos(y, x).inner_piece is None:
                        return way
                way.append((y, x))
            
        return way
    
    def create_spell_list(self) -> None:
        
        """
        Функция добавляет объекты класса Spell в piece.spell_list
        """
        
    def give_damage(self, damage: int) -> None:

        """
        Фигура получает урон
        """

        print(f"Входящий урон {damage}.")

        if self.shield >= damage:
            self.shield -= damage
            print(f"Весь урон ушёл в щит! Оставщаяся прочность щита {self.shield}.")

        else:
            if self.shield > 0:
                print(f"Щит поглатил {self.shield} урона и разрушился.")
                damage -= self.shield
                self.shield = 0

            print(f"Фигура получила {damage} урона.")
            self.hp -= damage
            if self.hp > 0:
                print(f"Осталось хп: {self.hp}/{self.max_hp}")

            else:
                self.destroy()

    def give_effect(self, effect: "Effect")  -> None:

        """
        Фигура получает эффект
        """

        if [effect.id for effect in self.effect_list].count(effect.id) == 0:
            self.effect_list.append(effect)
            effect.get_effect(self)
            print(f"Также на фигуру наложен дебафф! {effect.name} на {effect.strength}")

        else:
            i = [old_effect.id for old_effect in self.effect_list].index(effect.id)

            #Берём больший таймер из уже существующего и накладываемого эффекта
            if effect.timer > self.effect_list[i].timer:
                self.effect_list[i].timer = effect.timer
                print(f"{effect.name} продлено до {effect.timer}")

            #Берём большую силу из уже существующего и накладываемого эффекта
            if effect.strength > self.effect_list[i].strength:
                self.effect_list[i].strength = effect.strength
                print(f"{effect.name} усилено до {effect.strength}")


    def destroy(self):
        self.cell.del_inner_piece()
        self.game.del_piece(self)
        print("Фигура рассыпалась в каменную крошку!")

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
                effect.remove_effect(self)
                self.effect_list.remove(effect)

        self.active_turn = True

    def prepare_spell(self, spell: "Spell") -> list["Square"]:
        
        """
        Функция вызывается, когда пользователь нажимает на способность.
        Возвращает клетки, на которые можно использовать способность.
        :id_spell: кодовое слово способности
        """

        return spell.target(self)

    def cast_spell(self, spell: "Spell", cell: "Square") -> None:

        """
        Функция вызывается, когда пользователь активирует способность.
        Производит эффект способности
        :id_spell: кодовое слово способности
        :cell: клетка на которую способность использовали
        """
        if spell.cast_type == "attack":
            cell.attack_flash(self.cell, cell)
        elif spell.cast_type == "area_attack":
            cell.attack_flash(self.cell, spell.give_enemies_in_area(self, cell))

        spell.cast(self, cell)
        spell.cooldown_now = spell.cooldown
        self.AP -= spell.cost
        if self.AP < 0:
            self.AP = 0
        if self.AP == 0 and not 0 in [spell.cost for spell in self.spell_list]:
            self.active_turn = False

class Pawn(Piece):

    """
    Класс пешки
    """

    def __init__(self, team: str, game: "Game", field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        #инициируем фигуру
        super().__init__(team, game, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)
        #собираем спелы специальной функцией
        self.create_spell_list()

    def create_spell_list(self) -> None:
        
        """
        Функция добавляет объекты класса Spell в piece.spell_list
        """

        #Добавляем способности из модуля spell
        self.spell_list.append(PawnAttack1())
        self.spell_list.append(PawnAttack2_Move())
        self.spell_list.append(PawnUtility())

    def new_turn(self) -> None:

        print(type(self.spell_list[2]).__name__, "!!!")
        if type(self.spell_list[2]).__name__ == "PawnAttack2_Attack":
            self.spell_list[2] = PawnAttack2_Move()
            self.spell_list[2].cooldown_now = self.spell_list[2].cooldown

        super().new_turn()

class Bishop(Piece):

    """
    Класс слона
    """

    def __init__(self, team: str, game: "Game", field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, game, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)
        self.create_spell_list()

    def create_spell_list(self) -> None:
        
        """
        Функция добавляет объекты класса Spell в piece.spell_list
        """

        #Добавляем способности из модуля spell
        self.spell_list.append(BishopAttack1())
        self.spell_list.append(BishopAttack2())
        self.spell_list.append(BishopUtility())

class Knight(Piece):

    def __init__(self, team: str, game: "Game", field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, game, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)
        self.create_spell_list()

    def create_spell_list(self) -> None:
        
        """
        Функция добавляет объекты класса Spell в piece.spell_list
        """

        #Добавляем способности из модуля spell
        self.spell_list.append(KnightAttack1_Move())
        self.spell_list.append(KnightAttack2())
        self.spell_list.append(KnightUtility())

    def new_turn(self) -> None:

        if type(self.spell_list[1]).__name__ == "KnightAttack1_Attack":
            self.spell_list[1] = KnightAttack1_Move()
            self.spell_list[1].cooldown_now = self.spell_list[1].cooldown

        super().new_turn()

class Rook(Piece):

    def __init__(self, team: str, game: "Game", field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, game, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)
        self.create_spell_list()

    def create_spell_list(self) -> None:
        
        """
        Функция добавляет объекты класса Spell в piece.spell_list
        """

        #Добавляем способности из модуля spell
        self.spell_list.append(RookAttack1())
        self.spell_list.append(RookAttack2())
        self.spell_list.append(RookUtility())

class Queen(Piece):

    def __init__(self, team: str, game: "Game", field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, game, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)
        self.create_spell_list()

    def create_spell_list(self) -> None:
        
        """
        Функция добавляет объекты класса Spell в piece.spell_list
        """

        #Добавляем способности из модуля spell
        self.spell_list.append(QueenAttack1())
        self.spell_list.append(QueenAttack2())

    def new_turn(self) -> None:

        super().new_turn()

        self.cast_spell(QueenUtility(), self.cell)


class King(Piece):

    def __init__(self, team: str, game: "Game", field: "Field", cell: "Square", max_hp: int, accuracy: float, min_damage: int, max_damage: int, radius_move: int, radius_fov: int):
        super().__init__(team, game, field, cell, max_hp, accuracy, min_damage, max_damage, radius_move, radius_fov)
        self.create_spell_list()

    def create_spell_list(self) -> None:
        
        """
        Функция добавляет объекты класса Spell в piece.spell_list
        """

        #Отнимаем движение
        self.spell_list = []
        self.spell_list.append(KingAttack1())
        self.spell_list.append(KingAttack2())

        #У короля пока пусто
