import pygame as pg
import typing as tp

if tp.TYPE_CHECKING:
    from piece import Piece
    from field import Field
    from spell import Spell


class Game:
    """
    Класс для управления игровым процессом.
    """

    def __init__(self, field: 'Field') -> None:
        """
        Функция для инициализации игрового процесса.

        :param field: Игровое поле.
        """

        # Сохраняем экземпляр игрового поля
        self.field = field

        # Свойство для хранения выбранной фигуры
        self.selected_piece: tp.Union[Piece, None] = None

        # Свойство для хранения выбранного действия
        self.selected_spell: tp.Union[Spell, None] = None

        # Списки для хранения фигур игрока и фигур компьютера
        self.player_pieces: list[Piece] = []
        self.computer_pieces: list[Piece] = []

    def clear_activated_squares(self):
        """
        Функция для очистки клеток, ранее выбранных для того или иного действия.
        """

        # Если ранее выбранного действия нет, то завершаем выполнение функции
        if self.selected_spell is None:
            return

        # Очищаем клетки, ранее выбранные для того или иного действия
        square_for_cast = self.selected_piece.prepare_spell(self.selected_spell)
        for cell in square_for_cast:
            if cell.is_activated:
                cell.change_regime()
        self.field.update()

    def toggle_action_mode(self, spell: 'Spell'):
        """
        Функция для включения/выключения режима заданного действия.

        :param spell: Заданное действие.
        """

        # Меняем режим доступных для заданного действия клеток (снимаем или добавляем выделение)
        square_for_action = self.selected_piece.prepare_spell(spell)
        for cell in square_for_action:
            cell.change_regime()
        self.field.update()

        # Добавляем или убираем заданное действие в качестве выбранного действия
        # (Заданное действие может быть добавлена как выделенное действие
        # лишь при наличии хотя бы одной выделенной клетки)
        if square_for_action and (self.selected_spell != spell):
            self.selected_spell = spell
        else:
            self.selected_spell = None

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
        self.selected_spell = None

    def del_destroyed_pieces(self):
        """
        Функция для удаления всех уничтоженных фигур из соответствующего списка.
        """

        # Перебираем все фигуры игрока и удаляем те, у которых HP меньше нуля
        for piece in self.player_pieces:
            if piece.hp <= 0:
                self.player_pieces.remove(piece)

        # Перебираем все фигуры компьютера и удаляем те, у которых HP меньше нуля
        for piece in self.computer_pieces:
            if piece.hp <= 0:
                self.computer_pieces.remove(piece)






