# Импорты библиотек
import pygame as pg
import typing as tp

# Импорт файлов
from level_editor.edit_interface import EDIT_INTERFACE_BASE_LIST

# Импорт файлов для задания типов
if tp.TYPE_CHECKING:
    from level_editor.edit_field import EditSquare, EditField
    from level_editor.edit_interface import EditInterface


class EditController:
    """
    Класс для реализации контроллера для управления редактором уровней.
    """
    
    def __init__(self, field: 'EditField', interface: 'EditInterface') -> None:
        """
        Функция для инициализации контроллера редактирования.

        :param field: Игровое поле.
        :param interface: Интерфейс редактирования.
        """

        # Сохраняем игровое поле
        self.field = field

        # Сохраняем интерфейс редактирования
        self.interface = interface
        
        # Текущая выбранная клетка
        self.selected_square: tp.Union['EditSquare', None] = None

    def select_square(self, square: 'EditSquare') -> None:
        """
        Функция для перевода клетки в выбранный режим.

        :param square: Клетка, которую нужно перевести в выбранный режим.
        """

        # Если существует предыдущая выбранная клетка, то снимаем у неё режим выделения
        if self.selected_square is not None:
            self.selected_square.deselect()

        # Переводим клетку в выбранный режим и сохраняем её в памяти
        square.select()
        self.selected_square = square

        # Добавляем к интерфейсу базовый набор кнопок и открываем интерфейс 
        self.interface.add_buttons(EDIT_INTERFACE_BASE_LIST)
        self.interface.open()

    def deselect_square(self) -> None:
        """
        Функция для снятия выбранного режима у текущей выбранной клетки.
        """

        # Если выделенной клетки нет, то завершаем функцию
        if self.selected_square is None:
            return

        # Снимаем выбранный режим у выбранной клетки и удаляем её из памяти
        self.selected_square.deselect()
        self.selected_square = None

        # Закрываем интерфейс
        self.interface.close()


# Область для отладки
if __name__ == "__main__":
    pass
