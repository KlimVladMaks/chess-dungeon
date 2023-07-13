# Импорты библиотек
import pygame as pg
import typing as tp

# Импорты файлов
from level_editor.edit_field import EditSquare, EditButton, EditField
from level_editor.edit_interface import EditInterface
from level_editor.edit_controller import EditController
from level_editor.edit_menu import EditMenu, BASE_MENU_DICT
from saves import Save
from level_editor.edit_piece import EditPiece


# Импорт файлов для проверки типов
if tp.TYPE_CHECKING:
    from piece import Piece

# Ширина и высота экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Частота кадров
FPS = 60

# Начальная карта игрового поля
INITIAL_FIELD_MAP = [[1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1]]


class LevelEditor:
    """
    Класс для реализации редактора уровней.
    """

    @staticmethod
    def start(screen: pg.Surface) -> str:
        """
        Метод для запуска редактора уровней.

        :param screen: Экран игры.
        :return: Строка результата работы редактора уровней.
        """

        # Абсолютные координаты экрана относительно карты уровня
        screen_absolute_coordinates = [0, 0]

        # Часы для регулировки FPS
        clock = pg.time.Clock()

        # Поверхность для отображения игрового поля
        screen_field = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Устанавливаем фон
        background = pg.image.load("design/field/background.png")
        screen.blit(background, (0, 0))
        pg.display.update()

        # Создаём меню редактирования
        edit_menu = EditMenu(screen)

        # Создаём редактируемое игровое поле
        edit_field = EditField(screen, screen_field, background,
                               screen_absolute_coordinates, INITIAL_FIELD_MAP, edit_menu)

        # Создаём интерфейс редактирования
        edit_interface = EditInterface(screen, edit_field)

        # Создаём контроллер для управления редактором уровней
        edit_controller = EditController(edit_field, edit_interface)

        # Даём игровому полю доступ к контроллеру редактирования
        edit_field.edit_controller = edit_controller

        # Центрируем и отрисовываем игровое поле
        edit_field.center()
        edit_field.update()

        # Запускаем цикл работы редактора
        while True:

            # Регулируем FPS
            clock.tick(FPS)

            # Перебираем игровые события
            for e in pg.event.get():

                # При закрытии игрового окна завершаем программу
                if e.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit

                # Если нажата левая клавиша мыши
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:

                    # Получаем координаты клика
                    click_coordinates = pg.mouse.get_pos()

                    # Если клик пришёлся на интерфейс редактирования
                    if edit_interface.are_interface_coordinates(click_coordinates[0], click_coordinates[1]):

                        # Получаем кнопку, на которую пришёлся клик
                        button = edit_interface.get_button_by_coordinates(
                            click_coordinates[0], click_coordinates[1])

                        # Если клик не попал в кнопку, пропускаем итерацию
                        if button is None:
                            continue

                        # Если нажата кнопка установки обычной клетки, то делаем все выделенные клетки обычными клетками
                        elif button.button_type == "square":
                            for selected_square in edit_controller.selected_squares:
                                selected_square.set_square()
                            edit_field.update()
                            continue

                        # Если нажата кнопка установки барьера, то делаем все выделенные клетки барьерами
                        elif button.button_type == "barrier":
                            for selected_square in edit_controller.selected_squares:
                                selected_square.set_barrier()
                            edit_field.update()
                            continue

                        # Если нажата кнопка выбора белой фигуры, то открываем интерфейс выбора белых фигур
                        elif button.button_type == "white_piece":
                            edit_interface.open_white_pieces_interface()
                            continue

                        # Если нажата кнопка выбора чёрной фигуры, то открываем интерфейс выбора чёрных фигур
                        elif button.button_type == "black_piece":
                            edit_interface.open_black_pieces_interface()
                            continue

                        # При нажатии на кнопку "Назад", открываем базовый вариант интерфейса
                        elif button.button_type == "back":
                            edit_interface.open_base_interface()
                            continue

                        # Иначе размещаем не клетке выбранную фигуру
                        else:
                            for selected_square in edit_controller.selected_squares:
                                selected_square.square_type = button.button_type
                                selected_square.update()
                            edit_field.update()
                            continue

                    # Получаем кликнутый объект
                    clicked_object = edit_field.get_object_by_coordinates(click_coordinates[0], click_coordinates[1])

                    # Если кликнутого объекта нет
                    if clicked_object is None:

                        # Если нажата клавиша Ctrl, пропускаем итерацию
                        keys = pg.key.get_pressed()
                        if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:
                            continue

                        # Иначе снимаем выделение с текущих выделенных клеток
                        edit_controller.deselect_squares()
                        edit_field.update()

                    # Если клик пришёлся на кнопку открытия меню редактора уровней
                    elif isinstance(clicked_object, EditMenu):

                        # Запускаем игровое меню и получаем значение нажатой кнопки
                        edit_menu.add_buttons(BASE_MENU_DICT)
                        result = edit_menu.start()
                        
                        # Если нажата кнопка продолжения редактирования, то переходим к следующей итерации
                        if result == "continue":
                            edit_field.update()
                            continue

                        # Если нажата кнопка сохранения, то сохраняем уровень
                        elif result == "save":
                            LevelEditor.save(edit_field)
                            edit_field.update()
                            continue

                        # При нажатии кнопки выхода в главное меню, возвращаемся в главное меню
                        elif result == "main_menu":
                            return "main_menu"

                    # Если клик пришёлся на кнопку изменения размера поля поля
                    elif isinstance(clicked_object, EditButton):

                        # Снимаем выделение с текущей выделенной клетки
                        edit_controller.deselect_squares()

                        # Получаем кликнутую кнопку
                        clicked_button = clicked_object

                        # Если кликнута кнопка увеличения стороны поля
                        if clicked_button.button_type == "add":

                            # Увеличиваем соответствующую сторону и обновляем поле
                            edit_field.increase_side(clicked_button.side_type)
                            edit_field.update()

                        # Если кликнута кнопка уменьшения стороны поля
                        elif clicked_button.button_type == "delete":

                            # Уменьшаем соответствующую сторону и обновляем поле
                            edit_field.decrease_side(clicked_button.side_type)
                            edit_field.update()

                    # Если клик пришёлся на клетку поля
                    elif isinstance(clicked_object, EditSquare):

                        # Устанавливаем флаг множественного выделения клеток
                        edit_controller.is_multiple_selection = True

                        # Получаем кликнутую клетку
                        clicked_square = clicked_object

                        # Если нажата клавиша Ctrl
                        keys = pg.key.get_pressed()
                        if keys[pg.K_LCTRL] or keys[pg.K_RCTRL]:

                            # Если кликнутая клетка выбрана, то снимаем флаг массового выделения и ставим флаг
                            # массового снятия выделения с клеток
                            if clicked_square.is_selected:
                                edit_controller.is_multiple_selection = False
                                edit_controller.is_multiple_deselection = True

                            # Если кликнутая клетка выделена, то снимаем с неё выделение
                            if clicked_square.is_selected:
                                edit_controller.deselect_square(clicked_square)
                                edit_field.update()

                            # Если кликнутая клетка не выделена, то выделяем её
                            elif not clicked_square.is_selected:
                                edit_controller.select_square(clicked_square)
                                edit_field.update()

                        # Если клик пришёлся на единственную выбранную клетку
                        elif (len(edit_controller.selected_squares) == 1) and \
                                (edit_controller.selected_squares[0] == clicked_square):

                            # Снимаем выделение с ранее выделенной клетки
                            edit_controller.deselect_squares()
                            edit_field.update()

                            # Снимаем флаг множественного выделения клеток
                            edit_controller.is_multiple_selection = False

                        # Иначе
                        else:

                            # Снимаем выделение с ранее выделенных клеток и выделяем кликнутую клетку,
                            # не закрывая интерфейс
                            edit_controller.deselect_squares()
                            edit_controller.select_square(clicked_square)
                            edit_field.update()

                    # Актуализируем интерфейс
                    edit_controller.fix_interface()

                # Если отпущена левая клавиша мыши, то снимаем флаги множественного выделения
                # и снятия выделения с клеток
                elif e.type == pg.MOUSEBUTTONUP and e.button == 1:
                    edit_controller.is_multiple_selection = False
                    edit_controller.is_multiple_deselection = False

                # Если мышь движется с установленным флагом множественного выделения клеток
                elif e.type == pg.MOUSEMOTION and edit_controller.is_multiple_selection:

                    # Получаем текущие координаты мыши
                    mouse_pos = pg.mouse.get_pos()

                    # Если мышь наведена на интерфейс, то пропускаем итерацию
                    if edit_interface.are_interface_coordinates(mouse_pos[0], mouse_pos[1]):
                        continue

                    # Получаем объект, на который сейчас наведена мышь
                    pointed_object = edit_field.get_object_by_coordinates(
                        mouse_pos[0], mouse_pos[1])

                    # Если мышь наведена на клетку поля
                    if isinstance(pointed_object, EditSquare):

                        # Получаем клетку, на которую наведена мышь
                        pointed_square = pointed_object

                        # Если клетка ещё не выделена, то выделяем её
                        if not pointed_square.is_selected:
                            edit_controller.select_square(pointed_square)
                            edit_field.update()
                            continue

                # Если мышь движется с установленным флагом множественного снятия выделения с клеток
                elif e.type == pg.MOUSEMOTION and edit_controller.is_multiple_deselection:

                    # Получаем текущие координаты мыши
                    mouse_pos = pg.mouse.get_pos()

                    # Если мышь наведена на интерфейс, то пропускаем итерацию
                    if edit_interface.are_interface_coordinates(mouse_pos[0], mouse_pos[1]):
                        continue

                    # Получаем объект, на который сейчас наведена мышь
                    pointed_object = edit_field.get_object_by_coordinates(
                        mouse_pos[0], mouse_pos[1])

                    # Если мышь наведена на клетку поля
                    if isinstance(pointed_object, EditSquare):

                        # Получаем клетку, на которую наведена мышь
                        pointed_square = pointed_object

                        # Если клетка выделена, то снимаем с неё выделение
                        if pointed_square.is_selected:
                            edit_controller.deselect_square(pointed_square)
                            edit_field.update()
                            continue

                # Если нажата правая клавиша мыши, то ставим флаг движения карты и флаг для пропуска первого сдвига
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
                    edit_field.is_moving = True
                    edit_field.skip_first_move = True

                # Если отпущена правая клавиша мыши, то снимаем флаг движения карты и флаг пропуска первого сдвига
                elif e.type == pg.MOUSEBUTTONUP and e.button == 3:
                    edit_field.is_moving = False
                    edit_field.skip_first_move = False

                # Если мышь движется с установленным флагом движения карты
                elif e.type == pg.MOUSEMOTION and edit_field.is_moving:

                    # Находим сдвиг курсора по x и y
                    mouse_shift = pg.mouse.get_rel()
                    x_shift = mouse_shift[0]
                    y_shift = mouse_shift[1]

                    # Если у поля стоит флаг пропуска первого сдвига, то снимаем данный флаг и пропускаем итерацию
                    if edit_field.skip_first_move:
                        edit_field.skip_first_move = False
                        continue

                    # Сдвигаем игровое поле и обновляем его
                    edit_field.move(x_shift, y_shift)
                    edit_field.update()

    @staticmethod
    def save(edit_field: EditField) -> None:
        """
        Функция для сохранения уровня, созданного в редакторе уровней.

        :param edit_field: Игровое поле.
        """
        
        # Двойной список для хранения карты уровня
        field_map: list[list[int]] = []

        # Сложность уровня
        difficulty = 1

        # Словарь для хранения фигур из различных команд
        pieces: dict[str, list['EditPiece']] = {"white": [], "black": []}

        # Словарь для хранения королей различных команд
        kings: dict[str, 'EditPiece'] = {}

        #* Заполняем карту игрового поля
        # Перебираем все строки с клетками игрового поля
        for square_row_list in edit_field.squares_list:

            # Список для создания карты строки игрового поля
            field_map_row: list[int] = []

            # Перебираем все клетки из строки игрового поля
            for square in square_row_list:

                # Если клетка является барьером, записываем её как ноль
                if square.square_type == "barrier":
                    field_map_row.append(0)
                
                # Все остальные типы клеток записываем как единица
                else:
                    field_map_row.append(1)
            
            # Добавляем карту строки поля в общую карту поля
            field_map.append(field_map_row)

        #* Заполняем список фигур
        # Перебираем все клетки игрового поля
        for square_row_list in edit_field.squares_list:
            for square in square_row_list:
                
                # Если на клетке стоит белая или чёрная фигура
                if ("white" in square.square_type) or ("black" in square.square_type):
                    
                    # Получаем команду фигуры
                    team = square.square_type.split("_")[0]

                    # Получаем ранг фигуры
                    rang = square.square_type.split("_")[1]

                    # Если фигура является королём, добавляем её в словарь в качестве короля
                    if rang == "king":
                        kings[team] = EditPiece(team, square, rang)
                    
                    # Иначе добавляем фигуру в список обычных фигур
                    else:
                        pieces[team].append(EditPiece(team, square, rang))

        # Сохраняем данные уровня
        save = Save(field_map, difficulty, pieces, kings)
        save.save("edit_level")

# Область для отладки
if __name__ == "__main__":
    pass
