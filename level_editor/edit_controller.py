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
        
        # Список текущих выбранных клеток
        self.selected_squares: list['EditSquare'] = []

        # Флаг, показывающий, реализуется ли сейчас множественное выделение клеток
        self.is_multiple_selection = False

        # Флаг, показывающий, реализуется ли сейчас множественное снятие выделения клеток
        self.is_multiple_deselection = False

    def select_square(self, square: 'EditSquare') -> None:
        """
        Функция для перевода клетки в выбранный режим.

        :param square: Клетка, которую нужно перевести в выбранный режим.
        """

        # Переводим клетку в выбранный режим и сохраняем её в списке выбранных клеток
        square.select()
        self.selected_squares.append(square)

    def deselect_squares(self) -> None:
        """
        Функция для снятия выбранного режима у текущих выбранных клеток.

        :param is_close_interface: Флаг, нужно ли закрывать интерфейс.
        """

        # Если выделенных клеток нет, то завершаем функцию
        if len(self.selected_squares) == 0:
            return

        # Снимаем выбранный режим у всех выбранных клеток и очищаем список выбранных клеток
        for selected_square in self.selected_squares:
            selected_square.deselect()
        self.selected_squares = []

    def deselect_square(self, square: 'EditSquare') -> None:
        """
        Функция для снятия выбранного режима у одной выбранной клетки.

        :param square: Клетка, у которой нужно снять выбранный режим.
        """
        
        # Снимаем выделение у заданной клетки и удаляем её из списка выделенных клеток
        square.deselect()
        self.selected_squares.remove(square)

    def fix_interface(self) -> None:
        """
        Функция для актуализации состояния интерфейса.
        """
        
        # При необходимости закрываем интерфейс
        if len(self.selected_squares) == 0 and self.interface.is_open:
            self.interface.close()
        
        # При необходимости открываем интерфейс с базовым набором кнопок
        elif len(self.selected_squares) > 0 and not self.interface.is_open:
            self.interface.open_base_interface()


# Область для отладки
if __name__ == "__main__":
    pass
