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

        # Если ранее было выбрано действие атаки, то убираем для него выделенные клетки
        if self.selected_action == "attack":
            square_for_cast = self.selected_piece.prepare_spell('attack')
            for cell in square_for_cast:
                if cell.is_activated:
                    cell.change_regime()
            self.field.update()

        # Если ранее было выбрано действие движения, то убираем для него выделенные клетки
        elif self.selected_action == "move":
            square_for_cast = self.selected_piece.prepare_spell('move')
            for cell in square_for_cast:
                if cell.is_activated:
                    cell.change_regime()
            self.field.update()

    def toggle_move_mode(self):
        """
        Функция для включения/выключения режима движения.
        """

        # Меняем режим доступных для движения клеток (снимаем или добавляем выделение)
        square_for_move = self.selected_piece.prepare_spell('move')
        for cell in square_for_move:
            cell.change_regime()
        self.field.update()

        # Добавляем или убираем движение в качестве выбранного действия
        # (Движение может быть добавлена как выделенное действие
        # лишь при наличии хотя бы одной выделенной клетки)
        if square_for_move and (self.selected_action != "move"):
            self.selected_action = "move"
        else:
            self.selected_action = None

    def toggle_attack_mode(self):
        """
        Функция для включения/выключения режима атаки.
        """

        # Меняем режим доступных для атаки клеток (снимаем или добавляем выделение)
        square_for_cast = self.selected_piece.prepare_spell('attack')
        for cell in square_for_cast:
            cell.change_regime()
        self.field.update()

        # Добавляем или убираем атаку в качестве выбранного действия
        # (Атака может быть добавлена как выделенное действие
        # лишь при наличии хотя бы одной выделенной клетки)
        if square_for_cast and (self.selected_action != "attack"):
            self.selected_action = "attack"
        else:
            self.selected_action = None

    def finish_game_tact(self):
        """
        Функция для завершения игрового такта (очистка активированных клеток, снятие выбранных действий и фигур и т.д.).
        """

        # Очищаем раннее выделенные клетки
        self.clear_activated_squares()

        # Указываем, что клетка на которой стоит фигура, теперь не является выделенной
        self.selected_piece.cell.deselect()

        # Очищаем переменные с выделенными фигурой и действием
        self.selected_piece = None
        self.selected_action = None






