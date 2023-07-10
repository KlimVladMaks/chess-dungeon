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

# Размеры кнопок интерфейса в формате (ширина, высота)
EDIT_BUTTON_SIZE = (70, 70)

# Расстояние между кнопками интерфейса
EDIT_BUTTON_SPACING = 20

# Список с базовыми типами для кнопок интерфейса
EDIT_INTERFACE_BASE_LIST = ["square", "barrier", "white_piece", "black_piece"]

# Список с типами белых фигур для кнопок интерфейса
EDIT_INTERFACE_WHITE_PIECES_LIST = ["white_pawn", "white_knight", "white_bishop", 
                                    "white_rook", "white_queen", "back"]

# Список с типами чёрных фигур для кнопок интерфейса
EDIT_INTERFACE_BLACK_PIECES_LIST = ["black_pawn", "black_knight", "black_bishop",
                                    "black_rook", "black_queen", "black_king", "back"]


class EditInterfaceButton(pg.sprite.Sprite):
    """
    Класс для реализации кнопки интерфейса редактирования.
    """
    
    def __init__(self, coordinates: tuple[int, int], button_size: tuple[int, int], button_type: str) -> None:
        """
        Функция для инициализации кнопки.

        :param coordinates: Координаты кнопки в формате (x, y).
        :param button_size: Размеры кнопки в формате (ширина, высота).
        :param button_type: Тип кнопки.
        """
        
        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем тип кнопки
        self.button_type = button_type

        # Задаём поверхность кнопки
        self.image = pg.Surface((button_size[0], button_size[1]))

        # Задаём область кнопки
        self.rect = pg.Rect(coordinates[0], coordinates[1], button_size[0], button_size[1])

        # Обновляем состояние кнопки
        self.update()

    def update(self) -> None:
        """
        Функция для обновления состояния кнопки.
        """
        
        # Задаём изображение кнопки, отлавливая ошибки
        try:
            self.image = pg.image.load(f"./design/level_editor/edit_interface/{self.button_type}_button.png")
        except:
            pass


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

        # Группа для хранения кнопок интерфейса
        self.button_group = pg.sprite.Group()

    def open(self) -> None:
        """
        Функция для открытия интерфейса редактирования.
        """
        
        # Уменьшаем размер экрана игрового поля на величину интерфейса
        self.field.screen_field = pg.Surface((self.screen.get_width(), 
                                              self.screen.get_height() - EDIT_INTERFACE_HEIGHT))
        
        # Закрашиваем поверхность интерфейса
        self.image.fill(EDIT_INTERFACE_BACKGROUND_COLOR)

        # Отрисовываем интерфейс на экране вместе с кнопками
        self.button_group.draw(self.image)
        self.screen.blit(self.image, self.rect)
        pg.display.update()

        # Указываем, что интерфейс открыт
        self.is_open = True

    def open_base_interface(self) -> None:
        """
        Функция для открытия базового варианта интерфейса.
        """
        
        # Открываем интерфейс с базовым набором кнопок
        self.add_buttons(EDIT_INTERFACE_BASE_LIST)
        self.open()

    def open_white_pieces_interface(self) -> None:
        """
        Функция для открытия интерфейса выбора белых фигур.
        """
        
        # Открываем интерфейс с кнопками выбора белых фигур
        self.add_buttons(EDIT_INTERFACE_WHITE_PIECES_LIST)
        self.open()

    def open_black_pieces_interface(self) -> None:
        """
        Функция для открытия интерфейса выбора чёрных фигур.
        """
        
        # Открываем интерфейс с кнопками выбора чёрных фигур
        self.add_buttons(EDIT_INTERFACE_BLACK_PIECES_LIST)
        self.open()

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

    def add_buttons(self, button_types_list: list[str]) -> None:
        """
        Функция для добавления кнопок в интерфейс.

        :param button_types_list: Список с типами кнопок.
        """

        # Очищаем группу от предыдущего набора кнопок
        self.button_group.empty()

        # Задаём координаты для первой кнопки
        x = EDIT_BUTTON_SPACING
        y = (self.image.get_height() // 2) - (EDIT_BUTTON_SIZE[1] // 2)
        
        # Перебираем все типы кнопок и создаём соответствующие кнопки
        for button_type in button_types_list:
            button = EditInterfaceButton((x, y), EDIT_BUTTON_SIZE, button_type)
            self.button_group.add(button)
            x += EDIT_BUTTON_SIZE[0] + EDIT_BUTTON_SPACING

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[EditInterfaceButton, None]:
        """
        Функция для получения кнопки интерфейса по координатам.

        :param x: Координата x.
        :param y: Координата y.
        :return: Искомая кнопка или None, если кнопки с заданными координатами не найдено.
        """
        
        # Если интерфейс закрыт, возвращаем None
        if not self.is_open:
            return None
        
        # Рассчитываем координаты кнопки на поверхности интерфейса
        x_interface = x
        y_interface = y - self.field.screen_field.get_height()

        # Перебираем все кнопки из группы кнопок интерфейса
        for button in self.button_group:
            
            # Если координаты попадают в область кнопки, то возвращаем эту кнопку
            if button.rect.collidepoint(x_interface, y_interface):
                return button
        
        # Иначе возвращаем None
        return None


# Область для отладки
if __name__ == "__main__":
    pass
