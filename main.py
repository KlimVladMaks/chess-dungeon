import pygame as pg
import typing as tp
from field import *
from piece import *
from enemy import *

# Ширина и высота экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвет фона
BACKGROUND_COLOR = "#000000"

# Частота кадров
FPS = 60

# Стартовая структура игрового поля (1 - есть шахматная клетка, 0 - нет)
START_FIELD_MAP = [[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
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

    # Абсолютные координаты экрана относительно карты уровня
    screen_absolute_coordinates = [0, 0]

    # Часы для регулировки FPS
    clock = pg.time.Clock()

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
    pg.display.update()

    # Создаём игровое поле
    field = Field(screen, background, screen_absolute_coordinates, START_FIELD_MAP)

    #Тест расположения фигуры
    first_piece = Pawn(field, field.get_square_by_pos(6, 6), 10, 0.5, 2, 3, 1)
    second_piece = Pawn(field, field.get_square_by_pos(5, 6), 10, 0.5, 2, 3, 1)

    first_piece.cell.add_inner_piece(first_piece)
    second_piece.cell.add_inner_piece(second_piece)

    #флаг, что выбрана фигура для движения
    select_piece_for_move = None
    #флаг, что выбрана фигура для атаки
    select_piece_for_cast = None

    #Тест расположения фигуры - КОНЕЦ

    start = None
    end = None
    empty = EnemyPiece(field, field.get_square_by_pos(4, 6), 10, 0.5, 2, 3, 1)


    # Отрисовываем игровое поле
    field.update()

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
            
            elif e.type == pg.KEYDOWN and e.unicode == 's':
                # Получаем относительные координаты клика
                click_coordinates = pg.mouse.get_pos()

                # Получаем нажатую клетку
                start = field.get_square_by_coordinates(click_coordinates[0], click_coordinates[1])

                print(start.get_pos())

            elif e.type == pg.KEYDOWN and e.unicode == 'e':
                # Получаем относительные координаты клика
                click_coordinates = pg.mouse.get_pos()

                # Получаем нажатую клетку
                end = field.get_square_by_coordinates(click_coordinates[0], click_coordinates[1])

                print(end.get_pos())

            elif e.type == pg.KEYDOWN and e.unicode == 'w':
                
                way = empty.get_way(start, end)
                
                for cell in way:
                    cell.change_regime()

                print(way)
                field.update
                

            # Если нажата левая клавиша мыши
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:

                # Получаем относительные координаты клика
                click_coordinates = pg.mouse.get_pos()

                # Получаем нажатую клетку
                square_clicked = field.get_square_by_coordinates(click_coordinates[0], click_coordinates[1])

                # Если клетка относится к классу Square, то меняем её режим и обновляем поле
                if isinstance(square_clicked, Square):

                    #Тестовая часть управления фигурой
                    
                    #Тут если зажата клавиша "M" и не выделена фигура для атаки
                    #Это выделение фигуры для последующего движения
                    if (isinstance(square_clicked.inner_piece, Piece)
                        and True in pg.key.get_pressed() and pg.key.get_pressed().index(True) == 16
                            and select_piece_for_cast is None):
                        
                        piece = square_clicked.inner_piece

                        #Если был повторный клик по выделенной фигуре
                        if select_piece_for_move == piece:
                            #снимаем метку
                            select_piece_for_move = None
                            #И обратно закрашиваем клетки
                            square_for_move = piece.prepare_spell('move')
                            for cell in square_for_move:
                                cell.change_regime()
                        
                        else:
                            
                            #Если у нас уже была выделена клетка, а теперь попытка выделить другую - удаляем старую закраску
                            if not select_piece_for_move is None:
                                square_for_move = select_piece_for_move.prepare_spell('move')
                                for cell in square_for_move:
                                    cell.change_regime()

                            #ставим метку на фигуру и расскрашиваем область для движения
                            select_piece_for_move = piece
                            square_for_move = piece.prepare_spell('move')
                            for cell in square_for_move:
                                cell.change_regime()

                    #Тут если зажата клавиша "0" и не выделена фигура для движения
                    #Это выделение фигуры для последующей атаки
                    elif (isinstance(square_clicked.inner_piece, Piece)
                        and True in pg.key.get_pressed() and pg.key.get_pressed().index(True) == 39
                            and select_piece_for_move is None):
                        
                        piece = square_clicked.inner_piece
                        
                        #Если был повторный клик по выделенной фигуре
                        if select_piece_for_cast == piece:

                            #снимаем метку
                            select_piece_for_cast = None
                            #И обратно закрашиваем клетки
                            square_for_cast = piece.prepare_spell('attack')
                            for cell in square_for_cast:
                                cell.change_regime()
                        
                        else:
                            
                            #Если у нас уже была выделена клетка, а теперь попытка выделить другую - удаляем старую закраску
                            if not select_piece_for_cast is None:
                                square_for_cast = select_piece_for_cast.prepare_spell('attack')
                                for cell in square_for_cast:
                                    cell.change_regime()

                            #ставим метку на фигуру и расскрашиваем область для атаки
                            select_piece_for_cast = piece
                            square_for_cast = piece.prepare_spell('attack')
                            for cell in square_for_cast:
                                cell.change_regime()

                            #для удобства и наглядности, если целей для атаки нет - снимаем выделение
                            if not square_for_cast:
                                select_piece_for_cast = None

                    #если кликнули клетку с выделенной для перемещения фигурой
                    elif not select_piece_for_move is None:
                        
                        #и она выделена
                        if square_clicked.is_activated:

                            #убираем выделение
                            square_for_move = select_piece_for_move.prepare_spell('move')
                            for cell in square_for_move:
                                cell.change_regime()

                            #Передвигаем
                            select_piece_for_move.cast_spell('move', square_clicked)

                            select_piece_for_move = None

                    #Если кликнули на клетку
                    elif not select_piece_for_cast is None and square_clicked.is_activated:

                        #убираем выделение
                        square_for_cast = piece.prepare_spell('attack')
                        for cell in square_for_cast:
                            cell.change_regime()

                        #и она выделена
                        select_piece_for_cast.cast_spell('attack', square_clicked)

                        select_piece_for_cast = None

                        #Пока что просто получаем в консоле результат

                    field.update()

                    """
                    Отключаем свободную раскраску
                    else:
                        square_clicked.change_regime()
                        field.update()
                    """


            # Если нажата правая клавиша мыши, то ставим флаг движения карты и флаг для пропуска первого сдвига
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
                field.is_moving = True
                field.skip_first_move = True

            # Если мышь движется с установленным флагом движения карты
            elif e.type == pg.MOUSEMOTION and field.is_moving:

                # Находим сдвиг курсора по x и y
                mouse_shift = pg.mouse.get_rel()
                x_shift = mouse_shift[0]
                y_shift = mouse_shift[1]

                # Если у поля стоит флаг пропуска первого сдвига, то снимаем данный флаг и пропускаем итерацию
                if field.skip_first_move:
                    field.skip_first_move = False
                    continue

                # Сдвигаем игровое поле и обновляем его
                field.move(x_shift, y_shift)
                field.update()

            # Если отпущена правая клавиша мыши, то снимаем флаг движения карты и флаг пропуска первого сдвига
            elif e.type == pg.MOUSEBUTTONUP and e.button == 3:
                field.is_moving = False
                field.skip_first_move = False


# Запускаем Main-функцию
if __name__ == "__main__":
    main()
