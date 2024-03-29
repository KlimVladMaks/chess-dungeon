import pygame as pg
import typing as tp

if tp.TYPE_CHECKING:
    from piece import Piece
    from menu import Menu
    from king_square import KingSquare

# Размер стороны шахматной клетки
SQUARE_SIDE_SIZE = 50

# Цвет шахматной клетки
SQUARE_COLOR = "#FFFFFF"

# Цвет активной клетки
SQUARE_ACTIVATED_COLOR = "#008000"

# Ширина границы шахматной клетки
SQUARE_BORDER_WIDTH = 1

# Цвет границы шахматной клетки
SQUARE_BORDER_COLOR = "#000000"

# Стандартная скорость изменения размера шахматной клетки (в процентах)
CHANGE_SIZE_RATE = 0.05

# Цвет для несуществующей клетки
NONEXISTENT_SQUARE_COLOR = "#000000"

# Минимальный размер стороны шахматной клетки (в процентах от размера экрана)
MIN_SQUARE_SIDE_SIZE = 0.03

# Максимальный размер стороны шахматной клетки (в процентах от размера экрана)
MAX_SQUARE_SIDE_SIZE = 0.2

# Цвет для занятой клетки
SQUARE_OCCUPIED_COLOR = "#FFFF00"

# Цвет для занятой выбранной клетки
SQUARE_SELECTED_COLOR = "#8B00FF"

# Цвет вспышки клетки при её атаке
FLASH_ATTACKED_COLOR = (255, 0, 0, 128)

# Цвет вспышки клетки с которой атакуют
FLASH_ATTACK_COLOR = (0, 0, 255, 128)

# Время продолжительности вспышки клетки
FLASH_DELAY = 300

# Цвет для просматриваемой клетки
VIEWED_SQUARE_COLOR = (255, 165, 0, 128)

# Размер шрифта для размещения текста на шахматной клетке
SQUARE_FONT_SIZE = 30

# Цвет текста, размещаемого на шахматной клетке (очки здоровья)
SQUARE_FONT_COLOR_HP = (255, 165, 0)

# Цвет текста, размещаемого на шахматной клетке (очки щита)
SQUARE_FONT_COLOR_SHIELD = (0, 0, 255)

# Серый фильтр для наложения на неактивные фигуры
GRAY_FILTER = (0, 0, 0, 128)


class SquareTemplate(pg.sprite.Sprite):
    """
    Класс для реализации шаблона спрайта шахматной клетки.
    """

    def __init__(self, x: int, y: int, field: 'Field') -> None:
        """
        Инициализация шахматной клетки.

        :param x: Начальная координата x.
        :param y: Начальная координата y.
        :param field: Игровое поле.
        """

        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем игровое поле
        self.field = field

        # Сохраняем размер стороны клетки
        self.side_size = SQUARE_SIDE_SIZE

        # Задаём поверхность клетки
        self.image = pg.Surface((self.side_size, self.side_size))

        # Задаём область клетки, основываясь на переданных координатах
        self.rect = pg.Rect(x, y, self.side_size, self.side_size)

        # Указываем, что эта клетка не существует (т.к. это лишь шаблон)
        self.is_exist = False

        # Свойство для хранения фигуры, стоящей на клетке
        # (В данном классе всегда равно None, так как это просто шаблон)
        self.inner_piece = None

        # Флаг, указывающий на то, является ли фигура на клетке выбранной
        # (В данном классе всегда равно False, так как это просто шаблон)
        self.is_selected = False

        # Флаг, указывающий на то, является ли клетка просматриваемой
        self.is_viewed = False

        # Указываем, что клетка не активна
        self.is_activated = False

    def get_pos(self) -> tuple[int, int]:
        """
        Функция для получения позиции клетки в списке игровых клеток поля.

        :return: Позиция клетки в списке игровых клеток поля в формате (строка, столбец)
        """

        # Возвращаем позицию клетки в списке игровых клеток поля
        return self.field.get_pos_by_square(self)

    def move(self, x_shift: int, y_shift: int) -> None:
        """
        Функция для сдвига позиции шахматной клетки.

        :param x_shift: Сдвиг по x.
        :param y_shift: Сдвиг по y.
        """

        # Сдвигаем область клетки на заданные координатные сдвиги
        self.rect.move_ip(x_shift, y_shift)

    def increase_size(self) -> None:
        """
        Функция для увеличения размера шахматной клетки на стандартную величину.
        (Важно: данная функция влияет лишь на размеры клетки, а не на её позицию)
        """

        # Увеличиваем размер стороны на стандартную величину
        self.side_size += int(self.side_size * CHANGE_SIZE_RATE) + 1

        # Переформатируем клетку, учитывая увеличение её стороны
        self.image = pg.Surface((self.side_size, self.side_size))
        self.rect = pg.Rect(self.rect.x, self.rect.y, self.side_size, self.side_size)

    def decrease_size(self) -> None:
        """
        Функция для уменьшения размера шахматной клетки на стандартную величину.
        (Важно: данная функция влияет лишь на размеры клетки, а не на её позицию)
        """

        # Уменьшаем размер стороны на стандартную величину
        self.side_size -= int(self.side_size * CHANGE_SIZE_RATE) + 1

        # Переформатируем клетку, учитывая уменьшение её стороны
        self.image = pg.Surface((self.side_size, self.side_size))
        self.rect = pg.Rect(self.rect.x, self.rect.y, self.side_size, self.side_size)

    def add_inner_piece(self, piece: 'Piece') -> None:
        """
        Функция, не используемая для данного класса.
        Всегда возвращает None.
        """
        return None

    def get_inner_piece(self) -> tp.Union['Piece', None]:
        """
        Функция, не используемая для данного класса.
        Всегда возвращает None.
        """
        return None

    def del_inner_piece(self) -> None:
        """
        Функция, не используемая для данного класса.
        Всегда возвращает None.
        """
        return None

    def select(self) -> None:
        """
        Функция, не используемая для данного класса.
        Всегда возвращает None.
        """
        return None

    def deselect(self) -> None:
        """
        Функция, не используемая для данного класса.
        Всегда возвращает None.
        """
        return None

    def on_view(self) -> None:
        """
        Функция, не используемая для данного класса.
        Всегда возвращает None.
        """
        return None

    def off_view(self) -> None:
        """
        Функция, не используемая для данного класса.
        Всегда возвращает None.
        """
        return None


class Square(SquareTemplate):
    """
    Класс для реализации спрайта обычной шахматной клетки.
    """

    def __init__(self, x: int, y: int, field: 'Field') -> None:
        """
        Инициализация шахматной клетки.

        :param x: Координата x на экране.
        :param y: Координата y на экране.
        :param field: Игровое поле.
        """

        # Инициализируем шаблон клетки
        super().__init__(x, y, field)

        # Задаём клетке поверхность с изображением
        self.image = pg.image.load("design/field/square.png")

        # Флаг, показывающий активность/неактивность клетки
        self.is_activated = False

        # Указываем, что эта клетка существует
        self.is_exist = True

        # Свойство для хранения фигуры, стоящей на данной клетке
        # (содержит None, если на клетки не стоит фигура)
        self.inner_piece: tp.Union[Piece, None] = None

        # Флаг, показывающий занята или свободна клетка
        self.is_occupied = False

        # Флаг, указывающий на то, является ли фигура на клетке выбранной
        self.is_selected = False

        # Флаг, указывающий на то, является ли клетка просматриваемой
        self.is_viewed = False

        # Сохраняем шрифт для размещения надписей на клетке
        self.font = pg.font.Font(None, SQUARE_FONT_SIZE)

    def change_regime(self) -> None:
        """
        Функция для изменения режима шахматной клетки.
        Активная клетка становиться неактивной, а неактивная - активной.
        Активный режим отличается от неактивного другим цветом клетки.
        """

        # Если клетка активна, то меняем аё цвет на обычный и убираем флаг активации
        if self.is_activated:
            self.is_activated = False

        # Если клетка неактивна, то меняем её цвет на активный и ставим флаг активации
        else:
            self.is_activated = True

        # Обновляем клетку
        self.update()

    def change_color(self, new_square_color: str, new_border_color: str) -> None:
        """
        Функция для изменения цвета шахматной клетки и её границы.

        :param new_square_color: Новый цвет шахматной клетки.
        :param new_border_color: Новый цвет границы шахматной клетки.
        """

        # Обновляем цвет клетки и её границы
        self.image.fill(new_square_color)
        pg.draw.rect(self.image,
                     new_border_color,
                     pg.Rect(0, 0, self.side_size, self.side_size),
                     SQUARE_BORDER_WIDTH)

        # Если клетка занята, рисуем дополнительный круг
        if self.is_occupied:
            pg.draw.circle(self.image,
                           SQUARE_OCCUPIED_COLOR,
                           (self.side_size // 2,
                            self.side_size // 2),
                           self.side_size // 2)

    def update(self):
        """
        Функция для обновления шахматной клетки.
        """

        # Загружаем базовый вариант клетки
        self.image = pg.image.load("design/field/square.png")

        # Если клетка не занята фигурой
        if not self.is_occupied:

            # Если клетка активирована, то добавляем значок активации
            if self.is_activated:
                surface = pg.image.load("design/field/activated_square.png")
                self.image.blit(surface, (0, 0))

        # Если клетка занята фигурой
        elif self.is_occupied:

            # Отлавливаем ошибки на случай отсутствия подходящего изображения
            try:
                # Рисуем на клетке соответсвующую фигуру в зависимости от названия класса
                surface = pg.image.load(f"design/pieces/{type(self.inner_piece).__name__}.png")
                self.image.blit(surface, (0, 0))
            except:
                pass

            # Если клетка не имеет доступных ходов и это не вражеская клетка, преобразуем её в чёрно-белые тона
            if (not self.inner_piece.active_turn) and self.inner_piece.controller != "comp":
                surface = pg.Surface(self.image.get_size(), pg.SRCALPHA)
                surface.fill(GRAY_FILTER)
                self.image.blit(surface, (0, 0))

            # Если клетка выбрана, то добавляем значок выбранной фигуры
            if self.is_selected:
                surface = pg.image.load("design/game/select.png")
                self.image.blit(surface, (0, 0))

            # Если клетка активирована, добавляем значок воздействия на фигуру
            if self.is_activated:
                surface = pg.image.load("design/game/white_attack.png")
                self.image.blit(surface, (0, 0))

            # Рисуем на клетке с фигурой значение количества HP у данной фигуры
            hp_text = self.font.render(str(self.inner_piece.hp), True, SQUARE_FONT_COLOR_HP)
            self.image.blit(hp_text, (0, 0))

            # Если у фигуры есть щит, то рисуем его значение
            if self.inner_piece.shield > 0:
                shield_text = self.font.render(str(self.inner_piece.shield), True, SQUARE_FONT_COLOR_SHIELD)
                self.image.blit(shield_text, 
                                (0, 
                                self.image.get_height() - shield_text.get_height()))
            
            # Если на фигуру наложены эффекты, то добавляем специальный значок
            if len(self.inner_piece.effect_list) > 0:
                surface = pg.image.load("design/game/debuff.png")
                self.image.blit(surface, (0, 0))

        # Если клетка просматривается, то дополнительно выделяем клетку
        if self.is_viewed:
            view = pg.Surface((SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE), pg.SRCALPHA)
            view.fill(VIEWED_SQUARE_COLOR)
            self.image.blit(view, (0, 0))

    def increase_size(self) -> None:
        """
        Функция для увеличения размера шахматной клетки на стандартную величину.
        (Важно: данная функция влияет лишь на размеры клетки, а не на её позицию)
        """

        # Вызываем родительскую функцию увеличения клетки
        super().increase_size()

        # Перерисовываем клетку с учётом увеличения её стороны
        self.image.fill(SQUARE_COLOR)
        pg.draw.rect(self.image,
                     SQUARE_BORDER_COLOR,
                     pg.Rect(0, 0, self.side_size, self.side_size),
                     SQUARE_BORDER_WIDTH)

        # Если клетка активирована, то возвращаем ей активный цвет
        if self.is_activated:
            self.change_color(SQUARE_ACTIVATED_COLOR, SQUARE_BORDER_COLOR)

    def decrease_size(self) -> None:
        """
        Функция для уменьшения размера шахматной клетки на стандартную величину.
        (Важно: данная функция влияет лишь на размеры клетки, а не на её позицию)
        """

        # Вызываем родительскую функцию уменьшения клетки
        super().decrease_size()

        # Перерисовываем клетку с учётом уменьшения её стороны
        self.image.fill(SQUARE_COLOR)
        pg.draw.rect(self.image,
                     SQUARE_BORDER_COLOR,
                     pg.Rect(0, 0, self.side_size, self.side_size),
                     SQUARE_BORDER_WIDTH)

        # Если клетка активирована, то возвращаем ей активный цвет
        if self.is_activated:
            self.change_color(SQUARE_ACTIVATED_COLOR, SQUARE_BORDER_COLOR)

    def add_inner_piece(self, piece: 'Piece') -> None:
        """
        Функция для добавления фигуры на клетку.
        (Если на клетке уже стоит фигура, то старая фигура будет удалена).

        :param piece: Шахматная фигура.
        """

        # Размещаем фигуру на клетке
        self.inner_piece = piece

        # Вызываем функцию для переведения клетки в занятый режим
        self.occupy()

    def get_inner_piece(self) -> tp.Union['Piece', None]:
        """
        Функция для получения фигуры, стоящей на клетке.

        :return: Фигура, стоящая на клетке или None, если на клетке не стоит фигура.
        """

        # Возвращаем фигуру, стоящую на клетке
        return self.inner_piece

    def del_inner_piece(self) -> None:
        """
        Функция для удаления фигуры, стоящей на клетке.
        """

        # Удаляем фигуру, стоящую на клетке
        self.inner_piece = None

        # Вызываем функцию для переведения клетки в незанятый режим
        self.deoccupy()

    def occupy(self) -> None:
        """
        Функция, переводящая клетку в занятый режим.
        """

        # Ставим флаг, что клетка занята
        self.is_occupied = True

        # Обновляем клетку
        self.update()

    def deoccupy(self) -> None:
        """
        Функция, переводящая клетку в незанятый режим.
        """

        # Ставим флаг, что клетка не занята
        self.is_occupied = False

        # Обновляем клетку
        self.update()

    def select(self) -> None:
        """
        Функция для выделения выбранной клетки.
        """

        # Ставим флаг, что клетка выбрана
        self.is_selected = True

        # Обновляем клетку
        self.update()

    def deselect(self) -> None:
        """
        Функция для отмены выделения выбранной клетки.
        """

        # Ставим флаг, что клетка не выбрана
        self.is_selected = False

        # Обновляем клетку
        self.update()

    def flash(self, color="red") -> None:
        """
        Функция для закрашивания клетки в цвет вспышки.

        :param color: Цвет вспышки (red, blue).
        """

        # Закрашиваем клетку в цвет вспышки в зависимости от требуемого цвета
        flash = pg.Surface((SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE), pg.SRCALPHA)

        if color == "red":
            flash.fill(FLASH_ATTACKED_COLOR)
        elif color == "blue":
            flash.fill(FLASH_ATTACK_COLOR)
        else:
            flash.fill(FLASH_ATTACKED_COLOR)

        self.image.blit(flash, (0, 0))
        self.field.update()

    def on_view(self) -> None:
        """
        Функция для переведения клетки в режим обзора.
        """
        self.is_viewed = True
        self.update()

    def off_view(self) -> None:
        """
        Функция для выключения у клетки режима обзора.
        """
        self.is_viewed = False
        self.update()

    @staticmethod
    def attack_flash(attack_square: tp.Union['Square', list['Square']],
                     attacked_square: tp.Union['Square', list['Square']]) -> None:
        """
        Функция для реализации необходимых вспышек для обозначения атаке.

        :param attack_square: Клетка, с которой атакуют.
        :param attacked_square: Клетка, которую атакуют.
        """

        # Закрашиваем атакующие клетки
        if isinstance(attack_square, Square):
            attack_square.flash("blue")
        elif isinstance(attack_square, list):
            for square in attack_square:
                square.flash("blue")

        # Закрашиваем атакуемые клетки
        if isinstance(attacked_square, Square):
            attacked_square.flash("red")
        elif isinstance(attacked_square, list):
            for square in attacked_square:
                square.flash("red")

        # Совершаем небольшую задержку
        pg.time.delay(FLASH_DELAY)

        # Возвращаем атакующим клеткам обычный цвет
        if isinstance(attack_square, Square):
            attack_square.update()
        elif isinstance(attack_square, list):
            for square in attack_square:
                square.update()

        # Возвращаем атакуемым клеткам обычный цвет
        if isinstance(attacked_square, Square):
            attacked_square.update()
        elif isinstance(attacked_square, list):
            for square in attacked_square:
                square.update()

        # Обновляем игровое поле
        if isinstance(attacked_square, Square):
            attacked_square.field.update()
        elif isinstance(attacked_square, list):
            attacked_square[0].field.update()


class NonexistentSquare(SquareTemplate):
    """
    Класс для реализации несуществующей шахматной клетки.
    """

    def __init__(self, x: int, y: int, field: 'Field') -> None:
        """
        Инициализируем несуществующую шахматную клетку.

        :param x: Координата x на экране.
        :param y: Координата y на экране.
        :param field: Игровое поле.
        """

        # Инициализируем шаблон клетки
        super().__init__(x, y, field)

        # Задаём клетке поверхность с изображением
        self.image = pg.image.load("design/field/barrier.png")

        # Указываем, что клетка не существует
        self.is_exist = False


class Field:
    """
    Класс для реализации игрового поля.
    """

    def __init__(self,
                 screen: pg.Surface,
                 screen_field: pg.Surface,
                 background: pg.Surface,
                 screen_absolute_coordinates: list[int],
                 field_map: list[list[int]],
                 game_menu: 'Menu') -> None:
        """
        Функция для инициализации игрового поля.

        :param screen: Экран игры.
        :param screen_field: Экран игрового поля.
        :param background: Фон игры.
        :param screen_absolute_coordinates: Абсолютные координаты экрана игры.
        :param field_map: Карта игрового поля.
        :param game_menu: Игровое меню.
        :param king_square: Клетка (кнопка) короля игрока.
        """

        # Сохраняем экран игры
        self.screen = screen

        # Сохраняем экран игрового поля
        self.screen_field = screen_field

        # Сохраняем фон игры
        self.background = background

        # Сохраняем абсолютные координаты экрана игры
        self.screen_absolute_coordinates = screen_absolute_coordinates

        # Сохраняем карту игрового поля
        self.field_map = field_map

        # Сохраняем игровое меню
        self.game_menu = game_menu

        # Свойство для кнопки короля игрока
        self.king_square: tp.Union[KingSquare, None] = None

        # Двухмерный список для хранения спрайтов шахматных клеток
        self.squares_list: list[list[SquareTemplate]] = []

        # Группа для хранения спрайтов шахматных клеток
        self.squares_group = pg.sprite.Group()

        # Флаг движения игрового поля
        self.is_moving = False

        # Флаг первого сдвига при движении игрового поля
        self.skip_first_move = False

        # Извлекаем координаты начала экрана
        x = self.screen_absolute_coordinates[0]
        y = self.screen_absolute_coordinates[1]

        # Создаём шахматные клетки, задаём им стартовые координаты и помещаем в спрайт-группу.
        # Заполняем двухмерный список с шахматными клетками
        for row in self.field_map:
            inner_list = []
            for col in row:
                if col == 1:
                    square = Square(x, y, self)
                    self.squares_group.add(square)
                    inner_list.append(square)
                else:
                    nonexistent_square = NonexistentSquare(x, y, self)
                    self.squares_group.add(nonexistent_square)
                    inner_list.append(nonexistent_square)
                x += SQUARE_SIDE_SIZE
            y += SQUARE_SIDE_SIZE
            x = 0
            self.squares_list.append(inner_list)

    def get_square_side_size(self) -> int:
        """
        Функция, возвращающая размер стороны клетки игрового поля.

        :return: Текущий размер клетки игрового поля.
        """

        # Возвращаем размер стороны первой клетки в списке с игровыми клетками
        # (т.к. все клетки имеют одинаковый размер)
        return self.squares_list[0][0].rect.width

    def get_field_width(self) -> int:
        """
        Функция, возвращающая ширину игрового поля.

        :return: Ширина игрового поля.
        """

        # Рассчитываем и возвращаем ширину игрового поля
        return len(self.squares_list[0]) * self.get_square_side_size()

    def get_field_height(self) -> int:
        """
        Функция, возвращающая высоту игрового поля.

        :return: Высота игрового поля.
        """

        # Рассчитываем и возвращаем высоту игрового поля
        return len(self.squares_list) * self.get_square_side_size()

    def get_square_by_coordinates(self, x_coordinate: int, y_coordinate: int) -> tp.Union[SquareTemplate, None]:
        """
        Функция для получения шахматной клетки по её относительным координатам.

        :param x_coordinate: Относительная координата x клетки.
        :param y_coordinate: Относительная координата y клетки.
        :return: Клетка с заданными координатами или None, если клетка не найдена.
        """

        # Если координаты клетки совпадают с координатами клетки короля игрока, то возвращаем её
        if self.king_square.rect.collidepoint(x_coordinate, y_coordinate):
            return self.king_square

        # Рассчитываем абсолютные координаты клетки
        x_absolute = x_coordinate + self.screen_absolute_coordinates[0]
        y_absolute = y_coordinate + self.screen_absolute_coordinates[1]

        # Получаем размер стороны клетки
        square_side_size = self.get_square_side_size()

        # Если абсолютные x или y меньше 0, то возвращаем None
        if x_absolute < 0 or y_absolute < 0:
            return None

        # Отлавливаем ошибки для избежания выхода из диапазона
        try:

            # Рассчитываем позицию клетки и извлекаем её из двухмерного списка
            square_col = x_absolute // square_side_size
            square_row = y_absolute // square_side_size
            found_square = self.squares_list[square_row][square_col]

        # При выходе из диапазона возвращаем None
        except IndexError:
            return None

        # Возвращаем найденную клетку
        return found_square

    def get_square_by_pos(self, row_pos: int, col_pos: int) -> tp.Union[SquareTemplate, None]:
        """
        Функция, возвращающая клетку по её позиции в списке игровых клеток.

        :param row_pos: Строка клетки.
        :param col_pos: Столбец клетки.
        :return: Клетка с заданной позицией или None, если заданная позиция выходит за пределы диапазона.
        """

        # Отлавливаем ошибки для избежания выхода за пределы диапазона
        try:

            # Возвращаем клетку с заданной позицией
            return self.squares_list[row_pos][col_pos]

        # При выходе за пределы диапазона возвращаем None
        except IndexError:
            return None

    def get_pos_by_square(self, square: SquareTemplate) -> tuple[int, int]:
        """
        Функция, возвращающая позицию переданной клетки в списке игровых клеток.

        :param square: Клетка игрового поля.
        :return: Позиция клетки в списке игровых клеток.
        """

        # Находим и возвращаем позицию клетки в списке игровых клеток
        for i in range(len(self.squares_list)):
            for j in range(len(self.squares_list[i])):
                if self.squares_list[i][j] == square:
                    return i, j

    def update(self):
        """
        Функция для обновления (перерисовки) игрового поля.
        """

        # Перерисовываем игровое поле
        self.screen_field.blit(self.background, (0, 0))
        self.squares_group.draw(self.screen_field)
        self.screen.blit(self.screen_field, (0, 0))

        # Отрисовываем кнопку открытия игрового меню
        self.screen_field.blit(self.game_menu.open_menu_button.image, self.game_menu.open_menu_button.rect)
        self.screen.blit(self.screen_field, (0, 0))

        # Отрисовываем кнопку короля, если она добавлена
        if self.king_square is not None:
            self.king_square.update()
            self.screen_field.blit(self.king_square.image, self.king_square.rect)
            self.screen.blit(self.screen_field, (0, 0))

        # Обновляем экран
        pg.display.update()

    def move(self, x_shift: int, y_shift: int) -> None:
        """
        Функция для сдвига игрового поля.
        (Функция не даёт игровому полю выйти за пределы экрана более чем наполовину).

        :param x_shift: Сдвиг по x.
        :param y_shift: Сдвиг по y.
        """

        # Рассчитываем потенциальные новые абсолютные координаты экрана
        x_screen_test = self.screen_absolute_coordinates[0] - x_shift
        y_screen_test = self.screen_absolute_coordinates[1] - y_shift

        # Рассчитываем размеры поля
        field_width = self.get_field_width()
        field_height = self.get_field_height()

        # Получаем размеры одной клетки
        square_side_size = SQUARE_SIDE_SIZE

        # Получаем размеры экрана
        screen_width = self.screen_field.get_width()
        screen_height = self.screen_field.get_height()

        # Если при сдвиге по X на экран не попадает ни одной целой клетки, то обнуляем сдвиг по X
        if (x_screen_test < -(screen_width - square_side_size)) or \
           (x_screen_test > (field_width - square_side_size)):
            x_shift = 0
        
        # Если при сдвиге по Y на экран не попадает ни одной целой клетки, то обнуляем сдвиг по Y
        if (y_screen_test < -(screen_height - square_side_size)) or \
           (y_screen_test > (field_height - square_side_size)):
            y_shift = 0

        # Сдвигаем каждую клетку игрового поля
        for square in self.squares_group:
            square.move(x_shift, y_shift)

        # Обновляем абсолютные координаты экрана
        self.screen_absolute_coordinates[0] -= x_shift
        self.screen_absolute_coordinates[1] -= y_shift

    def is_into_map(self, row_pos: int, col_pos: int) -> bool:
        """
        Функция, проверяющая, существует ли клетка с заданными координатами.

        :param row_pos Позиция строки.
        :param col_pos Позиция столбца.
        :return: Возвращает True, если клетка существует, иначе False.
        """

        # также убеждаемся, что мы не просим отрицательные индексы
        if row_pos < 0 or col_pos < 0:
            return False

        # запрашиваем у поля клетку по координатам
        cell = self.get_square_by_pos(row_pos, col_pos)

        if cell is None:
            return False

        return True

    def is_barrier(self, row_pos: int, col_pos: int) -> bool:
        """
        Функция, проверяющая, является ли заданная клетка непроницаемой для движения.
        (Не вызывайте функцию, если не уверены, что клетка существует).

        :param row_pos Позиция строки клетки.
        :param col_pos Позиция столбца клетки.
        :return: Возвращает True, если клетка непроницаема для движения, иначе False.
        """

        # запрашиваем у поля клетку по координатам
        cell = self.get_square_by_pos(row_pos, col_pos)

        # спрашиваем у клетки преграждает ли она проход
        # (Пока просто проверяем, существует ли клетка)
        if cell.is_exist:
            return False

        return True

    def is_fog(self, row_pos: int, col_pos: int) -> bool:
        """
        Функция, проверяющая, является ли заданная клетка непроницаемой для обзора.
        (Не вызывайте функцию, если не уверены, что клетка существует).

        :param row_pos Позиция строки клетки.
        :param col_pos Позиция столбца клетки.
        :return: Возвращает True, если клетка непроницаема для обзора, иначе False.
        """

        # запрашиваем у поля клетку по координатам
        cell = self.get_square_by_pos(row_pos, col_pos)

        # спрашиваем у клетки преграждает ли она обзор
        # (Пока просто проверяем, существует ли клетка)
        if cell.is_exist:
            return False

        return True

    def get_way(self, start: Square, end: Square, piece_is_barrier: bool = False) -> tp.Union[list[SquareTemplate], None]:
        """
        Функция, возвращающая кратчайший маршрут между двумя клетками.

        :param start: Начальная клетка.
        :param end: Конечная клетка.
        :return: Список клеток, составляющих кратчайший маршрут между начальной и конечной клетками.
        """

        # храним индекс рассматриваемого элемента, симулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        # и ещё один массив, чтобы узнавать длину и при этом спокойно узнавать, были ли мы уже в этой клетке
        # и массив со ссылкой на обратную клетку пришли для восстановления пути
        i = 0
        moves = []
        len_way = []
        preview_cell = []

        # проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = start.get_pos()
        end_row_pos, end_col_pos = end.get_pos()
        if self.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))
            len_way.append(0)
            preview_cell.append(-1)

        # переменная чтобы убедиться, что мы вообще можем дойти
        way_is_find = False

        while i < len(moves):

            # проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if moves[i] == (end_row_pos, end_col_pos):
                way_is_find = True
                break

            if (not (moves[i][0] + 1, moves[i][1]) in moves  # ещё не посетили
                    and self.is_into_map(moves[i][0] + 1, moves[i][1])  # в пределах поля
                    and not self.is_barrier(moves[i][0] + 1, moves[i][1])  # можно пройти
                    and (self.get_square_by_pos(moves[i][0] + 1, moves[i][1]).inner_piece is None or not piece_is_barrier)):  # нет фигуры (если фигура = стена)
                moves.append((moves[i][0] + 1, moves[i][1]))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                    and self.is_into_map(moves[i][0] - 1, moves[i][1])
                    and not self.is_barrier(moves[i][0] - 1, moves[i][1])
                    and (self.get_square_by_pos(moves[i][0] - 1, moves[i][1]).inner_piece is None or not piece_is_barrier)):
                moves.append((moves[i][0] - 1, moves[i][1]))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)

            if (not (moves[i][0], moves[i][1] + 1) in moves
                    and self.is_into_map(moves[i][0], moves[i][1] + 1)
                    and not self.is_barrier(moves[i][0], moves[i][1] + 1)
                    and (self.get_square_by_pos(moves[i][0], moves[i][1] + 1).inner_piece is None or not piece_is_barrier)):
                moves.append((moves[i][0], moves[i][1] + 1))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)

            if (not (moves[i][0], moves[i][1] - 1) in moves
                    and self.is_into_map(moves[i][0], moves[i][1] - 1)
                    and not self.is_barrier(moves[i][0], moves[i][1] - 1)
                    and (self.get_square_by_pos(moves[i][0], moves[i][1] - 1).inner_piece is None or not piece_is_barrier)):
                moves.append((moves[i][0], moves[i][1] - 1))
                len_way.append(len_way[i] + 1)
                preview_cell.append(i)

            # переходим к следующему элементу
            i += 1

        if way_is_find:
            way = [self.get_square_by_pos(moves[i][0], moves[i][1])]

            while preview_cell[i] != -1:
                i = preview_cell[i]
                way.append(self.get_square_by_pos(moves[i][0], moves[i][1]))

            return way[::-1]

        else:
            return None

    def get_nearest(self, start: "Square", endest: list["Square"]) -> tp.Union["Square", None]:

        """
        Функция возвращает 
        Функция считает фигуры преградой

        :param start: Начальная клетка.
        :param endest: список конечных клетка.
        :return: ближайщая клетка из списка к стартовой клетке
        """

        # храним индекс рассматриваемого элемента, симулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        # и ещё один массив, чтобы узнавать длину и при этом спокойно узнавать, были ли мы уже в этой клетке
        # и массив со ссылкой на обратную клетку пришли для восстановления пути
        i = 0
        moves = []
        len_way = []

        # проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = start.get_pos()
        if self.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))
            len_way.append(0)

        #конечная клетка
        nearest_cell = None

        while i < len(moves):

            # проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if self.get_square_by_pos(moves[i][0], moves[i][1]) in endest:
                nearest_cell = self.get_square_by_pos(moves[i][0], moves[i][1])
                break

            if (not (moves[i][0] + 1, moves[i][1]) in moves  # ещё не посетили
                    and self.is_into_map(moves[i][0] + 1, moves[i][1])  # в пределах поля
                        and not self.is_barrier(moves[i][0] + 1, moves[i][1])  # можно пройти
                            and self.get_square_by_pos(moves[i][0] + 1, moves[i][1]).inner_piece is None):  # нет фигуры (если фигура = стена)
                moves.append((moves[i][0] + 1, moves[i][1]))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                    and self.is_into_map(moves[i][0] - 1, moves[i][1])
                        and not self.is_barrier(moves[i][0] - 1, moves[i][1])
                            and self.get_square_by_pos(moves[i][0] - 1, moves[i][1]).inner_piece is None):
                moves.append((moves[i][0] - 1, moves[i][1]))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0], moves[i][1] + 1) in moves
                    and self.is_into_map(moves[i][0], moves[i][1] + 1)
                        and not self.is_barrier(moves[i][0], moves[i][1] + 1)
                            and self.get_square_by_pos(moves[i][0], moves[i][1] + 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] + 1))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0], moves[i][1] - 1) in moves
                    and self.is_into_map(moves[i][0], moves[i][1] - 1)
                        and not self.is_barrier(moves[i][0], moves[i][1] - 1)
                            and self.get_square_by_pos(moves[i][0], moves[i][1] - 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] - 1))
                len_way.append(len_way[i] + 1)

            i += 1

        return nearest_cell
    
    def get_farthest(self, start: "Square", endest: list["Square"]) -> tp.Union["Square", None]:

        """
        Функция возвращает 
        Функция считает фигуры преградой

        :param start: Начальная клетка.
        :param endest: список конечных клетка.
        :return: дальняя клетка из списка от стартовой клетке
        """

        # храним индекс рассматриваемого элемента, симулируя очередь
        # и саму очередь, в которой храним клетку от которой параллельно идём
        # и ещё один массив, чтобы узнавать длину и при этом спокойно узнавать, были ли мы уже в этой клетке
        # и массив со ссылкой на обратную клетку пришли для восстановления пути
        i = 0
        moves = []
        len_way = []

        # проверим о выходе за пределы массива (зачем?)
        row_pos, col_pos = start.get_pos()
        if self.is_into_map(row_pos, col_pos):
            moves.append((row_pos, col_pos))
            len_way.append(0)

        #конечная клетка
        farthest_cell = None

        while i < len(moves):

            # проверяем были ли мы уже в соседних клетках от текущей
            # и, если не были и туда идти не больше radius_move добавляем в очередь
            # ах да, ещё проверка выхода за пределы массива

            if self.get_square_by_pos(moves[i][0], moves[i][1]) in endest:
                farthest_cell = self.get_square_by_pos(moves[i][0], moves[i][1])
                endest.remove(farthest_cell)
                if not endest:
                    break

            if (not (moves[i][0] + 1, moves[i][1]) in moves  # ещё не посетили
                    and self.is_into_map(moves[i][0] + 1, moves[i][1])  # в пределах поля
                        and not self.is_barrier(moves[i][0] + 1, moves[i][1])  # можно пройти
                            and self.get_square_by_pos(moves[i][0] + 1, moves[i][1]).inner_piece is None):  # нет фигуры (если фигура = стена)
                moves.append((moves[i][0] + 1, moves[i][1]))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0] - 1, moves[i][1]) in moves
                    and self.is_into_map(moves[i][0] - 1, moves[i][1])
                        and not self.is_barrier(moves[i][0] - 1, moves[i][1])
                            and self.get_square_by_pos(moves[i][0] - 1, moves[i][1]).inner_piece is None):
                moves.append((moves[i][0] - 1, moves[i][1]))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0], moves[i][1] + 1) in moves
                    and self.is_into_map(moves[i][0], moves[i][1] + 1)
                        and not self.is_barrier(moves[i][0], moves[i][1] + 1)
                            and self.get_square_by_pos(moves[i][0], moves[i][1] + 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] + 1))
                len_way.append(len_way[i] + 1)

            if (not (moves[i][0], moves[i][1] - 1) in moves
                    and self.is_into_map(moves[i][0], moves[i][1] - 1)
                        and not self.is_barrier(moves[i][0], moves[i][1] - 1)
                            and self.get_square_by_pos(moves[i][0], moves[i][1] - 1).inner_piece is None):
                moves.append((moves[i][0], moves[i][1] - 1))
                len_way.append(len_way[i] + 1)

            i += 1

        return farthest_cell
