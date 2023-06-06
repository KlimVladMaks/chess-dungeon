import pygame as pg
import typing as tp

if tp.TYPE_CHECKING:
    from piece import Piece
    from menu import GameMenu

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
FLASH_COLOR = (255, 0, 0, 128)

# Время продолжительности вспышки клетки
FLASH_DELAY = 300


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

        # Если клетка активирована, то задаём ей активированный дизайн
        if self.is_activated:
            self.image = pg.image.load("design/field/activated_square.png")

        # Иначе, задаём ей обычный дизайн
        else:
            self.image = pg.image.load("design/field/square.png")

        # Если клетка занята, то рисуем на ней фигуру
        if self.is_occupied:

            # Если на клетке стоит белая пешка
            if type(self.inner_piece).__name__ == "Pawn":

                # Если фигура имеет ОД (может совершать действия)
                if self.inner_piece.active_turn:

                    # Если клетка выбрана
                    if self.is_selected:
                        self.image = pg.image.load("design/pieces/selected_pawn.png")

                    # Если клетка активирована
                    elif self.is_activated:
                        self.image = pg.image.load("design/pieces/attacked_pawn.png")

                    # Иначе
                    else:
                        self.image = pg.image.load("design/pieces/pawn.png")

                # Если клетка не имеет ОД (не может совершать действия)
                else:

                    # Если клетка выбрана
                    if self.is_selected:
                        self.image = pg.image.load("design/pieces/off_selected_pawn.png")

                    # Если клетка активирована
                    elif self.is_activated:
                        self.image = pg.image.load("design/pieces/off_attacked_pawn.png")

                    # Иначе
                    else:
                        self.image = pg.image.load("design/pieces/off_pawn.png")

            # Если на клетке стоит чёрная пешка
            elif type(self.inner_piece).__name__ == "EnemyPawn":

                # Если клетка активирована
                if self.is_activated:
                    self.image = pg.image.load("design/pieces/attacked_black_pawn.png")

                # Иначе
                else:
                    self.image = pg.image.load("design/pieces/black_pawn.png")

            # Если на клетке стоит чёрный король
            elif type(self.inner_piece).__name__ == "EnemyKing":

                # Если клетка активирована
                if self.is_activated:
                    self.image = pg.image.load("design/pieces/attacked_black_king.png")

                # Иначе
                else:
                    self.image = pg.image.load("design/pieces/black_king.png")

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

    def flash(self) -> None:
        """
        Функция для вызова кратковременной вспышки клетки.
        """

        # Закрашиваем клетку в цвет вспышки
        flash = pg.Surface((SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE), pg.SRCALPHA)
        flash.fill(FLASH_COLOR)
        self.image.blit(flash, (0, 0))
        self.field.update()

        # Делаем небольшую задержку
        pg.time.delay(FLASH_DELAY)

        # Возвращаем оригинальное изображение клетки
        self.update()
        self.field.update()


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
                 game_menu: 'GameMenu') -> None:
        """
        Функция для инициализации игрового поля.

        :param screen: Экран игры.
        :param screen_field: Экран игрового поля.
        :param background: Фон игры.
        :param screen_absolute_coordinates: Абсолютные координаты экрана игры.
        :param field_map: Карта игрового поля.
        :param game_menu: Игровое меню.
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
        self.screen.blit(self.game_menu.open_menu_button.image, self.game_menu.open_menu_button.rect)

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

        # Получаем размеры экрана
        screen_width = self.screen_field.get_width()
        screen_height = self.screen_field.get_height()

        # Если координата x выходит за пределы поля больше чем наполовину размера экрана, то обнуляем сдвиг по x
        if (x_screen_test < -(screen_width / 2)) or (x_screen_test + (screen_width / 2) > field_width):
            x_shift = 0

        # Если координата y выходит за пределы поля больше чем наполовину размера экрана, то обнуляем сдвиг по y
        if (y_screen_test < -(screen_height / 2)) or (y_screen_test + (screen_height / 2) > field_height):
            y_shift = 0

        # Сдвигаем каждую клетку игрового поля
        for square in self.squares_group:
            square.move(x_shift, y_shift)

        # Обновляем абсолютные координаты экрана
        self.screen_absolute_coordinates[0] -= x_shift
        self.screen_absolute_coordinates[1] -= y_shift

    """Совместно с svgarik"""

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

    """Совместно с svgarik"""

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

    """Совместно с svgarik"""

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

    """Совместно с svgarik"""

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
