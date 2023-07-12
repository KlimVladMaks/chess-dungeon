import pygame as pg
import typing as tp
from field import Square
from field import SQUARE_SIDE_SIZE
from field import GRAY_FILTER

if tp.TYPE_CHECKING:
    from field import Field
    from field import Square
    from piece import King

# Отступ для кнопки короля игрока
KING_SQUARE_MARGIN = 20

# Размер границы для кнопки короля игрока
KING_SQUARE_BORDER_SIZE = 2

# Цвет границы для кнопки короля игрока
KING_SQUARE_BORDER_COLOR = (0, 0, 0)


class KingSquare(Square):
    """
    Класс для реализации клетки (кнопки) короля игрока без необходимости добавлять фигуру игрока на поле.
    (Данная клетка имеет формат кнопки).
    """

    def __init__(self, field: 'Field', player_king: 'King') -> None:
        """
        Функция для инициализации кнопки короля.

        :param field: Игровое поле.
        :param player_king: Фигура короля игрока.
        """

        # Инициализируем родительскую клетку
        super().__init__(field.screen_field.get_width() - KING_SQUARE_MARGIN - SQUARE_SIDE_SIZE, 
                         field.screen_field.get_height() - KING_SQUARE_MARGIN - SQUARE_SIDE_SIZE, 
                         field)
        
        # Добавляем фигуру короля как внутреннюю фигуру клетки
        self.add_inner_piece(player_king)
        
        # Обновляем кнопку короля игрока
        self.update()

    def update(self):
        """
        Функция для обновления кнопки короля игрока.
        """

        # Загружаем базовый вариант клетки
        self.image = pg.image.load("design/field/square.png")

        # Отрисовываем на кнопке фигуру короля
        king_surface = pg.image.load("./design/pieces/King.png")
        self.image.blit(king_surface, (0, 0))

        # Если клетка не имеет доступных ходов и это не вражеская клетка, преобразуем её в чёрно-белые тона
        if (not self.inner_piece.active_turn) and self.inner_piece.controler != "comp":
            surface = pg.Surface(self.image.get_size(), pg.SRCALPHA)
            surface.fill(GRAY_FILTER)
            self.image.blit(surface, (0, 0))
        
        # Если клетка выбрана, то добавляем значок выбранной фигуры
        if self.is_selected:
            surface = pg.image.load("design/game/select.png")
            self.image.blit(surface, (0, 0))

        # Рисуем границу для кнопки короля игрока
        pg.draw.rect(self.image, 
                     KING_SQUARE_BORDER_COLOR, 
                     (0, 0, SQUARE_SIDE_SIZE, SQUARE_SIDE_SIZE), 
                     KING_SQUARE_BORDER_SIZE)

        # Обновляем область кнопки короля игрока
        self.rect = pg.Rect(self.field.screen_field.get_width() - KING_SQUARE_MARGIN - SQUARE_SIDE_SIZE, 
                            self.field.screen_field.get_height() - KING_SQUARE_MARGIN - SQUARE_SIDE_SIZE,
                            SQUARE_SIDE_SIZE, 
                            SQUARE_SIDE_SIZE)


