import os
import pygame as pg
from menu import Menu
from saves import Save
from game_process import GameProcess

class LevelMenu:
    """
    Класс для реализации меню выбора уровней.
    """
    
    @staticmethod
    def start(screen: pg.Surface) -> str:
        """
        Функция для запуска меню выбора уровней.

        :param screen: Экран игры.
        """
        
        folder_path = "./saves"
        level_names: dict[str, str] = {}

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                level_names[filename] = filename
        
        level_menu = Menu(screen)
        level_menu.add_buttons(level_names)
        selected_level = level_menu.start()
        
        save = Save(save_name=selected_level.rsplit(".", 1)[0])
        return GameProcess.start(save, screen)
