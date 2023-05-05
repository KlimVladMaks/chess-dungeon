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

    def __init__(self, x: int, y: int) -> None:
        """
        Инициализация шахматной клетки.

        :param x:
        :param y:
        """

        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем размер стороны клетки
        self.side_size = SQUARE_SIDE_SIZE

        # Задаём поверхность клетки
        self.image = pg.Surface((self.side_size, self.side_size))

        # Задаём область клетки, основываясь на переданных координатах
        self.rect = pg.Rect(x, y, self.side_size, self.side_size)

        # Указываем, что эта клетка не существует (т.к. это лишь шаблон)
        self.is_exist = False

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

    def __init__(self, x: int, y: int) -> None:
        """
        Инициализация шахматной клетки.

        :param x: Координата x на экране.
        :param y: Координата y на экране.
        """

        # Инициализируем шаблон клетки
        super().__init__(x, y)

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

    def __init__(self, x: int, y: int) -> None:
        """
        Инициализируем несуществующую шахматную клетку.

        :param x: Координата x на экране.
        :param y: Координата y на экране.
        """

        # Инициализируем шаблон клетки
        super().__init__(x, y)

        # Указываем, что клетка не существует
        self.is_exist = False
