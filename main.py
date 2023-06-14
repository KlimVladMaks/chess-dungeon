import pygame as pg
import typing as tp
from field import *
from piece import *
from enemy import *
from interface import *
from game import *
from menu import *

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


class GameProcess:
    """
    Класс для реализации основного игрового процесса
    """

    @staticmethod
    def start(screen: pg.Surface) -> str:
        """
        Функция для запуска основного игрового процесса.

        :param screen: Экран игры.
        :return: Строка результата игрового процесса.
        """

        # Абсолютные координаты экрана относительно карты уровня
        screen_absolute_coordinates = [0, 0]

        # Часы для регулировки FPS
        clock = pg.time.Clock()

        # Создаём поверхность, предназначенную для отображения игрового поля
        screen_field = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Устанавливаем фон
        background = pg.image.load("design/field/background.png")
        screen.blit(background, (0, 0))
        pg.display.update()

        # Создаём игровое меню
        game_menu = GameMenu(screen)

        # Создаём игровое поле
        field = Field(screen, screen_field, background, screen_absolute_coordinates, START_FIELD_MAP, game_menu)

        # Создаём интерфейс для управления фигурами
        interface = Interface(screen, field)

        # Создаём экземпляр класса для управления процессом игры
        game = Game(field)

        # Тест расположения фигуры
        piece_1 = Pawn('p1', game, field, field.get_square_by_pos(6, 6), 10, 0.7, 1, 3, 3, 4)
        piece_2 = Bishop('p1', game, field, field.get_square_by_pos(5, 5), 10, 0.7, 1, 3, 3, 4)
        piece_3 = Knight('p1', game, field, field.get_square_by_pos(5, 6), 10, 0.7, 1, 3, 3, 4)
        piece_4 = Rook('p1', game, field, field.get_square_by_pos(6, 5), 10, 0.7, 1, 3, 3, 4)
        piece_5 = Queen('p1', game, field, field.get_square_by_pos(4, 6), 10, 0.7, 1, 3, 3, 4)

        enemy_1 = EnemyPawn('Shodan', game, field, field.get_square_by_pos(15, 17), 10, 0.7, 1, 3, 3, 4)
        enemy_1.set_way_patrol(field.get_square_by_pos(8, 6))
        enemy_2 = EnemyRook('Shodan', game, field, field.get_square_by_pos(18, 19), 10, 0.7, 1, 3, 3, 4)
        enemy_2.set_way_patrol(field.get_square_by_pos(6, 19))
        enemy_3 = EnemyBishop('Shodan', game, field, field.get_square_by_pos(18, 17), 10, 0.7, 1, 3, 3, 4)
        enemy_3.set_way_patrol(field.get_square_by_pos(5, 17))
        enemy_4 = EnemyKing('Shodan', game, field, field.get_square_by_pos(18, 18), 10, 0.7, 1, 3, 3, 4)

        # Помещаем все фигуры в соответствующие списки
        game.player_pieces = [piece_1, piece_2, piece_3, piece_4, piece_5]
        game.computer_pieces = [enemy_1, enemy_2, enemy_3, enemy_4]

        for piece in game.player_pieces:
            piece.cell.add_inner_piece(piece)

        for piece in game.computer_pieces:
            piece.cell.add_inner_piece(piece)

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
                    raise SystemExit

                # Если нажата кнопка Enter
                elif e.type == pg.KEYDOWN and e.key == pg.K_RETURN:

                    # Завершаем текущий игровой такт
                    game.finish_game_tact()

                    # Закрываем интерфейс (если он вдруг открыт)
                    interface.close()

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

                    # Обновляем все клетки, на которых стоят фигуры игрока
                    for piece in game.player_pieces:
                        piece.cell.update()

                    # Обновляем поле
                    field.update()

                    # Проверяем игру на завершение и при необходимости возвращаем результат игрового процесса
                    match game.get_game_status():
                        case "lose":
                            return "lose_menu"
                        case "win":
                            return "win_menu"

                # Если нажата левая клавиша мыши
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:

                    # Получаем относительные координаты клика
                    click_coordinates = pg.mouse.get_pos()

                    # Если нажата кнопка открытия главного меню
                    if game_menu.is_open_button_clicked(click_coordinates):

                        # Запускаем игровое меню и получаем значение нажатой кнопки
                        game_menu.add_buttons(["continue_game", "restart", "main_menu"])
                        result = game_menu.start()

                        # Если нажата кнопка продолжения игры, то обновляем поле и переходим к следующей итерации
                        if result == "continue_game":
                            field.update()
                            continue

                        # Если нажата кнопка перезапуска игры, то возвращаем значение "demo"
                        # (Для повторного запуска игры)
                        if result == "restart":
                            return "demo"

                        # Если нажата кнопка выхода в главном меню, то возвращаем значение "main_menu"
                        if result == "main_menu":
                            return "main_menu"

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
                        # (Также отключает режим просмотра для всех видимых клеток)
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

                            # Проводим выбранное ранее действие
                            game.selected_piece.cast_spell(game.selected_spell, square_clicked)

                            # Удаляем фигуру из соответствующего списка, если она была уничтожена
                            game.del_destroyed_pieces()

                            # Обновляем состояние всех вражеских фигур
                            for piece in game.computer_pieces:
                                piece.cell.update()

                            # Обновляем все клетки, на которых стоят фигуры игрока
                            for piece in game.player_pieces:
                                piece.cell.update()

                            # Проверяем игру на завершение и при необходимости возвращаем результат игрового процесса
                            match game.get_game_status():
                                case "lose":
                                    return "lose_menu"
                                case "win":
                                    return "win_menu"

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

                # Если курсор движется
                elif e.type == pg.MOUSEMOTION:

                    # Получаем координаты курсора
                    mouse_pos = pg.mouse.get_pos()

                    # Если координаты попадают в область интерфейса
                    if interface.are_interface_coordinates(mouse_pos[0], mouse_pos[1]):

                        # Получаем кнопку над которой находится курсор
                        button = interface.get_button_by_coordinates(mouse_pos[0], mouse_pos[1])

                        # Если кнопка не равна None и нет выбранного действия
                        if button is not None and game.selected_spell is None:

                            # Извлекаем из кнопки способность
                            button_spell = button.spell

                            # Если курсор переведён с кнопки другой способности, то очищаем предыдущее выделение
                            if (game.viewed_spell is not None) and (button_spell.id != game.viewed_spell.id):
                                game.off_view_for_all_squares()

                            # Сохраняем новую просматриваемую способность
                            game.viewed_spell = button_spell

                            # Получаем список клеток из области действия способности
                            game.viewed_squares = button_spell.zone(game.selected_piece)

                            # Защита от None
                            if game.viewed_squares is None:
                                continue

                            # Делаем все полученные клетки просматриваемыми
                            for square in game.viewed_squares:
                                square.on_view()

                            # Обновляем игровое поле
                            game.field.update()

                            # Переходим к следующей итерации
                            continue

                        # Иначе отключаем режим просмотра для всех клеток
                        else:
                            game.off_view_for_all_squares()

                    # Иначе отключаем режим просмотра для всех клеток
                    else:
                        game.off_view_for_all_squares()


def main() -> None:
    """
    Main-функция.
    """

    # Инициализируем игру
    pg.init()

    # Создаём экран игры
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Задаём заголовок игры
    pg.display.set_caption("Chess Dungeon")

    # Создаём переменную для хранения того, какой окно сейчас следует открыть
    # (Изначально открываем главное меню)
    active_object = "main_menu"

    # Запускаем основной цикл приложения
    while True:

        # Запускаем главное меню
        if active_object == "main_menu":
            main_menu = MainMenu(screen)
            main_menu.add_buttons(["demo", "quit"])
            active_object = main_menu.start()

        # Запускаем демо игровой процесс
        elif (active_object == "demo") or (active_object == "restart"):
            active_object = GameProcess.start(screen)

        # Запускаем финальное меню при проигрыше
        elif active_object == "lose_menu":
            final_menu = FinalMenu(screen)
            final_menu.add_buttons(["quit", "restart", "main_menu"])
            active_object = final_menu.start(False)

        # Запускаем финальное меню при победе
        elif active_object == "win_menu":
            final_menu = FinalMenu(screen)
            final_menu.add_buttons(["quit", "restart", "main_menu"])
            active_object = final_menu.start(True)


# Запускаем Main-функцию
if __name__ == "__main__":
    main()
