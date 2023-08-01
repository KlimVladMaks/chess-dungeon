import pygame as pg
import typing as tp
from settings.controls import Controls

BUTTON_SIZE = (400, 50)
BUTTON_BACKGROUND_COLOR = (255, 145, 77)
BUTTON_FONT_SIZE = 40
BUTTON_FONT_COLOR = (0, 0, 0)

OPEN_BUTTON_SIZE = (40, 40)
OPEN_BUTTON_MARGIN = 20

ARROW_BUTTON_SIZE = (40, 40)
ARROW_BUTTON_MARGIN = 50

MENU_MARGIN = 50
SPACE_BETWEEN_BUTTONS = 40
MAX_BUTTONS_ON_PAGE = 6


class OpenMenuButton(pg.sprite.Sprite):
    """
    Класс для реализации кнопки отрытия меню.
    """

    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации кнопки открытия меню.

        :param screen: Экран игры.
        """
        
        pg.sprite.Sprite.__init__(self)

        coordinates = (screen.get_width() - OPEN_BUTTON_MARGIN - OPEN_BUTTON_SIZE[0], OPEN_BUTTON_MARGIN)
        size = (OPEN_BUTTON_SIZE[0], OPEN_BUTTON_SIZE[1])

        self.image = pg.image.load("./design/level_editor/edit_menu/open_edit_menu_button.png")
        self.rect = pg.Rect(coordinates[0], coordinates[1], size[0], size[1])


class MenuButton(pg.sprite.Sprite):
    """
    Класс для реализации кнопки меню.
    """
    
    def __init__(self, key: str, text: str, coordinates: tuple[int, int], size: tuple[int, int]) -> None:
        """
        Функция для инициализации кнопки меню.

        :param key: Уникальный ключ кнопки.
        :param text: Текст надписи на кнопке.
        :param coordinates: Координаты кнопки в формате (x, y).
        :param size: Размер кнопки в формате (ширина, высота).
        """

        pg.sprite.Sprite.__init__(self)

        self.key = key
        self.text = text

        self.image = pg.Surface((size[0], size[1]))
        self.image.fill(BUTTON_BACKGROUND_COLOR)

        self.rect = pg.Rect(coordinates[0], coordinates[1], size[0], size[1])

        self.font = pg.font.Font(None, BUTTON_FONT_SIZE)

        text_surface = self.font.render(self.text, True, BUTTON_FONT_COLOR)
        self.image.blit(text_surface, 
                        (self.image.get_width() // 2 - text_surface.get_width() // 2, 
                         self.image.get_height() // 2 - text_surface.get_height() // 2))


class ArrowButtonLeft(pg.sprite.Sprite):
    """
    Класс для реализации правой стрелки пролистывания меню.
    """
    
    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации правой стрелки пролистывания меню.

        :param screen: Экран игры.
        """
        
        pg.sprite.Sprite.__init__(self)

        coordinates = (ARROW_BUTTON_MARGIN, screen.get_height() // 2 - ARROW_BUTTON_SIZE[1] // 2)
        size = (ARROW_BUTTON_SIZE[0], ARROW_BUTTON_SIZE[1])

        self.image = pg.image.load("./design/menu/left_arrow_button.png")
        self.rect = pg.Rect(coordinates[0], coordinates[1], size[0], size[1])


class ArrowButtonRight(pg.sprite.Sprite):
    """
    Класс для реализации левой стрелки пролистывания меню.
    """
    
    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации левой стрелки пролистывания меню.

        :param screen: Экран игры.
        """
        
        pg.sprite.Sprite.__init__(self)

        coordinates = (screen.get_width() - ARROW_BUTTON_MARGIN - ARROW_BUTTON_SIZE[0], 
                       screen.get_height() // 2 - ARROW_BUTTON_SIZE[1] // 2)
        size = (ARROW_BUTTON_SIZE[0], ARROW_BUTTON_SIZE[1])

        self.image = pg.image.load("./design/menu/right_arrow_button.png")
        self.rect = pg.Rect(coordinates[0], coordinates[1], size[0], size[1])


class Menu:
    """
    Класс для реализации меню с кнопками выбора.
    """
    
    def __init__(self, screen: pg.Surface) -> None:
        """
        Функция для инициализации меню.

        :param screen: Экран игры.
        """
        
        self.screen = screen
        self.buttons_structure = []
        self.buttons_group_on_page = pg.sprite.Group()
        self.current_page = 0
        self.background_type = "base"

        self.open_menu_button = OpenMenuButton(screen)
        self.left_arrow_button = ArrowButtonLeft(screen)
        self.right_arrow_button = ArrowButtonRight(screen)
    
    def add_buttons(self, button_keys_texts_dict: dict[str, str], menu_layout="top") -> None:
        """
        Функция для добавления кнопок меню.
        (Предыдущие кнопки меню при этом удаляются)

        :param button_keys_texts_dict: Словарь с ключами и надписями кнопок в формате {ключ: надпись}.
        :param menu_layout: Расположения меню ("top" - сверху, "bottom" - снизу).
        """

        self.menu_layout = menu_layout

        self.buttons_structure = []

        buttons_on_page_dict = {}
        button_counter = 0

        for key in button_keys_texts_dict:
            buttons_on_page_dict[key] = button_keys_texts_dict[key]
            button_counter += 1

            if button_counter >= MAX_BUTTONS_ON_PAGE:
                self.buttons_structure.append(buttons_on_page_dict.copy())
                buttons_on_page_dict = {}
                button_counter = 0
        
        if buttons_on_page_dict:
            self.buttons_structure.append(buttons_on_page_dict.copy())

        self.add_buttons_on_page(self.buttons_structure[self.current_page])

    def add_buttons_on_page(self, button_keys_texts_dict: dict[str, str]) -> None:
        """
        Функция для добавления кнопок меню на отдельную страницу.

        :param button_keys_texts_dict: Словарь с ключами и надписями кнопок в формате {ключ: надпись}.
        """

        self.buttons_group_on_page = pg.sprite.Group()
        
        if self.menu_layout == "top":

            x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
            y = MENU_MARGIN

            for key in button_keys_texts_dict:
                button = MenuButton(key, button_keys_texts_dict[key], (x, y), BUTTON_SIZE)
                self.buttons_group_on_page.add(button)
                y += BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS
        
        elif self.menu_layout == "bottom":

            x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
            y = self.screen.get_height() - MENU_MARGIN - BUTTON_SIZE[1]

            for key in button_keys_texts_dict:
                button = MenuButton(key, button_keys_texts_dict[key], (x, y), BUTTON_SIZE)
                self.buttons_group_on_page.add(button)
                y -= BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS

    def is_open_button_clicked(self, click_coordinates: tuple[int, int]) -> bool:
        """
        Функция для проверки того, была ли нажата кнопка открытия меню.

        :param click_coordinates: Координаты клика.
        :return: True - если кнопка открытия меню нажата, False - если нет.
        """

        return self.open_menu_button.rect.collidepoint(click_coordinates)

    def start(self, background_type="base") -> str:
        """
        Функция для запуска (открытия) экрана меню.

        :param background: Тип фона меню ("base" - стандартный фон, "win" - фон победы, "lose" - фон поражения).
        :return: Значение выбранной кнопки.
        """

        self.background_type = background_type

        self.draw_buttons()

        while True:

            for e in pg.event.get():

                if Controls.is_quit(e):
                    pg.quit()
                    raise SystemExit
                
                elif Controls.is_selection(e):

                    click_coordinates = pg.mouse.get_pos()
                    click_button = self.get_button_by_coordinates(click_coordinates[0], click_coordinates[1])

                    if click_button is None:
                        continue

                    elif isinstance(click_button, ArrowButtonLeft):
                        self.flip("left")
                    
                    elif isinstance(click_button, ArrowButtonRight):
                        self.flip("right")

                    else:
                        return click_button.key

    def draw_buttons(self) -> None:
        """
        Функция для отрисовки кнопок на экране.

        :param background: Тип фона меню ("base" - стандартный фон, "win" - фон победы, "lose" - фон поражения).
        """
        
        if self.background_type == "base":
            background = pg.image.load("design/menu/main_background.png")
        elif self.background_type == "win":
            background = pg.image.load("design/menu/win_background.png")
        elif self.background_type == "lose":
            background = pg.image.load("design/menu/lose_background.png")

        self.screen.blit(background, (0, 0))

        if len(self.buttons_structure) > 1:
            self.buttons_group_on_page.add(self.left_arrow_button)
            self.buttons_group_on_page.add(self.right_arrow_button)

        self.buttons_group_on_page.draw(self.screen)
        pg.display.update()

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[MenuButton, None]:
        """
        Функция для получения кнопки меню, расположенной по заданным координатам.

        :param x: Координата x кнопки.
        :param y: Координата y кнопки.
        :return: Кнопка или None, если по заданным координатам кнопка не найдена.
        """

        for button in self.buttons_group_on_page:
            if button.rect.collidepoint(x, y):
                return button
        
        return None

    def flip(self, direction: str) -> None:
        """
        Функция для пролистывания меню.

        :param direction: Направление пролистывания ("left" или "right").
        """
        
        if direction == "left":
            self.current_page -= 1
        elif direction == "right":
            self.current_page += 1
        
        if self.current_page < 0:
            self.current_page = len(self.buttons_structure) - 1
        elif self.current_page > len(self.buttons_structure) - 1:
            self.current_page = 0
        
        self.add_buttons_on_page(self.buttons_structure[self.current_page])

        self.draw_buttons()
