# Импорты библиотек
import pygame as pg
import typing as tp

# Импорт файлов для задания типов
if tp.TYPE_CHECKING:
    from level_editor.edit_field import EditField

# Высота интерфейса
EDIT_INTERFACE_HEIGHT = 100

# Цвет фона интерфейса
EDIT_INTERFACE_BACKGROUND_COLOR = (128, 128, 128)


class EditInterfaceButton(pg.sprite.Sprite):
    """
    Класс для реализации кнопки интерфейса редактирования.
    """
    
    def __init__(self, coordinates: tuple[int, int], button_size: tuple[int, int]) -> None:
        """
        Функция для инициализации кнопки.

        :param coordinates: Координаты кнопки в формате (x, y).
        :param button_size: Размеры кнопки в формате (ширина, высота).
        """
        
        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Задаём поверхность кнопки
        self.image = pg.Surface((button_size[0], button_size[1]))

        # Задаём область кнопки
        self.rect = pg.Rect(coordinates[0], coordinates[1], button_size[0], button_size[1])


class EditInterface(pg.sprite.Sprite):
    """
    Класс для реализации интерфейса редактирования.
    """
    
    def __init__(self, screen: pg.Surface, field: 'EditField') -> None:
        """
        Функция для инициализации интерфейса редактирования.

        :param screen: Экран игры.
        :param field: Игровое поле.
        :param edit_controller: Контроллер редактирования.
        """
        
        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем экран игры
        self.screen = screen

        # Сохраняем игровое поле
        self.field = field

        # Задаём поверхность интерфейса и закрашиваем её в соответствующий цвет
        self.image = pg.Surface((self.screen.get_width(), EDIT_INTERFACE_HEIGHT))
        self.image.fill(EDIT_INTERFACE_BACKGROUND_COLOR)

        # Задаём область интерфейса
        self.rect = pg.Rect(0, self.screen.get_height() - EDIT_INTERFACE_HEIGHT, 
                            self.screen.get_width(), EDIT_INTERFACE_HEIGHT)
        
        # Флаг, показывающий, открыт ли интерфейс
        self.is_open = False

    def open(self) -> None:
        """
        Функция для открытия интерфейса редактирования.
        """
        
        # Уменьшаем размер экрана игрового поля на величину интерфейса
        self.field.screen_field = pg.Surface((self.screen.get_width(), 
                                              self.screen.get_height() - EDIT_INTERFACE_HEIGHT))
        
        # Отрисовываем интерфейс на экране
        self.screen.blit(self.image, self.rect)
        pg.display.update()

        # Указываем, что интерфейс открыт
        self.is_open = True

    def close(self) -> None:
        """
        Функция для закрытия интерфейса редактирования.
        """

        # Расширяем поверхность игрового поля до полного экрана игры и обновляем экран игры
        self.field.screen_field = pg.Surface((self.screen.get_width(), self.screen.get_height()))
        self.field.update()
        pg.display.update()
        
        # Указываем, что интерфейс закрыт
        self.is_open = False

    def toggle(self) -> None:
        """
        Функция для переключения состояния интерфейса редактирования.
        (Если интерфейс был открыт - закрывает, если закрыт - открывает).
        """
        
        # Если интерфейс открыт, то закрываем его, иначе открываем
        if self.is_open:
            self.close()
        else:
            self.open()

    def are_interface_coordinates(self, x: int, y: int) -> bool:
        """
        Функция, проверяющая, попадают ли переданные координаты в область интерфейса.

        :param x: Координата x.
        :param y: Координата y.
        :return: True - если попадают, False - если нет.
        """

        # Если интерфейс закрыт, возвращаем False
        if not self.is_open:
            return False

        # Если координаты попадают в область интерфейса, возвращаем True
        if self.rect.collidepoint(x, y):
            return True

        # Иначе возвращаем False
        else:
            return False


# Область для отладки
if __name__ == "__main__":
    pass
