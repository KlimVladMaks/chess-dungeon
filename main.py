import pygame as pg
import typing as tp
from field import *
from piece import *
from enemy import *
from interface import *
from game import *

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

    # Создаём экземпляр класса для управления процессом игры
    game = Game(field)

    # Тест расположения фигуры
    first_piece = Pawn('p1', field, field.get_square_by_pos(6, 6), 10, 0.5, 2, 3, 1)
    second_piece = Pawn('p1', field, field.get_square_by_pos(5, 6), 10, 0.5, 2, 3, 1)
    first_piece.cell.add_inner_piece(first_piece)
    second_piece.cell.add_inner_piece(second_piece)

    enemy = EnemyPawn('Shodan', field, field.get_square_by_pos(15, 17), 10, 0.5, 2, 3, 5)
    enemy.set_way_patrol(field.get_square_by_pos(7, 6))
    enemy.cell.add_inner_piece(enemy)

    # Помещаем все фигуры в список
    pieces = [first_piece, second_piece, enemy]

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

            # Если нажата кнопка Enter
            elif e.type == pg.KEYDOWN and e.key == pg.K_RETURN:

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

                        # Если ранее было какое-либо выбранное действие и это не движение,
                        # то очищаем выделенные для него клетки
                        if (game.selected_action is not None) and (game.selected_action != "move"):
                            game.clear_activated_squares()

                        # Изменяем режим движения для выбранной фигуры
                        # (Выбранное действие обновляется автоматически)
                        game.toggle_move_mode()

                    # Если выбрана кнопка атаки
                    elif button.action == "attack":

                        # Если ранее было какое-либо выбранное действие и это не атака,
                        # то очищаем выделенные для него клетки
                        if (game.selected_action is not None) and (game.selected_action != "attack"):
                            game.clear_activated_squares()

                        # Изменяем режим атаки для выбранной фигуры
                        # (Выбранное действие обновляется автоматически)
                        game.toggle_attack_mode()

                    # Переходим к следующей итерации цикла
                    continue

                # Получаем нажатую клетку
                square_clicked = field.get_square_by_coordinates(click_coordinates[0], click_coordinates[1])

                # Если клетка относится к классу Square (т.е. существует)
                if isinstance(square_clicked, Square):

                    # Если на клетке стоит фигура, выделенная для действия, направленного на неё
                    if isinstance(square_clicked.inner_piece, Piece) and square_clicked.is_activated:

                        # Если выбрано действие атаки
                        if game.selected_action == "attack":

                            # Очищаем ранее активированные клетки
                            game.clear_activated_squares()

                            # Атакуем выбранную фигуру
                            game.selected_piece.cast_spell('attack', square_clicked)

                            # Завершаем игровой такт
                            game.finish_game_tact()

                            # Закрываем интерфейс
                            interface.close()

                    # Если на клетке находится ранее не выбранная фигура
                    elif isinstance(square_clicked.inner_piece, Piece) and (
                            square_clicked.inner_piece != game.selected_piece):

                        # Если уже есть выбранное действие, то пропускаем итерацию
                        if game.selected_action is not None:
                            continue

                        # Если игрок нажал на вражескую фигуру, то пропускаем итерацию
                        if "Enemy" in type(square_clicked.inner_piece).__name__:
                            continue

                        # Если существовала ранее выбранная фигура, то завершаем предыдущий игровой такт
                        if game.selected_piece is not None:
                            game.finish_game_tact()

                        # Сохраняем выбранную фигуру
                        game.selected_piece = square_clicked.inner_piece

                        # Выделяем клетку, на которой стоит выбранная фигура
                        game.selected_piece.cell.select()

                        # Очищаем группу со старыми кнопками
                        interface.buttons_group.empty()

                        # Получаем список способностей выбранной фигуры
                        spell_list = [spell.id for spell in game.selected_piece.spell_list]

                        # Задаём новые кнопки с действиями, используя список со способностями выбранной фигуры
                        interface.add_buttons(spell_list)

                        # Открываем интерфейс
                        interface.open()

                    # Если на клетке находится ранее выбранная фигура
                    elif isinstance(square_clicked.inner_piece, Piece) \
                            and square_clicked.inner_piece == game.selected_piece:

                        # Завершаем игровой такт
                        game.finish_game_tact()

                        # Закрываем интерфейс
                        interface.close()

                    # Если нажатая клетка была выделена для определённого действия (не связанного с другими фигурами)
                    elif square_clicked.is_activated:

                        # Если выбранным действием является движение
                        if game.selected_action == "move":

                            # Очищаем ранее активированные клетки
                            game.clear_activated_squares()

                            # Снимаем выделение с клетки, на которой раньше стояла фигура
                            game.selected_piece.cell.deselect()

                            # Перемещаем фигуру
                            game.selected_piece.cast_spell('move', square_clicked)

                            # Завершаем игровой такт
                            game.finish_game_tact()

                            # Закрываем интерфейс
                            interface.close()

                    # Обновляем поле
                    field.update()

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