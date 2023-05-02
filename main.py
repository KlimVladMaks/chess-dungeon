import pygame as pg
import typing as tp
from square import *
from view import *

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
    level_map = [[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

    # Двухмерный список для хранения спрайтов шахматных клеток
    squares_list: list[list[SquareObject]] = []

    # Группа для хранения спрайтов шахматных клеток
    squares_group = pg.sprite.Group()

    # Часы для регулировки FPS
    clock = pg.time.Clock()

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
                nonexistent_square = NonexistentSquare(x, y)
                squares_group.add(nonexistent_square)
                inner_list.append(nonexistent_square)
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

            # Если нажата левая клавиша мыши
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                
                # Получаем нажатую клетку
                square_clicked = get_square_by_coordinates(squares_list, pg.mouse.get_pos(), (x_screen, y_screen))
                
                #Проверка, зажата ли клавиша клавища с цифрой при клике по клетке 
                if True in pg.key.get_pressed():
                   
                    #PS Я понятие не имею, почему при выполнении условия ниже
                    #строчка pg.key.get_pressed()[I] выдаёт False, а сейчас разбираться лень
                    radius_view = pg.key.get_pressed().index(True) - 29
                    if radius_view >= 1 and radius_view <= 10:
                        
                        #получаем позицию нажатой клетки в массиве
                        pos = get_pos_by_coordinates(squares_list, pg.mouse.get_pos(), (x_screen, y_screen))
                        
                        #создаём абстрактную фигуру в нажатой клетке и расскрашиваем её обзор
                        if not pos is None:
                            view_cells = Piece(level_map, pos, radius_view).get_view()
                            for square in view_cells:
                                square_clicked = get_square_by_pos(squares_list, square)
                                if (square_clicked is not None) and square_clicked.is_exist:
                                    square_clicked.change_regime()
                                    screen.blit(background, (0, 0))
                                    squares_group.draw(screen)
                                    pg.display.update()

                else:
                    # Если полученная клетка не равна None, то меняем её цвет и обновляем экран
                    if (square_clicked is not None) and square_clicked.is_exist:
                        square_clicked.change_regime()
                        screen.blit(background, (0, 0))
                        squares_group.draw(screen)
                        pg.display.update()

            # Если нажата правая клавиша мыши, то ставим флаг движения карты и сохраняем позицию курсора
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
                is_map_moving = True
                mouse_pos = pg.mouse.get_pos()

            # Если мышь движется с установленным флагом движения карты
            elif e.type == pg.MOUSEMOTION and is_map_moving:

                # Находим сдвиг по x и y
                new_mouse_pos = pg.mouse.get_pos()
                x_shift = new_mouse_pos[0] - mouse_pos[0]
                y_shift = new_mouse_pos[1] - mouse_pos[1]

                # Рассчитываем потенциальные новые абсолютные координаты экрана
                x_screen_test = x_screen - x_shift
                y_screen_test = y_screen - y_shift

                # Рассчитываем размеры поля
                field_width = len(squares_list[0]) * get_square_side_size(squares_list)
                field_height = len(squares_list) * get_square_side_size(squares_list)

                # Если координата x выходит за пределы поля больше чем наполовину размера экрана, то обнуляем сдвиг по x
                if (x_screen_test < -(SCREEN_WIDTH / 2)) or (x_screen_test + (SCREEN_WIDTH / 2) > field_width):
                    x_shift = 0

                # Если координата y выходит за пределы поля больше чем наполовину размера экрана, то обнуляем сдвиг по y
                if (y_screen_test < -(SCREEN_HEIGHT / 2)) or (y_screen_test + (SCREEN_HEIGHT / 2) > field_height):
                    y_shift = 0

                # Обновляем координаты экрана относительно карты уровня
                x_screen -= x_shift
                y_screen -= y_shift

                # Обновляем координаты спрайтов шахматных клеток
                for s in squares_group:
                    s.move(x_shift, y_shift)

                # Сохраняем новую позицию курсора
                mouse_pos = new_mouse_pos

                # Перерисовываем шахматные клетки
                screen.blit(background, (0, 0))
                squares_group.draw(screen)
                pg.display.update()

            # Если отпущена правая клавиша мыши, то снимаем флаг движения карты
            elif e.type == pg.MOUSEBUTTONUP and e.button == 3:
                is_map_moving = False

            # Если колёсико мышки прокручено вперёд
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 4:

                # Если размер клетки уже превосходит допустимое значение, то пропускаем итерацию
                if squares_list[0][0].side_size > min(SCREEN_WIDTH, SCREEN_HEIGHT) * MAX_SQUARE_SIDE_SIZE:
                    continue

                # Увеличиваем масштаб поля
                zoom_in_field(squares_list)

                # Проверяем и при наличии исправляем выход за пределы поля
                x_screen, y_screen = fix_out_of_field(x_screen,
                                                      y_screen,
                                                      screen,
                                                      squares_group,
                                                      squares_list,
                                                      background)

                # Перерисовываем шахматные клетки
                screen.blit(background, (0, 0))
                squares_group.draw(screen)
                pg.display.update()

            # Если колёсико мышки прокручено назад
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 5:

                # Если размер клетки уже меньше допустимого значения, то пропускаем итерацию
                if squares_list[0][0].side_size < max(SCREEN_WIDTH, SCREEN_HEIGHT) * MIN_SQUARE_SIDE_SIZE:
                    continue

                # Уменьшаем масштаб поля
                zoom_out_field(squares_list)

                # Проверяем и при наличии исправляем выход за пределы поля
                x_screen, y_screen = fix_out_of_field(x_screen,
                                                      y_screen,
                                                      screen,
                                                      squares_group,
                                                      squares_list,
                                                      background)

                # Перерисовываем шахматные клетки
                screen.blit(background, (0, 0))
                squares_group.draw(screen)
                pg.display.update()


def get_square_side_size(squares_list: list[list[SquareObject]]) -> int:
    """
    Функция для получения текущего размера стороны шахматной клетки.

    :param squares_list: Двухмерный список с шахматными клетками игрового поля.
    :return: Текущий размер стороны шахматной клетки.
    """

    # Перебираем элементы списка и возвращаем размер стороны первой попавшейся шахматной клетки
    # т.к. у всех клеток должен быть одинаковый размер стороны
    for i in range(len(squares_list)):
        for j in range(len(squares_list[i])):
            if squares_list[i][j] is not None:
                return squares_list[i][j].side_size


def get_square_by_coordinates(squares_list: list[list[SquareObject]],
                              square_pos: tuple[int, int],
                              screen_pos: tuple[int, int]) -> tp.Union[SquareObject, None]:
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

    # Если абсолютные x или y меньше 0, то возвращаем None
    if x_absolute < 0 or y_absolute < 0:
        return None

    # Отлавливаем ошибки для избежания выхода из диапазона
    try:

        # Рассчитываем позицию клетки и извлекаем её из двухмерного списка
        square_col = x_absolute // get_square_side_size(squares_list)
        square_row = y_absolute // get_square_side_size(squares_list)
        found_square = squares_list[square_row][square_col]

    # При выходе из диапазона возвращаем None
    except IndexError:
        return None

    # Возвращаем найденную клетку
    return found_square

def get_pos_by_coordinates(squares_list: list[list[SquareObject]],
                              square_pos: tuple[int, int],
                              screen_pos: tuple[int, int]) -> tuple[int]:
    """
    Эта функция копирует функцию выше, но возвращает координаты клетки в массиве
    """

    # Рассчитываем абсолютные координаты клетки
    x_absolute = square_pos[0] + screen_pos[0]
    y_absolute = square_pos[1] + screen_pos[1]

    # Если абсолютные x или y меньше 0, то возвращаем None
    if x_absolute < 0 or y_absolute < 0:
        return None

    # Отлавливаем ошибки для избежания выхода из диапазона
    try:

        # Рассчитываем позицию клетки и извлекаем её из двухмерного списка
        square_col = x_absolute // get_square_side_size(squares_list)
        square_row = y_absolute // get_square_side_size(squares_list)

    # При выходе из диапазона возвращаем None
    except IndexError:
        return None

    # Возвращаем найденную клетку
    return (square_col, square_row)

def get_square_by_pos(squares_list: list[list[SquareObject]],
                      pos: tuple[int]) -> tp.Union[SquareObject, None]:
    """
    Получаем клетку по её индексам в массиве
    """
    found_square = squares_list[pos[0]][pos[1]]
    return found_square

def zoom_in_field(squares_list: list[list[SquareObject]]) -> None:
    """
    Функция для увеличения масштаба поля.

    :param squares_list: Двухмерный список с шахматными клетками игрового поля.
    """

    # Увеличиваем размер каждой клетки поля
    for i in range(len(squares_list)):
        for j in range(len(squares_list[i])):
            if squares_list[i][j] is not None:
                squares_list[i][j].increase_size()

    # Выравниваем поле
    level_field(squares_list)


def zoom_out_field(squares_list: list[list[SquareObject]]) -> None:
    """
    Функция для уменьшения масштаба поля.

    :param squares_list: Двухмерный список с шахматными клетками игрового поля.
    """

    # Уменьшаем размер каждой клетки поля
    for i in range(len(squares_list)):
        for j in range(len(squares_list[i])):
            if squares_list[i][j] is not None:
                squares_list[i][j].decrease_size()

    # Выравниваем поле
    level_field(squares_list)


def level_field(squares_list: list[list[SquareObject]]) -> None:
    """
    Функция для выравнивания шахматного поля (можно использовать при изменении размеров шахматных клеток).

    :param squares_list: Двухмерный список с шахматными клетками игрового поля.
    """

    # Если поле пусто, то завершаем выполнение функции
    if len(squares_list) == 0:
        return

    # Обновляем координаты всех клеток в соответствии с их размерами
    x = squares_list[0][0].rect.x
    y = squares_list[0][0].rect.y
    for i in range(len(squares_list)):
        for j in range(len(squares_list[i])):
            squares_list[i][j].rect.x = x
            squares_list[i][j].rect.y = y
            x += get_square_side_size(squares_list)
        y += get_square_side_size(squares_list)
        x = squares_list[0][0].rect.x


def fix_out_of_field(x_screen: int,
                     y_screen: int,
                     screen: pg.Surface,
                     squares_group: pg.sprite.Group,
                     squares_list: list[list[SquareObject]],
                     background: pg.Surface) -> tuple[int, int]:
    """
    Функция для проверки и при наличии исправления выхода за пределы поля.

    :param x_screen: Абсолютная координата x экрана.
    :param y_screen: Абсолютная координата y экрана.
    :param screen: Поверхность экрана.
    :param squares_group: Группа клеток-спрайтов.
    :param squares_list: Двухмерный список клеток-спрайтов.
    :param background: Поверхность фона.
    :return: Новые координаты (x, y) экрана.
    """

    # Рассчитываем размеры поля
    field_width = len(squares_list[0]) * get_square_side_size(squares_list)
    field_height = len(squares_list) * get_square_side_size(squares_list)

    # По-умолчанию ставим флаг, что экран выходит за поле
    is_out_of_field = True

    # Цикл длится, пока выход за пределы поле не будет исправлен
    while is_out_of_field:

        # Указываем, что пока выхода за пределы поля не обнаружено
        is_out_of_field = False

        # Проверяем выход за пределы поля по X влево.
        # При наличии исправляем на один пиксель и указываем, что выход за поле обнаружен
        if x_screen < -(SCREEN_WIDTH / 2):
            is_out_of_field = True
            for s in squares_group:
                s.move(-1, 0)
            x_screen += 1
            screen.blit(background, (0, 0))
            squares_group.draw(screen)
            pg.display.update()

        # Проверяем выход за пределы поля по X вправо.
        # При наличии исправляем на один пиксель и указываем, что выход за поле обнаружен
        if x_screen + (SCREEN_WIDTH / 2) > field_width:
            is_out_of_field = True
            for s in squares_group:
                s.move(1, 0)
            x_screen -= 1
            screen.blit(background, (0, 0))
            squares_group.draw(screen)
            pg.display.update()

        # Проверяем выход за пределы поля по Y влево.
        # При наличии исправляем на один пиксель и указываем, что выход за поле обнаружен
        if y_screen < -(SCREEN_HEIGHT / 2):
            is_out_of_field = True
            for s in squares_group:
                s.move(0, -1)
            y_screen += 1
            screen.blit(background, (0, 0))
            squares_group.draw(screen)
            pg.display.update()

        # Проверяем выход за пределы поля по Y вправо.
        # При наличии исправляем на один пиксель и указываем, что выход за поле обнаружен
        if y_screen + (SCREEN_HEIGHT / 2) > field_height:
            is_out_of_field = True
            for s in squares_group:
                s.move(0, 1)
            y_screen -= 1
            screen.blit(background, (0, 0))
            squares_group.draw(screen)
            pg.display.update()

    # Возвращаем координаты экрана
    return x_screen, y_screen


# Запускаем Main-функцию
if __name__ == "__main__":
    main()
