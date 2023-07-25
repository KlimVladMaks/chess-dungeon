import pygame as pg
import typing as tp

if tp.TYPE_CHECKING:
    from piece import Piece
    from piece import King
    from field import Field
    from field import Square
    from spell import Spell
    from interface import Interface


class Game:
    """
    Класс для управления игровым процессом.
    """

    def __init__(self, field: 'Field', interface: 'Interface') -> None:
        """
        Функция для инициализации игрового процесса.

        :param field: Игровое поле.
        :param interface: Игровой интерфейс.
        """

        # Сохраняем экземпляр игрового поля
        self.field = field

        # Сохраняем экземпляр интерфейса
        self.interface = interface

        # Свойство для хранения выбранной фигуры
        self.selected_piece: tp.Union[Piece, None] = None

        # Свойство для хранения выбранного действия
        self.selected_spell: tp.Union[Spell, None] = None

        # Словарь для хранения команд фигур
        self.pieces_teams: dict[str, list[Piece]] = {}
        # Словарь для хранения команд королей
        self.kings_teams: dict[str, King] = {}

        # Команда, чей ход
        self.active_team: str = ""

        # Список очереди (нужен для коректной передачи очереди при любом удалении команд)
        self.queue_teams: list[str] = list(self.kings_teams.keys())

        # Свойство для хранения вражеского короля
        self.computer_king: tp.Union[Piece, None] = None

        # Список для хранения просматриваемых клеток
        self.viewed_squares: tp.Union[list[Square], None] = None

        # Базовая просматриваемая клетка (относительно которой распространяется область обзора)
        self.base_viewed_square: tp.Union[Square, None] = None

        # Просматриваемая способность
        self.viewed_spell: tp.Union[Spell, None] = None

    def clear_activated_squares(self) -> None:
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

    def toggle_action_mode(self, spell: 'Spell') -> None:
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

            # Отключаем режим просмотра для всех клеток
            self.off_view_for_all_squares()

        else:
            self.selected_spell = None

    def finish_game_tact(self) -> None:
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

    def del_destroyed_pieces(self) -> None:
        """
        Функция для удаления всех уничтоженных фигур из соответствующего списка.
        """

        # Перебираем все фигуры и удаляем те, у которых HP меньше нуля
        for team in self.pieces_teams:
            for piece in self.pieces_teams[team]:
                if piece.hp <= 0:
                    self.pieces_teams[team].remove(piece)

    def del_piece(self, piece: 'Piece') -> None:
        """
        Функция для удаления фигуры из соответствующего списка.

        :param piece: Фигура, которую нужно удалить.
        """

        # Удаляем фигуру из соответсвующего списка
        self.pieces_teams[piece.team].remove(piece)
        if piece.controller == "player":
            if not self.pieces_teams[piece.team]:

                self.del_king(self.kings_teams[piece.team])


    def del_king(self, king: "King") -> None:
        """
        Функция обрабатывает смерть короля

        :param piece: Фигура, которую нужно удалить.
        """

        # Удаляем команду Короля из словаря с Королями
        self.kings_teams.pop(king.team)
        if king.controller == "comp":
            print(f"Король убит! Команда {king.team} растеряна и сдаётся в плен")
        elif king.controller == "player":
            print(f"Вся команда {king.team} уничтожена!")

    def next_team(self) -> None:
        
        """
        Функция меняет атрибут активной команды на следущую в списке команд
        """

        # Берём список команд как список ключей из словаря с Королями
        active_teams = list(self.kings_teams.keys())

        # Находим индекс текущей команды
        index = (self.queue_teams.index(self.active_team))

        for i in range(1, len(self.queue_teams)):
            if self.queue_teams[(index + i) % len(self.queue_teams)] in active_teams:
                self.active_team = self.queue_teams[(index + i) % len(self.queue_teams)]
                break
        
        # Если мы не нашли команду, то значит осталась всего 1 или 0 живых и мы должны были уже узнать поюедителя

    def get_game_status(self) -> str:
        """
        Функция для выведения состояния игры.

        :return: Строка с текущим статусом игры:
        win - победа игрока, lose - поражение игрока, continue - игра всё ещё идёт.
        """

        # Получаем все активные на данный момент команды
        active_teams = list(self.kings_teams.keys())

        # Возвращаем результат игры в зависимости от того, какой команды нет в списке
        if "white" not in active_teams:
             return "lose"
        elif "black" not in active_teams:
             return "win"

        # Если все команды есть в списке, возвращаем "continue"
        print(active_teams)
        return "continue"

    def get_overview_for_team(self, team: str) -> set['Square']:
        """
        Функция для получения клеток в области обзора всех фигур заданной команды.

        :team: Команда требующая обзор
        :return: Множество, содержащее клетки из области обзора.
        """

        # Множество для хранения клеток из области обзора
        pieces_overview_set = set()

        # Перебираем все фигуры и собираем клетки из их области обзора
        for piece in self.pieces_teams[team]:
            pieces_overview_set.update(piece.get_fovs())

        # Возвращаем полученное множество
        return pieces_overview_set

    def off_view_for_all_squares(self) -> None:
        """
        Функция для отключения режима просмотра для всех клеток.
        """

        # Убираем базовую просматриваемую клетку
        self.base_viewed_square = None

        # Если есть просматриваемые клетки
        if self.viewed_squares is not None:

            # Выключаем у них режим просмотра
            for square in self.viewed_squares:
                square.off_view()

            # Убираем все сопутствующие атрибуты
            self.viewed_squares = None
            self.viewed_spell = None

            # Обновляем игровое поле
            self.field.update()

    def next_move(self) -> None:
        """
        Функция для перехода к следующему игровому ходу.
        """
        
        # Прежде чем поменять активную команду, нужно убедиться не уничтожена ли предыдущая
        # поскольку для определения следующей в списке команд должна остаться предыдущая
        # такое возможно, если игрок последней пешкой использует "Просто пешка"

        # Делаем все фигуры старой команды неактивными
        for piece in self.pieces_teams[self.active_team]:
            piece.active_turn = False
            piece.cell.update()


        print(self.active_team, 'prev_active_team')

        # Сдвигаем команду на следующую
        self.next_team()

        print(self.active_team, 'active_team')

        # Очищаем все просматриваемые клетки
        self.off_view_for_all_squares()

        # Завершаем текущий игровой такт
        self.finish_game_tact()

        # Закрываем интерфейс (если он вдруг открыт)
        self.interface.close()

        # Делаем новый ход для каждой фигуры активной команды
        for piece in self.pieces_teams[self.active_team]:
            piece.new_turn()
        
        # Делаем новый ход для короля активной команды
        self.kings_teams[self.active_team].new_turn()

        # Обновляем состояние всех фигур
        for team in self.pieces_teams:
            for piece in self.pieces_teams[team]:
                piece.cell.update()

        # Обновляем поле
        self.field.update()

        match self.get_game_status():
            case "lose":
                return "lose"
            case "win":
                return "win"

        # Если ходил компьютер, то он сам Передаёт ход
        if self.kings_teams[self.active_team].controller == "comp":
            self.next_move()