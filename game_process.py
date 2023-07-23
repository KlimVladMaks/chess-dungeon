# Импорты библиотек
import pygame as pg
import typing as tp

# Импорты файлов
from field import *
from piece import *
from enemy import *
from interface import *
from game import *
from menu import *
from king_square import *
from saves import Save

# Ширина и высота экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Частота кадров
FPS = 60


class GameProcess:
    """
    Класс для реализации основного игрового процесса
    """

    @staticmethod
    def start(save: Save, screen: pg.Surface) -> str:

        #Загружаем игру из файла
        """
        Функция для запуска основного игрового процесса из файла.

        :param screen: Экран игры.
        :param save: Объект сохранения.
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
        field = Field(screen, screen_field, background, screen_absolute_coordinates, save.field_map, game_menu)

        # Создаём интерфейс для управления фигурами
        interface = Interface(screen, field)

        # Создаём экземпляр класса для управления процессом игры
        game = Game(field)

        for piece in save.pieces:
            team = piece["team"]
            cell_row = piece["cell"][0]
            cell_col = piece["cell"][1]
            cell = field.get_square_by_pos(cell_row, cell_col)

            game.pieces_teams.setdefault(team, [])
            if piece["controller"] == "player":
                if piece["rang"] == "pawn":
                    pack_piece = Pawn(team, game, field, cell)
                elif piece["rang"] == "bishop":
                    pack_piece = Bishop(team, game, field, cell)
                elif piece["rang"] == "knight":
                    pack_piece = Knight(team, game, field, cell)
                elif piece["rang"] == "rook":
                    pack_piece = Rook(team, game, field, cell)
                elif piece["rang"] == "queen":
                    pack_piece = Queen(team, game, field, cell)

            elif piece["controller"] == "comp":
                if piece["rang"] == "pawn":
                    pack_piece = EnemyPawn(team, game, field, cell, save.difficulty)
                elif piece["rang"] == "bishop":
                    pack_piece = EnemyBishop(team, game, field, cell, save.difficulty)
                elif piece["rang"] == "knight":
                    pack_piece = EnemyKnight(team, game, field, cell, save.difficulty)
                elif piece["rang"] == "rook":
                    pack_piece = EnemyRook(team, game, field, cell, save.difficulty)
                elif piece["rang"] == "queen":
                    pack_piece = EnemyQueen(team, game, field, cell, save.difficulty)
                for cell in piece["way_patrol"]:
                    pack_piece.way_patrol.append(field.get_square_by_pos(cell[0], cell[1]))
                pack_piece.pos_patrol = piece["pos_patrol"]
                pack_piece.action = piece["action"]

            pack_piece.hp = piece["hp"]
            pack_piece.AP = piece["AP"]
            pack_piece.shield = piece["shield"]
            pack_piece.active_turn = piece["active_turn"]
            pack_piece.max_hp = piece["max_hp"]
            pack_piece.accuracy = piece["accuracy"]
            pack_piece.min_damage = piece["min_damage"]
            pack_piece.max_damage = piece["max_damage"]
            pack_piece.radius_move = piece["radius_move"]
            pack_piece.radius_fov = piece["radius_fov"]
            pack_piece.effect_list: list["Effect"] = []
            for effect in piece["effect_list"]:
                pack_piece.give_effect(Effect.give_effect_by_id(effect["id"], effect["timer"], effect["strength"]))
            pack_piece.spell_list: list["Spell"] = []
            for spell in piece["spell_list"]:
                pack_piece.spell_list.append(Spell.give_object_by_id(spell["id"]))
                pack_piece.spell_list[-1].cooldown_now = spell["cooldown_now"]

            game.pieces_teams[team].append(pack_piece)

        for piece in save.kings:
            team = piece["team"]
            if piece["cell"] is None:
                cell = None
            else:
                cell_row = piece["cell"][0]
                cell_col = piece["cell"][1]
                cell = field.get_square_by_pos(cell_row, cell_col)

            if piece["controller"] == "player":
                pack_piece = King(team, game, field, cell)
            elif piece["controller"] == "comp":
                pack_piece = EnemyKing(team, game, field, cell, save.difficulty)
                game.pieces_teams[team].append(pack_piece)

            pack_piece.hp = piece["hp"]
            pack_piece.AP = piece["AP"]
            pack_piece.shield = piece["shield"]
            pack_piece.active_turn = piece["active_turn"]
            pack_piece.max_hp = piece["max_hp"]
            pack_piece.accuracy = piece["accuracy"]
            pack_piece.min_damage = piece["min_damage"]
            pack_piece.max_damage = piece["max_damage"]
            pack_piece.radius_move = piece["radius_move"]
            pack_piece.radius_fov = piece["radius_fov"]
            pack_piece.effect_list: list["Effect"] = []
            for effect in piece["effect_list"]:
                pack_piece.give_effect(Effect.give_effect_by_id(effect["id"], effect["timer"], effect["strength"]))
            pack_piece.spell_list: list["Spell"] = []
            for spell in piece["spell_list"]:
                pack_piece.spell_list.append(Spell.give_object_by_id(spell["id"]))
                pack_piece.spell_list[-1].cooldown_now = spell["cooldown_now"]

            game.kings_teams[team] = pack_piece

        '''
        Часть для адаптации к текущей версии
        '''

        player_king = game.kings_teams['white']
        king_square = KingSquare(field, player_king)
        player_king.cell = king_square
        field.king_square = king_square

        # Сохраняем вражеского короля
        game.computer_king = game.kings_teams['black']

        # Делаем первую команду активной
        game.active_team = list(game.kings_teams.keys())[0]

        # Помещаем все фигуры в соответствующие списки
        for team in game.pieces_teams:
            for piece in game.pieces_teams[team]:
                piece.cell.add_inner_piece(piece)

        # И не забываем королей!
        for king in game.kings_teams.values():
            if king.controller == 'comp':
                king.cell.add_inner_piece(king)

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

                    # Прежде чем поменять активную команду, нужно убедиться не уничтожена ли предыдущая
                    # поскольку для определения следующей в списке команд должна остаться предыдущая
                    # такое возможно, если игрок последней пешкой использует "Просто пешка"
                    
                    # Заводим флаг
                    delete_previor_team = False

                    # Убеждаемся, что прошлая команда - игрока и она уничтожена
                    if (game.kings_teams[game.active_team].controller == "player"
                        and len(game.pieces_teams[game.active_team]) == 0):
                        # меняем состояние флага
                        delete_previor_team = True
                        # сохраняем команду
                        previor_team = game.active_team

                    # Делаем все фигуры старой команды неактивными
                    for piece in game.pieces_teams[game.active_team]:
                        piece.active_turn = False
                        piece.cell.update()

                    # Сдвигаем команду на следующую
                    game.next_team()

                    # удаляем короля из списка
                    if delete_previor_team:
                        game.del_king(game.kings_teams[previor_team])

                    # Очищаем все просматриваемые клетки
                    game.off_view_for_all_squares()

                    # Завершаем текущий игровой такт
                    game.finish_game_tact()

                    # Закрываем интерфейс (если он вдруг открыт)
                    interface.close()

                    # Делаем новый ход для каждой фигуры активной команды
                    for piece in game.pieces_teams[game.active_team]:
                        piece.new_turn()
                    
                    # Делаем новый ход для короля активной команды
                    game.kings_teams[game.active_team].new_turn()

                    # Обновляем состояние всех фигур
                    for team in game.pieces_teams:
                        for piece in game.pieces_teams[team]:
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

                            # Очищаем все просматриваемые клетки
                            game.off_view_for_all_squares()

                            # Очищаем ранее активированные клетки
                            game.clear_activated_squares()
                            game.selected_piece.cell.deselect()

                            # Проводим выбранное ранее действие
                            game.selected_piece.cast_spell(game.selected_spell, square_clicked)

                            # Обновляем состояние всех фигур
                            for team in game.pieces_teams:
                                for piece in game.pieces_teams[team]:
                                    piece.cell.update()

                            print('Hi')

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

                            # Если игрок нажал на фигуру компьютера, то пропускаем итерацию
                            if square_clicked.inner_piece.controller == "comp":
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

                    # Получаем квадрат, на котором находится курсор
                    view_square = field.get_square_by_coordinates(mouse_pos[0], mouse_pos[1])

                    # Если координаты попадают в область интерфейса
                    if interface.are_interface_coordinates(mouse_pos[0], mouse_pos[1]):

                        # Получаем кнопку над которой находится курсор
                        button = interface.get_button_by_coordinates(mouse_pos[0], mouse_pos[1])

                        # Если кнопка не равна None
                        if button is not None:

                            # Извлекаем из кнопки способность
                            button_spell = button.spell

                            # Если курсор переведён с кнопки другой способности, то очищаем предыдущее выделение
                            if (game.viewed_spell is not None) and (button_spell.id != game.viewed_spell.id):
                                game.off_view_for_all_squares()

                                # Очищаем интерфейс от текста
                                interface.show()
                            
                            # Сохраняем новую просматриваемую способность
                            game.viewed_spell = button_spell

                            # Получаем список клеток из области действия способности
                            game.viewed_squares = button_spell.zone(game.selected_piece)

                            # Выводим описание способности в интерфейсе
                            interface.add_text(button_spell.description)

                            # Если нет выбранного действия
                            if game.selected_spell is None:

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

                            # Очищаем интерфейс от текста
                            interface.show()

                    # Если клетка, на которую наведён курсор существует и активна
                    elif (view_square is not None) and (view_square.is_activated):

                        # Получаем область клеток на которые распространяется выбранная способность
                        squares_area = game.selected_spell.give_area_of_attack(game.selected_piece, view_square)

                        # Если способность не наносит эффект по области
                        if squares_area is None:
                            
                            # Выделяем клетку как просматриваемую
                            view_square.on_view()

                            # Если просматриваемая клетка не является базовой просматриваемой клеткой
                            if view_square != game.base_viewed_square:

                                # Очищаем все предыдущие просматриваемые клетки
                                game.off_view_for_all_squares()

                                # Делаем новую клетку базовой и просматриваемой
                                game.base_viewed_square = view_square
                                game.viewed_squares = [view_square]

                        # Иначе
                        else:

                            # Выделяем стартовую клетку как просматриваемую
                            view_square.on_view()

                            # Выделяем для просмотра все клетки из полученной области
                            for square in squares_area:
                                square.on_view()
                            
                            # Если просматриваемая клетка не является базовой просматриваемой клеткой
                            if view_square != game.base_viewed_square:

                                # Очищаем все предыдущие просматриваемые клетки
                                game.off_view_for_all_squares()

                                # Делаем новую клетку базовой и просматриваемой, а также обновляем список 
                                # просматриваемых клеток
                                game.base_viewed_square = view_square
                                game.viewed_squares = squares_area
                                game.viewed_squares.append(view_square)

                        # Обновляем игровое поле
                        game.field.update()

                    # Иначе отключаем режим просмотра для всех клеток
                    else:
                        game.off_view_for_all_squares()

                        # Если интерфейс открыт, очищаем его от текста
                        if interface.is_open:
                            interface.show()
