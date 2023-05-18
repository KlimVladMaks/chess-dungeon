import pygame as pg
import typing as tp
from field import *
from piece import *
from enemy import *
from interface import *

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

    # Создаём поверхность, предназначенную для отображения игрового поля
    screen_field = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Задаём заголовок игры
    pg.display.set_caption("Chess Dungeon")

    # Устанавливаем фон
    background = pg.image.load("design/background.png")
    screen.blit(background, (0, 0))
    pg.display.update()

    # Создаём игровое поле
    field = Field(screen, screen_field, background, screen_absolute_coordinates, START_FIELD_MAP)

    # Создаём интерфейс для управления фигурами
    interface = Interface(screen, field)

    # Переменная для хранения выбранной фигуры
    selected_piece: tp.Union[Piece, None] = None

    # Переменная для хранения выбранного действия
    selected_action: tp.Union[str, None] = None

    # Тест расположения фигуры
    first_piece = Pawn(field, field.get_square_by_pos(6, 6), 10, 0.5, 2, 3, 1)
    second_piece = Pawn(field, field.get_square_by_pos(5, 6), 10, 0.5, 2, 3, 1)
    first_piece.cell.add_inner_piece(first_piece)
    second_piece.cell.add_inner_piece(second_piece)

    enemy = EnemyPawn(field, field.get_square_by_pos(15, 17), 10, 0.5, 2, 3, 5)
    enemy.set_way_patrol(field.get_square_by_pos(7, 6))
    enemy.cell.add_inner_piece(enemy)

    # Помещаем все фигуры в список
    pieces = [first_piece, second_piece, enemy]

    # флаг, что выбрана фигура для движения
    select_piece_for_move = None
    # флаг, что выбрана фигура для атаки
    select_piece_for_cast = None

    # Тест расположения фигуры - КОНЕЦ

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

            # Если нажата кнопка N
            elif e.type == pg.KEYDOWN and e.key == 110:

                # Делаем новый ход для каждой фигуры и обновляем поле
                for piece in pieces:
                    piece.new_turn()
                field.update()

            # Если нажата левая клавиша мыши
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:

                # Получаем относительные координаты клика
                click_coordinates = pg.mouse.get_pos()

                # Если координаты клика попадают в область интерфейса
                if interface.are_interface_coordinates(click_coordinates[0], click_coordinates[1]):

                    # Получаем нажатую кнопку интерфейса
                    button = interface.get_button_by_coordinates(click_coordinates[0], click_coordinates[1])

                    # Если кнопка не нажата (т.е. было возвращено значение None), то пропускаем итерацию
                    if button is None:
                        continue

                    # Если выбрана кнопка движения
                    if button.action == "move":

                        # Если ранее было выбрано действие атаки, то убираем для него выделенные клетки
                        if selected_action == "attack":
                            square_for_cast = selected_piece.prepare_spell('attack')
                            for cell in square_for_cast:
                                cell.change_regime()
                            field.update()

                        # Меняем режим доступных для движения клеток (снимаем или добавляем выделение)
                        square_for_move = selected_piece.prepare_spell('move')
                        for cell in square_for_move:
                            cell.change_regime()
                        field.update()

                        # Добавляем или убираем движение в качестве выбранного действия
                        # (Движение может быть добавлена как выделенное действие
                        # лишь при наличии хотя бы одной выделенной клетки)
                        if square_for_move and (selected_action != "move"):
                            selected_action = "move"
                        else:
                            selected_action = None

                    # Если выбрана кнопка атаки
                    elif button.action == "attack":

                        # Если ранее было выбрано действие движения, то убираем для него выделенные клетки
                        if selected_action == "move":
                            square_for_cast = selected_piece.prepare_spell('move')
                            for cell in square_for_cast:
                                cell.change_regime()
                            field.update()

                        # Меняем режим доступных для атаки клеток (снимаем или добавляем выделение)
                        square_for_cast = selected_piece.prepare_spell('attack')
                        for cell in square_for_cast:
                            cell.change_regime()
                        field.update()

                        # Добавляем или убираем атаку в качестве выбранного действия
                        # (Атака может быть добавлена как выделенное действие
                        # лишь при наличии хотя бы одной выделенной клетки)
                        if square_for_cast and (selected_action != "attack"):
                            selected_action = "attack"
                        else:
                            selected_action = None

                # Получаем нажатую клетку
                square_clicked = field.get_square_by_coordinates(click_coordinates[0], click_coordinates[1])

                # Если клетка относится к классу Square (т.е. существует)
                if isinstance(square_clicked, Square):

                    # Если на клетке стоит фигура, выделенная для действия, направленного на неё
                    if isinstance(square_clicked.inner_piece, Piece) and square_clicked.is_activated:

                        # Если выбрано действие атаки
                        if selected_action == "attack":

                            # Очищаем раннее выделенные для атаки клетки
                            square_for_cast = selected_piece.prepare_spell('attack')
                            for cell in square_for_cast:
                                cell.change_regime()

                            # Атакуем выбранную фигуру
                            selected_piece.cast_spell('attack', square_clicked)

                            # Указываем, что клетка на которой стоит фигура, теперь не является выделенной
                            selected_piece.cell.deselect()

                            # Очищаем переменные с выделенными фигурой и действием
                            selected_piece = None
                            selected_action = None

                            # Закрываем интерфейс
                            interface.close()

                    # Если на клетке находится ранее не выбранная фигура
                    elif isinstance(square_clicked.inner_piece, Piece) and (
                            square_clicked.inner_piece != selected_piece):

                        # Если уже есть выбранное действие, то пропускаем итерацию
                        if selected_action is not None:
                            continue

                        # Если существовала ранее выбранная фигура, то убираем выделение у её клетки
                        if selected_piece is not None:
                            selected_piece.cell.deselect()

                        # Сохраняем выбранную фигуру
                        selected_piece = square_clicked.inner_piece

                        # Выделяем клетку, на которой стоит выбранная фигура
                        selected_piece.cell.select()

                        # Очищаем группу со старыми кнопками
                        interface.buttons_group.empty()

                        """
                        По идее, нужно брать список действий из фигуры, но пока задаём вручную.
                        """

                        # Задаём новые кнопки с действиями
                        interface.add_buttons(["move", "attack"])

                        # Открываем интерфейс
                        interface.open()

                    # Если на клетке находится ранее выбранная фигура
                    elif isinstance(square_clicked.inner_piece, Piece) and square_clicked.inner_piece == selected_piece:

                        # Отменяем выделение клетки, на которой стоит выбранная фигура
                        selected_piece.cell.deselect()

                        # Если есть выделенные для движения клетки, то очищаем их
                        square_for_move = selected_piece.prepare_spell('move')
                        if square_for_move[0].is_activated:
                            for cell in square_for_move:
                                cell.change_regime()

                        # Если есть выделенные для атаки клетки, то очищаем их
                        square_for_move = selected_piece.prepare_spell('attack')
                        if len(square_for_move) > 0 and square_for_move[0].is_activated:
                            for cell in square_for_move:
                                cell.change_regime()

                        # Очищаем переменную с выбранной фигурой
                        selected_piece = None

                        # Очищаем переменную с выбранным действием
                        selected_action = None

                        # Закрываем интерфейс
                        interface.close()

                    # Если нажатая клетка была выделена для определённого действия (не связанного с другими фигурами)
                    elif square_clicked.is_activated:

                        # Если выбранным действием является движение
                        if selected_action == "move":

                            # Очищаем выделенные клетки доступные для движения
                            square_for_move = selected_piece.prepare_spell('move')
                            for cell in square_for_move:
                                cell.change_regime()

                            # Перемещаем фигуру
                            selected_piece.cast_spell('move', square_clicked)

                            # Указываем, что клетка на которой раньше стояла фигура, теперь не является выделенной
                            selected_piece.cell.deselect()

                            # Очищаем переменные с выделенными фигурой и действием
                            selected_piece = None
                            selected_action = None

                            # Закрываем интерфейс
                            interface.close()

                    # Тестовая часть управления фигурой

                    # Тут если зажата клавиша "M" и не выделена фигура для атаки
                    # Это выделение фигуры для последующего движения
                    if (isinstance(square_clicked.inner_piece, Piece)
                            and True in pg.key.get_pressed() and pg.key.get_pressed().index(True) == 16
                            and select_piece_for_cast is None):

                        piece = square_clicked.inner_piece

                        # Если был повторный клик по выделенной фигуре
                        if select_piece_for_move == piece:
                            # снимаем метку
                            select_piece_for_move = None
                            # И обратно закрашиваем клетки
                            square_for_move = piece.prepare_spell('move')
                            for cell in square_for_move:
                                cell.change_regime()

                        else:

                            # Если у нас уже была выделена клетка, а теперь попытка выделить другую - удаляем старую закраску
                            if not select_piece_for_move is None:
                                square_for_move = select_piece_for_move.prepare_spell('move')
                                for cell in square_for_move:
                                    cell.change_regime()

                            # ставим метку на фигуру и расскрашиваем область для движения
                            select_piece_for_move = piece
                            square_for_move = piece.prepare_spell('move')
                            for cell in square_for_move:
                                cell.change_regime()

                    # Тут если зажата клавиша "0" и не выделена фигура для движения
                    # Это выделение фигуры для последующей атаки
                    elif (isinstance(square_clicked.inner_piece, Piece)
                          and True in pg.key.get_pressed() and pg.key.get_pressed().index(True) == 39
                          and select_piece_for_move is None):

                        piece = square_clicked.inner_piece

                        # Если был повторный клик по выделенной фигуре
                        if select_piece_for_cast == piece:

                            # снимаем метку
                            select_piece_for_cast = None
                            # И обратно закрашиваем клетки
                            square_for_cast = piece.prepare_spell('attack')
                            for cell in square_for_cast:
                                cell.change_regime()

                        else:

                            # Если у нас уже была выделена клетка, а теперь попытка выделить другую - удаляем старую закраску
                            if not select_piece_for_cast is None:
                                square_for_cast = select_piece_for_cast.prepare_spell('attack')
                                for cell in square_for_cast:
                                    cell.change_regime()

                            # ставим метку на фигуру и расскрашиваем область для атаки
                            select_piece_for_cast = piece
                            square_for_cast = piece.prepare_spell('attack')
                            for cell in square_for_cast:
                                cell.change_regime()

                            # для удобства и наглядности, если целей для атаки нет - снимаем выделение
                            if not square_for_cast:
                                select_piece_for_cast = None

                    # если кликнули клетку с выделенной для перемещения фигурой
                    elif not select_piece_for_move is None:

                        # и она выделена
                        if square_clicked.is_activated:

                            # убираем выделение
                            square_for_move = select_piece_for_move.prepare_spell('move')
                            for cell in square_for_move:
                                cell.change_regime()

                            # Передвигаем
                            select_piece_for_move.cast_spell('move', square_clicked)

                            select_piece_for_move = None

                    # Если кликнули на клетку
                    elif not select_piece_for_cast is None and square_clicked.is_activated:

                        # убираем выделение
                        square_for_cast = piece.prepare_spell('attack')
                        for cell in square_for_cast:
                            cell.change_regime()

                        # и она выделена
                        select_piece_for_cast.cast_spell('attack', square_clicked)

                        select_piece_for_cast = None

                        # Пока что просто получаем в консоле результат

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
