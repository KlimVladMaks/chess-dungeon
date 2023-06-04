import pygame as pg

# Размер кнопки в формате (ширина, высота)
BUTTON_SIZE = (400, 50)

# Расстояние между кнопками
SPACE_BETWEEN_BUTTONS = 40

# Верхний отступ для первой кнопки
TOP_MARGIN = 50


class MenuButton(pg.sprite.Sprite):
    """
    Класс для реализации кнопки меню.
    """

    def __init__(self, value: str, coordinates: tuple[int, int], button_size: tuple[int, int]) -> None:
        """
        Функция для инициализации кнопки меню.

        :param value: Значение кнопки.
        :param coordinates: Координаты кнопки.
        :param button_size: Размеры кнопки в формате (ширина, высота).
        """

        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем значение кнопки
        self.value = value

        # Задаём поверхность кнопки
        self.image = pg.Surface((button_size[0], button_size[1]))

        # Задаем цвет кнопки
        self.image.fill("#0000FF")

        # Задаём область кнопки
        self.rect = pg.Rect(coordinates[0], coordinates[1], button_size[0], button_size[1])


class MainMenu:
    """
    Класс для реализации главного меню.
    """

    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации главного меню.

        :param screen: Экран игры.
        """

        # Сохраняем экран игры
        self.screen = screen

        # Создаём группу для хранения спрайтов кнопок меню
        self.buttons_group = pg.sprite.Group()

    def add_buttons(self, button_values: list[str]) -> None:
        """
        Функция для добавления кнопок меню.

        :param button_values: Список значений кнопок.
        """

        # Создаём начальные координаты
        x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
        y = TOP_MARGIN

        # Формируем кнопки и добавляем их в группу спрайтов
        for value in button_values:
            button = MenuButton(value, (x, y), BUTTON_SIZE)
            self.buttons_group.add(button)
            y += BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS

    def open(self) -> None:
        """
        Функция для запуска главного меню.
        """

        # Устанавливаем фон
        background = pg.image.load("design/main_menu/background.png")
        self.screen.blit(background, (0, 0))
        pg.display.update()

        # Отрисовываем кнопки меню на экране
        self.buttons_group.draw(self.screen)
        pg.display.update()

        # Запускаем бесконечный цикл
        while True:

            # Перебираем игровые события
            for e in pg.event.get():

                # При закрытии игрового окна завершаем программу
                if e.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit

