# Импорты библиотек
import pygame as pg
import typing as tp

# Импорты файлов
from menu import Menu
from level_editor.level_editor import LevelEditor
from saves import Save
from game_process import GameProcess
from level_menu import LevelMenu

# Ширина и высота экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвет фона
BACKGROUND_COLOR = "#000000"

# Частота кадров
FPS = 60

#Сложность игры
GAME_DIFFICULTY = 1

# Стартовая структура игрового поля (1 - есть шахматная клетка, 0 - нет)
START_FIELD_MAP = [[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                   [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                   [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                   [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                   [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]]

def main() -> None:
    """
    Main-функция.
    """

    # Инициализируем игру
    pg.init()

    # Создаём экран игры
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Задаём заголовок игры
    pg.display.set_caption("Chess Dungeon")

    # Создаём переменную для хранения того, какой окно сейчас следует открыть
    # (Изначально открываем главное меню)
    active_object = "main_menu"

    # Запускаем основной цикл приложения
    while True:

        if active_object == "quit":
            pg.quit()
            raise SystemExit

        # Запускаем главное меню
        if active_object == "main_menu":
            main_menu = Menu(screen)
            main_menu.add_buttons({"demo": "Демоверсия",
                                   "level_select": "Выбор уровня",
                                   "level_editor": "Редактор уровней",
                                   "quit": "Выход"})
            active_object = main_menu.start()
        
        # Перед началом игры спрашиваем уровень сложности
        elif (active_object == "demo") or (active_object == "restart"):
            difficulty_menu = Menu(screen)
            difficulty_menu.add_buttons({"hard": "Высокая сложность", 
                                         "normal": "Нормальная сложность", 
                                         "easy": "Низкая сложность", 
                                         "main_menu": "Главное меню"})
            difficulty = difficulty_menu.start()
            if difficulty == "main_menu":
                active_object = "main_menu"
                continue
            global GAME_DIFFICULTY
            if difficulty == "easy":
                GAME_DIFFICULTY = 0.5
            elif difficulty == "normal":
                GAME_DIFFICULTY = 1
            elif difficulty == "hard":
                GAME_DIFFICULTY = 1.5
            active_object = "demo_start"

        # Запускаем демо игровой процесс
        elif active_object == "demo_start":
            save = Save(save_name="First")
            active_object = GameProcess.start(save, screen)

        elif active_object == "level_select":
            active_object = LevelMenu.start(screen)

        # Запускаем редактор уровней
        elif active_object == "level_editor":
            active_object = LevelEditor.start(screen)

        # Запускаем финальное меню при проигрыше
        elif active_object == "lose_menu":
            final_menu = Menu(screen)
            final_menu.add_buttons({"quit": "Выход", 
                                    "restart": "Начать сначала", 
                                    "main_menu": "Главное меню"}, 
                                    menu_layout="bottom")
            active_object = final_menu.start(background_type="lose")

        # Запускаем финальное меню при победе
        elif active_object == "win_menu":
            final_menu = Menu(screen)
            final_menu.add_buttons({"quit": "Выход", 
                                    "restart": "Начать сначала", 
                                    "main_menu": "Главное меню"}, 
                                    menu_layout="bottom")
            active_object = final_menu.start(background_type="win")


# Запускаем Main-функцию
if __name__ == "__main__":
    main()
