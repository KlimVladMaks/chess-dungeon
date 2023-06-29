# Импорты библиотек
import pygame as pg

# Импорты файлов
from field import EditField

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
        background = pg.image.load("design/field/background.png")
        screen.blit(background, (0, 0))
        pg.display.update()

        # Создаём редактируемое игровое поле
        edit_field = EditField(screen, screen_field, background, screen_absolute_coordinates, INITIAL_FIELD_MAP)

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
