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
    background = pg.image.load("design/field/background.png")
    screen.blit(background, (0, 0))
    pg.display.update()

    # Создаём игровое поле
    field = Field(screen, screen_field, background, screen_absolute_coordinates, START_FIELD_MAP)

    # Создаём интерфейс для управления фигурами
    interface = Interface(screen, field)

    # Создаём экземпляр класса для управления процессом игры
    game = Game(field)

    # Тест расположения фигуры
    piece_1 = Pawn('p1', game, field, field.get_square_by_pos(5, 6), 10, 0.7, 1, 3, 3, 4)
    piece_2 = Pawn('p1', game, field, field.get_square_by_pos(6, 6), 10, 0.7, 1, 3, 3, 4)
    piece_3 = Pawn('p1', game, field, field.get_square_by_pos(5, 5), 10, 0.7, 1, 3, 3, 4)
    piece_4 = Pawn('p1', game, field, field.get_square_by_pos(6, 5), 10, 0.7, 1, 3, 3, 4)

    piece_1.cell.add_inner_piece(piece_1)
    piece_2.cell.add_inner_piece(piece_2)
    piece_3.cell.add_inner_piece(piece_3)
    piece_4.cell.add_inner_piece(piece_4)

    enemy_1 = EnemyPawn('Shodan', game, field, field.get_square_by_pos(15, 17), 10, 0.7, 1, 3, 3, 4)
    enemy_1.set_way_patrol(field.get_square_by_pos(8, 6))
    enemy_2 = EnemyPawn('Shodan', game, field, field.get_square_by_pos(18, 19), 10, 0.7, 1, 3, 3, 4)
    enemy_2.set_way_patrol(field.get_square_by_pos(6, 19))
    enemy_3 = EnemyPawn('Shodan', game, field, field.get_square_by_pos(18, 17), 10, 0.7, 1, 3, 3, 4)
    enemy_3.set_way_patrol(field.get_square_by_pos(5, 17))
    enemy_4 = EnemyKing('Shodan', game, field, field.get_square_by_pos(18, 18), 10, 0.7, 1, 3, 3, 4)

    enemy_1.cell.add_inner_piece(enemy_1)
    enemy_2.cell.add_inner_piece(enemy_2)
    enemy_3.cell.add_inner_piece(enemy_3)
    enemy_4.cell.add_inner_piece(enemy_4)

    # Помещаем все фигуры в соответствующие списки
    game.player_pieces = [piece_1, piece_2, piece_3, piece_4]
    game.computer_pieces = [enemy_1, enemy_2, enemy_3, enemy_4]

    # Формируем словарь с командами фигур
    game.pieces_teams[game.player_pieces[0].team] = game.player_pieces
    game.pieces_teams[game.computer_pieces[0].team] = game.computer_pieces

    # Сохраняем вражеского короля
    game.computer_king = enemy_4

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

                # Завершаем текущий игровой такт
                game.finish_game_tact()

                # TODO: Перенести механизм удаления уничтоженных фигур в класс Piece

                # Удаляем уничтоженные фигуры из соответсвующий списков
                game.del_destroyed_pieces()

                # Делаем новый ход для каждой фигуры игрока
                for piece in game.player_pieces:
                    piece.new_turn()

                # Удаляем уничтоженные фигуры из соответсвующий списков
                game.del_destroyed_pieces()

                # Делаем новый ход для каждой фигуры компьютера
                for piece in game.computer_pieces:
                    piece.new_turn()

                # Удаляем уничтоженные фигуры из соответсвующий списков
                game.del_destroyed_pieces()

                # Закрываем интерфейс (если он вдруг открыт)
                interface.close()

                # Обновляем все клетки, на которых стоят фигуры игрока
                for piece in game.player_pieces:
                    piece.cell.update()

                # Обновляем поле
                field.update()

                # Проверяем игру на завершение и при необходимости выводим финальную заставку
                match game.get_game_status():
                    case "lose":
                        set_final_screensaver(screen, False)
                        return
                    case "win":
                        set_final_screensaver(screen, True)
                        return

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

                    # Если ранее было какое-либо выбранное действие и оно не равно новому выбранному действию,
                    # то очищаем выделенные для него клетки
                    if (game.selected_spell is not None) and (game.selected_spell != button.spell):
                        game.clear_activated_squares()

                    # Изменяем режим для выбранного действия
                    game.toggle_action_mode(button.spell)

                    # Переходим к следующей итерации цикла
                    continue

                # Получаем нажатую клетку
                square_clicked = field.get_square_by_coordinates(click_coordinates[0], click_coordinates[1])

                # Если клетка относится к классу Square (т.е. существует)
                if isinstance(square_clicked, Square):

                    # Если нажатая клетка была выделена для определённого действия
                    if square_clicked.is_activated:

                        """Нужно быть осторожнее с добавлением новых действий, требующих другой обработки"""

                        # Очищаем ранее активированные клетки
                        game.clear_activated_squares()
                        game.selected_piece.cell.deselect()

                        # Проводим выбранное ранее действие над выбранной фигуру
                        game.selected_piece.cast_spell(game.selected_spell, square_clicked)

                        # Удаляем фигуру из соответствующего списка, если она была уничтожена
                        game.del_destroyed_pieces()

                        # Проверяем игру на завершение и при необходимости выводим финальную заставку
                        match game.get_game_status():
                            case "lose":
                                set_final_screensaver(screen, False)
                                return
                            case "win":
                                set_final_screensaver(screen, True)
                                return

                        # Активируем клетку, на которой теперь стоит фигура
                        game.selected_piece.cell.select()

                        # Убираем прошлое выбранное действие
                        game.selected_spell = None

                        # Обновляем интерфейс с учётом новых способностей
                        interface.buttons_group.empty()
                        interface.add_buttons(game.selected_piece.spell_list, game.selected_piece)
                        interface.open()

                        # Если HP выбранной фигуры упало до нуля
                        if game.selected_piece.hp <= 0:

                            # Закрываем интерфейс, убираем выделение с клетки, убираем выделенную фигуру
                            interface.close()
                            game.selected_piece.cell.deselect()
                            game.selected_piece = None

                    # Если на клетке находится ранее не выбранная фигура
                    elif isinstance(square_clicked.inner_piece, Piece) and (
                            square_clicked.inner_piece != game.selected_piece):

                        # Если уже есть выбранное действие, то пропускаем итерацию
                        if game.selected_spell is not None:
                            continue

                        # Если игрок нажал на вражескую фигуру, то пропускаем итерацию
                        if square_clicked.inner_piece.team == "Shodan":
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
                        spell_list = [spell for spell in game.selected_piece.spell_list]

                        # Задаём новые кнопки с действиями, используя список со способностями выбранной фигуры
                        interface.add_buttons(spell_list, game.selected_piece)

                        # Открываем интерфейс
                        interface.open()

                    # Если на клетке находится ранее выбранная фигура
                    elif isinstance(square_clicked.inner_piece, Piece) \
                            and square_clicked.inner_piece == game.selected_piece:

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


def set_final_screensaver(screen: pg.Surface, is_player_win: bool) -> None:
    """
    Функция для установки финальной заставки игры.

    :param screen: Экран игры.
    :param is_player_win: Флаг, показывающий, выиграл ли игрок.
    """

    # Часы для регулировки FPS
    clock = pg.time.Clock()

    # Выбираем заставку экрана в зависимости от результата игры
    if is_player_win:
        screensaver = pg.image.load("design/screensaver/win_screen.png")
    else:
        screensaver = pg.image.load("design/screensaver/lose_screen.png")

    # Устанавливаем финальную заставку на экран игры
    screen.blit(screensaver, (0, 0))
    pg.display.update()

    # Запускаем бесконечный цикл
    while True:

        # Регулируем FPS
        clock.tick(FPS)

        # Перебираем возникшие игровые события
        for e in pg.event.get():

            # При закрытии игрового окна завершаем программу
            if e.type == pg.QUIT:
                pg.quit()
                return


# Запускаем Main-функцию
if __name__ == "__main__":
    main()
