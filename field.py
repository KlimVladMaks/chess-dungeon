import pygame as pg
import typing as tp

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

        # Закрашиваем клетку в соответсвующий цвет
        self.image.fill(SQUARE_COLOR)

        # Рисуем границы клетки
        pg.draw.rect(self.image,
                     SQUARE_BORDER_COLOR,
                     pg.Rect(0, 0, self.side_size, self.side_size),
                     SQUARE_BORDER_WIDTH)

        # Флаг, показывающий активность/неактивность клетки
        self.is_activated = False

        # Указываем, что эта клетка существует
        self.is_exist = True

    def change_regime(self) -> None:
        """
        Функция для изменения режима шахматной клетки.
        Активная клетка становиться неактивной, а неактивная - активной.
        Активный режим отличается от неактивного другим цветом клетки.
        """

        # Если клетка активна, то меняем аё цвет на обычный и убираем флаг активации
        if self.is_activated:
            self.change_color(SQUARE_COLOR, SQUARE_BORDER_COLOR)
            self.is_activated = False

        # Если клетка неактивна, то меняем её цвет на активный и ставим флаг активации
        else:
            self.change_color(SQUARE_ACTIVATED_COLOR, SQUARE_BORDER_COLOR)
            self.is_activated = True

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

        # Указываем, что клетка не существует
        self.is_exist = False


class Field:
    """
    Класс для реализации игрового поля.
    """

    def __init__(self, screen: pg.Surface,
                 background: pg.Surface,
                 screen_absolute_coordinates: list[int],
                 field_map: list[list[int]]) -> None:
        """
        Функция для инициализации игрового поля.

        :param screen: Экран игры.
        :param background: Фон игры.
        :param screen_absolute_coordinates: Абсолютные координаты экрана игры.
        :param field_map: Карта игрового поля.
        """

        # Сохраняем экран игры
        self.screen = screen

        # Сохраняем фон игры
        self.background = background

        # Сохраняем абсолютные координаты экрана игры
        self.screen_absolute_coordinates = screen_absolute_coordinates

        # Сохраняем карту игрового поля
        self.field_map = field_map

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
        self.screen.blit(self.background, (0, 0))
        self.squares_group.draw(self.screen)
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
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

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
