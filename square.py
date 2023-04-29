import pygame as pg

# Размер стороны шахматной клетки
SQUARE_SIDE_SIZE = 40

# Цвет шахматной клетки
SQUARE_COLOR = "#FFFFFF"

# Цвет активной клетки
SQUARE_ACTIVATED_COLOR = "#008000"

# Ширина границы шахматной клетки
SQUARE_BORDER_WIDTH = 1

# Цвет границы шахматной клетки
SQUARE_BORDER_COLOR = "#000000"


class Square(pg.sprite.Sprite):
    """
    Класс для реализации спрайта шахматной клетки.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Инициализация шахматной клетки.

        :param x: Координата x на экране.
        :param y: Координата y на экране.
        """

        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Задаём поверхность клетки и закрашиваем её в соответсвующий цвет
        self.image = pg.Surface((SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE))
        self.image.fill(SQUARE_COLOR)

        # Рисуем границы клетки
        pg.draw.rect(self.image,
                     SQUARE_BORDER_COLOR,
                     pg.Rect(0, 0, SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE),
                     SQUARE_BORDER_WIDTH)

        # Задаём область клетки, основываясь на переданных координатах
        self.rect = pg.Rect(x, y, SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE)

        # Флаг, показывающий активность/неактивность клетки
        self.is_activated = False

    def move(self, x_shift: int, y_shift: int) -> None:
        """
        Функция для сдвига позиции шахматной клетки.

        :param x_shift: Сдвиг по x.
        :param y_shift: Сдвиг по y.
        """

        # Сдвигаем область клетки на заданные координатные сдвиги
        self.rect.move_ip(x_shift, y_shift)

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
                     pg.Rect(0, 0, SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE),
                     SQUARE_BORDER_WIDTH)
