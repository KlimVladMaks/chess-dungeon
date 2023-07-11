# Импорты библиотек
import pygame as pg
import typing as tp

# Импорты файлов
from menu import GameMenu

# Размер кнопки открытия меню
OPEN_BUTTON_SIZE = (40, 40)

# Отступ для кнопки открытия меню
OPEN_BUTTON_MARGIN = 20

# Размер кнопки меню в формате (ширина, высота)
BUTTON_SIZE = (400, 50)

# Цвет фона кнопок меню редактора уровней
BUTTON_BACKGROUND_COLOR = (255, 145, 77)

# Верхний отступ для первой кнопки развёрнутого меню
TOP_MARGIN = 50

# Расстояние между кнопками меню
SPACE_BETWEEN_BUTTONS = 40

# Размер текста для надписей на кнопках меню
FONT_SIZE = 40

# Цвет текста для надписей на кнопках меню
FONT_COLOR = (0, 0, 0)

# Базовый набор кнопок меню редактора уровней
BASE_MENU_DICT = {"continue": "Продолжить",
                  "main_menu": "Главное меню"}


class OpenEditMenuButton(pg.sprite.Sprite):
    """
    Кнопка для открытия меню редактора уровней.
    """
    
    def __init__(self, coordinates: tuple[int, int], button_size: tuple[int, int]) -> None:
        """
        Функция для инициализации кнопки открытия меню редактора уровней.

        :param coordinates: Координаты кнопки в формате (x, y).
        :param button_size: Размеры кнопки в формате (ширина, высота).
        """
        
        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Загружаем изображение кнопки
        self.image = pg.image.load("./design/level_editor/edit_menu/open_edit_menu_button.png")

        # Задаём область кнопки
        self.rect = pg.Rect(coordinates[0], coordinates[1], button_size[0], button_size[1])


class EditMenuButton(pg.sprite.Sprite):
    """
    Класс для реализации кнопки меню редактора уровней.
    """
    
    def __init__(self, value: str, text: str, coordinates: tuple[int, int], button_size: tuple[int, int]) -> None:
        """
        Функция для инициализации кнопки меню.

        :param value: Значение кнопки.
        :param text: Текст надписи на кнопке.
        :param coordinates: Координаты кнопки в формате (x, y).
        :param button_size: Размеры кнопки в формате (ширина, высота).
        """

        # Инициализируем спрайт
        pg.sprite.Sprite.__init__(self)

        # Сохраняем значение кнопки
        self.value = value

        # Сохраняем текст надписи на кнопке
        self.text = text

        # Задаём поверхность кнопки
        self.image = pg.Surface((button_size[0], button_size[1]))
        self.image.fill(BUTTON_BACKGROUND_COLOR)

        # Задаём область кнопки
        self.rect = pg.Rect(coordinates[0], coordinates[1], button_size[0], button_size[1])

        # Создаём шрифт для нанесения надписей на кнопки
        self.font = pg.font.Font(None, FONT_SIZE)

        # Отрисовываем заданный текст на кнопке
        text_surface = self.font.render(self.text, True, FONT_COLOR)
        self.image.blit(text_surface, 
                        (self.image.get_width() // 2 - text_surface.get_width() // 2, 
                         self.image.get_height() // 2 - text_surface.get_height() // 2))


class EditMenu:
    """
    Класс для реализации меню редактора уровней.
    """
    
    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации меню редактора уровней.

        :param screen: Экран игры.
        """

        # Сохраняем экран игры
        self.screen = screen

        # Создаём кнопку открытия меню
        self.open_menu_button = OpenEditMenuButton((self.screen.get_width() - OPEN_BUTTON_MARGIN - OPEN_BUTTON_SIZE[0], 
                                                    OPEN_BUTTON_MARGIN), 
                                                   (OPEN_BUTTON_SIZE[0], 
                                                    OPEN_BUTTON_SIZE[1]))

        # Создаём группу для хранения спрайтов кнопок меню
        self.buttons_group = pg.sprite.Group()

    def is_open_button_clicked(self, click_coordinates: tuple[int, int]) -> bool:
        """
        Функция для проверки того, была ли нажата кнопка открытия меню.

        :param click_coordinates: Координаты клика.
        :return: True - если кнопка открытия меню нажата, False - если нет.
        """

        # Возвращаем результат проверки
        return self.open_menu_button.rect.collidepoint(click_coordinates)

    def add_buttons(self, button_values_and_texts: dict[str, str]) -> None:
        """
        Функция для добавления кнопок меню в развёрнутом состоянии.

        :param button_values_and_texts: Словарь со значениями и текстами кнопок в формате {значение: текст}.
        """

        # Задаём начальные координаты
        x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
        y = TOP_MARGIN

        # Формируем кнопки и добавляем их в группу спрайтов
        for value in button_values_and_texts:
            button = EditMenuButton(value, button_values_and_texts[value], (x, y), BUTTON_SIZE)
            self.buttons_group.add(button)
            y += BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS

    def start(self) -> str:
        """
        Функция для запуска меню в развёрнутом состоянии.

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

                    # Иначе возвращаем значение нажатой кнопки
                    return click_button.value

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[EditMenuButton, None]:
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
