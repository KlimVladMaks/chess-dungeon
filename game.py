import pygame as pg
import typing as tp


class _Piece:
    pass


class _Field:
    pass


class Game:
    """
    Класс для управления игровым процессом.
    """

    def __init__(self, field: _Field) -> None:
        """
        Функция для инициализации игрового процесса.

        :param field: Игровое поле.
        """

        # Сохраняем экземпляр игрового поля
        self.field = field

        # Свойство для хранения выбранной фигуры
        self.selected_piece: tp.Union[_Piece, None] = None

        # Свойство для хранения выбранного действия
        self.selected_action: tp.Union[str, None] = None

    def clear_activated_squares(self):
        """
        Функция для очистки клеток, ранее выбранных для того или иного действия.
        """

        # Если ранее выбранного действия нет, то завершаем выполнение функции
        if self.selected_action is None:
            return

        # Очищаем клетки, ранее выбранные для того или иного действия
        square_for_cast = self.selected_piece.prepare_spell(self.selected_action)
        for cell in square_for_cast:
            if cell.is_activated:
                cell.change_regime()
        self.field.update()

    def toggle_action_mode(self, action: str):
        """
        Функция для включения/выключения режима заданного действия.

        :param action: Название действия.
        """

        # Меняем режим доступных для заданного действия клеток (снимаем или добавляем выделение)
        square_for_action = self.selected_piece.prepare_spell(action)
        for cell in square_for_action:
            cell.change_regime()
        self.field.update()

        # Добавляем или убираем заданное действие в качестве выбранного действия
        # (Заданное действие может быть добавлена как выделенное действие
        # лишь при наличии хотя бы одной выделенной клетки)
        if square_for_action and (self.selected_action != action):
            self.selected_action = action
        else:
            self.selected_action = None

    def finish_game_tact(self):
        """
        Функция для завершения игрового такта (очистка активированных клеток, снятие выбранных действий и фигур и т.д.).
        """

        # Очищаем раннее выделенные клетки
        self.clear_activated_squares()

        # Указываем, что клетка на которой стоит фигура, теперь не является выделенной
        if self.selected_piece is not None:
            self.selected_piece.cell.deselect()

        # Очищаем переменные с выделенными фигурой и действием
        self.selected_piece = None
        self.selected_action = None






