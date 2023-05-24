import typing as tp
import pygame as pg

# Высота интерфейса
INTERFACE_HEIGHT = 100

# Цвет фона интерфейса
INTERFACE_BACKGROUND_COLOR = "#BBBBBB"

# Цвет кнопки для движения фигуры
MOVE_BUTTON_COLOR = "#008000"

# Цвет кнопки для атаки другой фигуры
ATTACK_BUTTON_COLOR = "#FF0000"

# Расстояние между кнопками интерфейса
BUTTON_SPACING = 20

# Размеры кнопок интерфейса в формате (ширина, высота)
BUTTON_SIZE = (70, 70)


class _Field:
    """
    Фиктивный класс игрового поля.
    """
    pass


class Button(pg.sprite.Sprite):
    """
    Класс для реализации кнопки.
    """

    def __init__(self, action: str, coordinates: tuple[int, int], button_size: tuple[int, int]) -> None:
        """
        Функция для инициализации кнопки.

        :param coordinates: Координаты кнопки.
        :param action: Тип действия, реализуемого кнопкой (move - движение, attack - атака).
        :param button_size: Размеры кнопки в формате (ширина, высота).
        """

        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем тип действия, реализуемого кнопкой
        self.action = action

        # Задаём поверхность кнопки
        self.image = pg.Surface((button_size[0], button_size[1]))

        # Задаём изображение поверхности кнопки в соответствии с типом действия кнопки
        if self.action == "move":
            self.image = pg.image.load("design/move_button.png")
        elif self.action == "attack":
            self.image = pg.image.load("design/attack_button.png")

        # Задаём поверхность кнопки
        self.rect = pg.Rect(coordinates[0], coordinates[1], button_size[0], button_size[1])


class Interface(pg.sprite.Sprite):
    """
    Класс для реализации интерфейса управления фигурами.
    (Класс реализован на основе спрайта).
    """

    def __init__(self, screen: pg.Surface, field: _Field) -> None:
        """
        Функция для инициализации интерфейса.

        :param screen: Экран игры.
        :param field: Игровое поле.
        """

        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем экран игры
        self.screen = screen

        # Сохраняем игровое поле
        self.field = field

        # Создаём группу для хранения спрайтов кнопок интерфейса
        self.buttons_group = pg.sprite.Group()

        # Задаём поверхность интерфейса и закрашиваем её в соответсвующий цвет
        self.image = pg.Surface((self.screen.get_width(), INTERFACE_HEIGHT))
        self.image.fill(INTERFACE_BACKGROUND_COLOR)

        # Задаём область интерфейса
        self.rect = pg.Rect(0, self.screen.get_height() - INTERFACE_HEIGHT, self.screen.get_width(), INTERFACE_HEIGHT)

        # Флаг, показывающий, открыт ли интерфейс
        self.is_open = False

    def show(self) -> None:
        """
        Функция для вывода интерфейса на экран.
        """

        # Отрисовываем кнопки интерфейса
        self.buttons_group.draw(self.image)

        # Отрисовываем интерфейс на экране
        self.screen.blit(self.image, self.rect)
        pg.display.update()

    def open(self) -> None:
        """
        Функция для открытия интерфейса.
        """

        # Уменьшаем размер экрана игрового поля на величину интерфейса
        self.field.screen_field = pg.Surface((self.screen.get_width(), self.screen.get_height() - INTERFACE_HEIGHT))

        # Отрисовываем интерфейс
        self.show()

        # Ставим флаг, что игровое поле открыто
        self.is_open = True

    def close(self) -> None:
        """
        Функция для закрытия интерфейса.
        """

        # Расширяем экран игрового поля до полного экрана игры
        self.field.screen_field = pg.Surface((self.screen.get_width(), self.screen.get_height()))

        # Ставим флаг, что игровое поле скрыто
        self.is_open = False

    def change_regime(self) -> None:
        """
        Функция для изменения режима интерфейса.
        (Если режим был закрыт - он открывается, если закрыт - открывается).
        """

        # Если интерфейс уже открыт, то закрываем его
        if self.is_open:
            self.close()

        # Иначе открываем его
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

    def add_buttons(self, buttons_actions: list[str]) -> None:
        """
        Функция, добавляющая в интерфейс кнопки для заданных действий.

        :param buttons_actions: Список действий, для которых нужно добавить кнопки.
        """

        # Задаём координаты для первой кнопки
        x = BUTTON_SPACING
        y = (self.image.get_height() // 2) - (BUTTON_SIZE[1] // 2)

        # Перебираем все переданные действия и формируем для них кнопки, располагая их в области интерфейса
        for action in buttons_actions:
            button = Button(action, (x, y), (BUTTON_SIZE[0], BUTTON_SIZE[1]))
            self.buttons_group.add(button)
            x += BUTTON_SIZE[0] + BUTTON_SPACING

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[Button, None]:
        """
        Функция для получения кнопки, расположенной по заданным координатам.

        :param x: Координата x кнопки на экране.
        :param y: Координата y кнопки на экране.
        :return: Кнопка или None, если по заданным координатам кнопка не найдена.
        """

        # Если интерфейс закрыт, возвращаем None
        if not self.is_open:
            return None

        # Рассчитываем координаты кнопки на поверхности интерфейса
        x_interface = x
        y_interface = y - self.field.screen_field.get_height()

        # Перебираем все кнопки из соответствующей группы спрайтов
        for button in self.buttons_group:

            # Если координаты кнопки попадают в область интерфейса, возвращаем кнопку
            if button.rect.collidepoint(x_interface, y_interface):
                return button

        # Иначе возвращаем None
        return None
