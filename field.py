import pygame as pg
import typing as tp
from square import *


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
                    square = Square(x, y)
                    self.squares_group.add(square)
                    inner_list.append(square)
                else:
                    nonexistent_square = NonexistentSquare(x, y)
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
