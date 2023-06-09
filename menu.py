import pygame as pg
import typing as tp

# Размер кнопки в формате (ширина, высота)
BUTTON_SIZE = (400, 50)

# Расстояние между кнопками
SPACE_BETWEEN_BUTTONS = 40

# Верхний отступ для первой кнопки в главном меню
TOP_MARGIN = 50

# Нижний отступ для первой кнопки в финальном меню
BOTTOM_MARGIN = 50

# Размер кнопки открытия игрового меню
OPEN_BUTTON_SIZE = (40, 40)

# Отступ для кнопки открытия игрового меню
OPEN_BUTTON_MARGIN = 20


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

        # Задаём область кнопки
        self.rect = pg.Rect(coordinates[0], coordinates[1], button_size[0], button_size[1])

        # Задаём изображение кнопке
        self.update()

    def update(self) -> None:
        """
        Функция для заполнения кнопки меню соответствующим изображением.
        """

        # Устанавливаем изображение в зависимости от значения кнопки
        if self.value == "demo":
            self.image = pg.image.load("design/menu/demo_button.png")
        elif self.value == "quit":
            self.image = pg.image.load("design/menu/quit_button.png")
        elif self.value == "main_menu":
            self.image = pg.image.load("design/menu/main_menu_button.png")
        elif self.value == "game_menu":
            self.image = pg.image.load("design/menu/open_game_menu_button.png")
        elif self.value == "continue_game":
            self.image = pg.image.load("design/menu/continue_game_button.png")
        elif self.value == "restart":
            self.image = pg.image.load("design/menu/restart_button.png")
        elif self.value == "hard":
            self.image = pg.image.load("design/menu/hard_button.png")
        elif self.value == "normal":
            self.image = pg.image.load("design/menu/normal_button.png")
        elif self.value == "easy":
            self.image = pg.image.load("design/menu/easy_button.png")
        elif self.value == "level_editor":
            self.image = pg.image.load("design/menu/level_editor_button.png")


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

        # Задаём начальные координаты
        x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
        y = TOP_MARGIN

        # Формируем кнопки и добавляем их в группу спрайтов
        for value in button_values:
            button = MenuButton(value, (x, y), BUTTON_SIZE)
            self.buttons_group.add(button)
            y += BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS

    def start(self) -> str:
        """
        Функция для запуска главного меню.

        :return: Значение выбранной кнопки.
        """

        # Устанавливаем фон
        background = pg.image.load("design/menu/main_background.png")
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

                # Если нажата левая клавиша мыши
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:

                    # Получаем относительные координаты клика
                    click_coordinates = pg.mouse.get_pos()

                    # Получаем нажатую кнопку
                    click_button = self.get_button_by_coordinates(click_coordinates[0], click_coordinates[1])

                    # Если нажатая кнопка равна None (т.е. никакая кнопка не нажата), то переходим к следующей итерации
                    if click_button is None:
                        continue

                    # Если нажата кнопка выхода, то завершаем игру
                    if click_button.value == "quit":
                        pg.quit()
                        raise SystemExit

                    # Иначе возвращаем значение нажатой кнопки
                    return click_button.value

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[MenuButton, None]:
        """
        Функция для получения кнопки, расположенной по заданным координатам.

        :param x: Координата x кнопки на экране.
        :param y: Координата y кнопки на экране.
        :return: Кнопка или None, если по заданным координатам кнопка не найдена.
        """

        # Перебираем все кнопки из соответствующей группы спрайтов
        for button in self.buttons_group:

            # Если координаты кнопки попадают в область интерфейса, то возвращаем кнопку
            if button.rect.collidepoint(x, y):
                return button

        # Иначе возвращаем None
        return None


class FinalMenu:
    """
    Класс для реализации финального меню (появляется после завершения игровой сессии).
    """

    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации финального меню.

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

        # Задаём начальные координаты
        x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
        y = self.screen.get_height() - BOTTOM_MARGIN - BUTTON_SIZE[1]

        # Формируем кнопки и добавляем их в группу спрайтов
        for value in button_values:
            button = MenuButton(value, (x, y), BUTTON_SIZE)
            self.buttons_group.add(button)
            y -= BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS

    def start(self, is_player_win: bool) -> str:
        """
        Функция для запуска финального меню.

        :param is_player_win: Флаг, показывающий, выиграл ли игрок.
        :return: Значение результата работы меню.
        """

        # Устанавливаем фон
        if is_player_win:
            background = pg.image.load("design/menu/win_background.png")
        else:
            background = pg.image.load("design/menu/lose_background.png")
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

                # Если нажата левая клавиша мыши
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:

                    # Получаем относительные координаты клика
                    click_coordinates = pg.mouse.get_pos()

                    # Получаем нажатую кнопку
                    click_button = self.get_button_by_coordinates(click_coordinates[0], click_coordinates[1])

                    # Если нажатая кнопка равна None (т.е. никакая кнопка не нажата), то переходим к следующей итерации
                    if click_button is None:
                        continue

                    # Если нажата кнопка выхода, то завершаем игру
                    if click_button.value == "quit":
                        pg.quit()
                        raise SystemExit

                    # Иначе возвращаем значение нажатой кнопки
                    return click_button.value

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[MenuButton, None]:
        """
        Функция для получения кнопки, расположенной по заданным координатам.

        :param x: Координата x кнопки на экране.
        :param y: Координата y кнопки на экране.
        :return: Кнопка или None, если по заданным координатам кнопка не найдена.
        """

        # Перебираем все кнопки из соответствующей группы спрайтов
        for button in self.buttons_group:

            # Если координаты кнопки попадают в область интерфейса, то возвращаем кнопку
            if button.rect.collidepoint(x, y):
                return button

        # Иначе возвращаем None
        return None


class GameMenu:
    """
    Класс для реализации игрового меню.
    """

    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации игрового меню.

        :param screen: Экран игры.
        """

        # Сохраняем экран игры
        self.screen = screen

        # Создаём кнопку открытия меню
        self.open_menu_button = MenuButton("game_menu",
                                           (self.screen.get_width() - OPEN_BUTTON_MARGIN - OPEN_BUTTON_SIZE[0],
                                            OPEN_BUTTON_MARGIN),
                                           (OPEN_BUTTON_SIZE[0], OPEN_BUTTON_SIZE[1]))

        # Создаём группу для хранения спрайтов кнопок меню
        self.buttons_group = pg.sprite.Group()

    def is_open_button_clicked(self, click_coordinates: tuple[int, int]) -> bool:
        """
        Функция для проверки того, была ли нажата кнопка открытия игрового меню.

        :param click_coordinates: Координаты клика.
        :return: True - если кнопка открытия игрового меню нажата, False - если нет.
        """

        # Возвращаем результат проверки
        return self.open_menu_button.rect.collidepoint(click_coordinates)

    def add_buttons(self, button_values: list[str]) -> None:
        """
        Функция для добавления кнопок игрового меню в развёрнутом состоянии.

        :param button_values: Список значений кнопок.
        """

        # Задаём начальные координаты
        x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
        y = TOP_MARGIN

        # Формируем кнопки и добавляем их в группу спрайтов
        for value in button_values:
            button = MenuButton(value, (x, y), BUTTON_SIZE)
            self.buttons_group.add(button)
            y += BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS

    def start(self) -> str:
        """
        Функция для запуска игрового меню в развёрнутом состоянии.

        :return: Значение выбранной кнопки.
        """

        # Устанавливаем фон
        background = pg.image.load("design/menu/main_background.png")
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

                # Если нажата левая клавиша мыши
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:

                    # Получаем относительные координаты клика
                    click_coordinates = pg.mouse.get_pos()

                    # Получаем нажатую кнопку
                    click_button = self.get_button_by_coordinates(click_coordinates[0], click_coordinates[1])

                    # Если нажатая кнопка равна None (т.е. никакая кнопка не нажата), то переходим к следующей итерации
                    if click_button is None:
                        continue

                    # Если нажата кнопка выхода, то завершаем игру
                    if click_button.value == "quit":
                        pg.quit()
                        raise SystemExit

                    # Иначе возвращаем значение нажатой кнопки
                    return click_button.value

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[MenuButton, None]:
        """
        Функция для получения кнопки, расположенной по заданным координатам.

        :param x: Координата x кнопки на экране.
        :param y: Координата y кнопки на экране.
        :return: Кнопка или None, если по заданным координатам кнопка не найдена.
        """

        # Перебираем все кнопки из соответствующей группы спрайтов
        for button in self.buttons_group:

            # Если координаты кнопки попадают в область интерфейса, то возвращаем кнопку
            if button.rect.collidepoint(x, y):
                return button

        # Иначе возвращаем None
        return None


class DifficultyMenu(MainMenu):
    """
    Меню для выбора сложности игры.
    """
    pass

