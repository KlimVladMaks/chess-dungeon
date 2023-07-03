# Импорты библиотек
import pygame as pg
import typing as tp

# Импорты файлов
from level_editor.edit_field import EditSquare, EditButton, EditField
from level_editor.edit_interface import EditInterface
from level_editor.edit_controller import EditController

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
    def start(screen: pg.Surface) -> None:
        """
        Метод для запуска редактора уровней.

        :param screen: Экран игры.
        """

        # Абсолютные координаты экрана относительно карты уровня
        screen_absolute_coordinates = [0, 0]
        
        # Часы для регулировки FPS
        clock = pg.time.Clock()

        # Поверхность для отображения игрового поля
        screen_field = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Устанавливаем фон
        background = pg.image.load("design/level_editor/background.png")
        screen.blit(background, (0, 0))
        pg.display.update()

        # Создаём редактируемое игровое поле
        edit_field = EditField(screen, screen_field, background, screen_absolute_coordinates, INITIAL_FIELD_MAP)

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
                        continue

                    # Получаем кликнутый объект
                    clicked_object = edit_field.get_object_by_coordinates(click_coordinates[0], click_coordinates[1])

                    # Если кликнутого объекта нет, снимаем выделение с текущей выделенной клетки
                    if clicked_object is None:
                        edit_controller.deselect_square()

                    # Если клик пришёлся на кнопку редактирования поля
                    elif isinstance(clicked_object, EditButton):

                        # Снимаем выделение с текущей выделенной клетки
                        edit_controller.deselect_square()

                        # Получаем кликнутую кнопку
                        clicked_button = clicked_object
                        
                        # Если кликнута кнопка увеличения стороны поля
                        if clicked_button.button_type == "add":

                            # Увеличиваем соответствующую сторону и обновляем поле
                            edit_field.increase_side(clicked_button.side_type)
                            edit_field.update()

                            # Переходим к новой итерации цикла
                            continue

                        # Если кликнута кнопка уменьшения стороны поля
                        elif clicked_button.button_type == "delete":

                            # Уменьшаем соответствующую сторону и обновляем поле
                            edit_field.decrease_side(clicked_button.side_type)
                            edit_field.update()

                            # Переходим к новой итерации цикла
                            continue

                    # Если клик пришёлся на клетку поля
                    elif isinstance(clicked_object, EditSquare):
                        
                        # Получаем кликнутую клетку
                        clicked_square = clicked_object

                        # Если кликнутая клетка уже была выбрана ранее, то снимаем у неё выбранный режим
                        if clicked_square == edit_controller.selected_square:
                            edit_controller.deselect_square()
                            edit_field.update()
                            continue

                        # Если кликнутая клетка не была выбрана ранее, то переводим её в выбранный режим
                        elif clicked_square != edit_controller.selected_square:
                            edit_controller.select_square(clicked_square)
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


# Область для отладки
if __name__ == "__main__":
    pass
