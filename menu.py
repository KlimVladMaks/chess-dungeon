import pygame as pg
import typing as tp
from settings.controls import Controls

BUTTON_SIZE = (400, 50)
BUTTON_BACKGROUND_COLOR = (255, 145, 77)
BUTTON_FONT_SIZE = 40
BUTTON_FONT_COLOR = (0, 0, 0)

OPEN_BUTTON_SIZE = (40, 40)
OPEN_BUTTON_MARGIN = 20

MENU_MARGIN = 50
SPACE_BETWEEN_BUTTONS = 40


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
        self.buttons_group = pg.sprite.Group()
        self.open_menu_button = OpenMenuButton(screen)
    
    def add_buttons(self, button_keys_texts_dict: dict[str, str], menu_layout="top") -> None:
        """
        Функция для добавления кнопок меню.
        (Предыдущие кнопки меню при этом удаляются)

        :param button_keys_texts_dict: Словарь с ключами и надписями кнопок в формате {ключ: надпись}.
        :param menu_layout: Расположения меню ("top" - сверху, "bottom" - снизу).
        """

        self.buttons_group = pg.sprite.Group()

        if menu_layout == "top":

            x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
            y = MENU_MARGIN

            for key in button_keys_texts_dict:
                button = MenuButton(key, button_keys_texts_dict[key], (x, y), BUTTON_SIZE)
                self.buttons_group.add(button)
                y += BUTTON_SIZE[1] + SPACE_BETWEEN_BUTTONS
        
        elif menu_layout == "bottom":

            x = self.screen.get_width() // 2 - BUTTON_SIZE[0] // 2
            y = self.screen.get_height() - MENU_MARGIN - BUTTON_SIZE[1]

            for key in button_keys_texts_dict:
                button = MenuButton(key, button_keys_texts_dict[key], (x, y), BUTTON_SIZE)
                self.buttons_group.add(button)
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
        
        if background_type == "base":
            background = pg.image.load("design/menu/main_background.png")
        elif background_type == "win":
            background = pg.image.load("design/menu/win_background.png")
        elif background_type == "lose":
            background = pg.image.load("design/menu/lose_background.png")

        self.screen.blit(background, (0, 0))
        self.buttons_group.draw(self.screen)
        pg.display.update()

        while True:

            for e in pg.event.get():

                if Controls.is_quit(e):
                    pg.quit()
                    raise SystemExit
                
                # Нажатие правой клавиши мыши
                elif Controls.is_selection(e):

                    click_coordinates = pg.mouse.get_pos()
                    click_button = self.get_button_by_coordinates(click_coordinates[0], click_coordinates[1])

                    if click_button is None:
                        continue

                    return click_button.key

    def get_button_by_coordinates(self, x: int, y: int) -> tp.Union[MenuButton, None]:
        """
        Функция для получения кнопки меню, расположенной по заданным координатам.

        :param x: Координата x кнопки.
        :param y: Координата y кнопки.
        :return: Кнопка или None, если по заданным координатам кнопка не найдена.
        """

        for button in self.buttons_group:
            if button.rect.collidepoint(x, y):
                return button
        
        return None
