import pygame as pg
import typing as tp
from square import *

# Ширина и высота экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвет фона
BACKGROUND_COLOR = "#000000"

# Частота кадров
FPS = 60

"""
Примечание:

Данный вариант предполагает наличия двух видов координат - абсолютных и относительных. Абсолютные координаты привязаны к
карте и их началом является верхний левый угол верхнего левого квадрата карты. Относительные координаты привязаны к 
экрану и их началом является верхний левый угол видимой области (экрана).
"""


def main() -> None:
    """
    Main-функция.
    """

    # Координаты экрана относительно карты уровня
    x_screen = 0
    y_screen = 0

    # Карта уровня (1 - есть шахматная клетка, 0 - нет)
    level_map = [[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

    # Двухмерный список для хранения спрайтов шахматных клеток
    squares_list: list[list[tp.Union[Square, None]]] = []

    # Группа для хранения спрайтов шахматных клеток
    squares_group = pg.sprite.Group()

    # Часы для регулировки FPS
    clock = pg.time.Clock()

    # Флаг, показывающий, что пользователь нажимает на шахматную клетку
    is_clicking_on_square = False

    # Флаг, показывающий, что пользователь двигает карту
    is_map_moving = False

    # Переменная для хранения позиции курсора
    mouse_pos: tuple[int, int] = (0, 0)

    # Инициализируем игру
    pg.init()

    # Создаём экран игры
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Задаём заголовок игры
    pg.display.set_caption("Chess Dungeon")

    # Устанавливаем фон
    background = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))

    # Координаты начала экрана
    x = 0
    y = 0

    # Создаём шахматные клетки, задаём им стартовые координаты и помещаем в спрайт-группу.
    # Заполняем двухмерный список с шахматными клетками
    for row in level_map:
        inner_list = []
        for col in row:
            if col == 1:
                square = Square(x, y)
                squares_group.add(square)
                inner_list.append(square)
            else:
                inner_list.append(None)
            x += SQUARE_SIDE_SIZE
        y += SQUARE_SIDE_SIZE
        x = 0
        squares_list.append(inner_list)

    # Отрисовываем шахматные клетки
    squares_group.draw(screen)

    # Обновляем экран
    pg.display.update()

    # Запускаем игровой цикл
    while True:

        # Регулируем FPS
        clock.tick(FPS)

        # Перебираем возникшие игровые события
        for e in pg.event.get():

            # При закрытии игрового окна завершаем программу
            if e.type == pg.QUIT:
                pg.quit()
                return

            # Если нажата левая клавиша мыши, то ставим флаг нажатия на клетку и сохраняем позицию курсора
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                is_clicking_on_square = True
                mouse_pos = pg.mouse.get_pos()

            # Если мышь движется с установленным флагом нажатия на клетку или флагом движения карты
            elif e.type == pg.MOUSEMOTION and (is_clicking_on_square or is_map_moving):

                # Меняем флаг нажатия на клетку на флаг движения карты
                if not is_map_moving:
                    is_clicking_on_square = False
                    is_map_moving = True

                # Находим сдвиг по x и y
                new_mouse_pos = pg.mouse.get_pos()
                x_shift = new_mouse_pos[0] - mouse_pos[0]
                y_shift = new_mouse_pos[1] - mouse_pos[1]

                # Обновляем координаты экрана относительно карты уровня
                x_screen -= x_shift
                y_screen -= y_shift

                # Обновляем координаты спрайтов шахматных клеток
                for s in squares_group:
                    s.move(x_shift, y_shift)

                # Сохраняем новую позицию курсора
                mouse_pos = new_mouse_pos

                # Отрисовываем шахматные клетки
                screen.blit(background, (0, 0))
                squares_group.draw(screen)
                pg.display.update()

            # Если левая кнопка мыши отпущена
            elif e.type == pg.MOUSEBUTTONUP and e.button == 1:

                # Если это был клик по клетке
                if is_clicking_on_square:

                    # Получаем нажатую клетку
                    square_clicked = get_square_by_coordinates(squares_list, pg.mouse.get_pos(), (x_screen, y_screen))

                    # Если полученная клетка не равна None, то меняем её цвет и обновляем экран
                    if square_clicked is not None:
                        square_clicked.change_regime()
                        screen.blit(background, (0, 0))
                        squares_group.draw(screen)
                        pg.display.update()

                # Снимаем флаг нажатия на клетку и флаг движения карты
                is_clicking_on_square = False
                is_map_moving = False


def get_square_by_coordinates(squares_list: list[list[tp.Union[Square, None]]],
                              square_pos: tuple[int, int],
                              screen_pos: tuple[int, int]) -> tp.Union[Square, None]:
    """
    Функция для нахождения клетки по её координатам.

    :param squares_list: Двухмерный список с шахматными клетками игрового поля.
    :param square_pos: Координаты клетки.
    :param screen_pos: Координаты экрана.
    :return: Найденная клетка или None (если клетка не найдена).
    """

    # Рассчитываем абсолютные координаты клетки
    x_absolute = square_pos[0] + screen_pos[0]
    y_absolute = square_pos[1] + screen_pos[1]

    # Если x или y меньше 0, то возвращаем None
    if x_absolute < 0 or y_absolute < 0:
        return None

    # Отлавливаем ошибки для избежания выхода из диапазона
    try:

        # Рассчитываем позицию клетки и извлекаем её из двухмерного списка
        square_col = x_absolute // SQUARE_SIDE_SIZE
        square_row = y_absolute // SQUARE_SIDE_SIZE
        found_square = squares_list[square_row][square_col]

    # При выходе из диапазона возвращаем None
    except IndexError:
        return None

    # Возвращаем найденную клетку
    return found_square


# Запускаем Main-функцию
if __name__ == "__main__":
    main()
