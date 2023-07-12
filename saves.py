import typing as tp
import json
from piece import *

class Save:

    def __init__(self, field_map: list[list[int]] = None, difficulty: float = None, pieces: dict[str, list["Piece"]] = None, kings: dict[str, "Piece"] = None, save_name: str = None):
        
        """
        :param save_name: Задаётся, если требуется загрузка из файла
        :param field_map: Двойной массив хранящий карту поля в числовом представлении
        :param difficulty: Значение сложности игры
        :param pieces: Словарь "Название команды": Список фигур, каждая фигура - защифрованный параметр
        :param kings: Словарь "Название команды": Королевская фигура
        """

        #Если задан парамерт save_name загружаем с файла
        if not save_name is None:
            self.load(save_name)
            return

        #Собираем данные уровня
        self.field_map = field_map
        self.difficulty = difficulty

        #Распаковываем класс Piece для сохранения
        self.pieces = []
        for team in pieces.keys():
            for piece in pieces[team]:
                depack_piece = {}
                depack_piece["controller"] = piece.controller
                if depack_piece["controller"] == "comp":
                    depack_piece["action"] = piece.action
                    depack_piece["pos_patrol"] = piece.pos_patrol
                    depack_piece["way_patrol"] = []
                    for cell in piece.way_patrol:
                        depack_piece["way_patrol"].append(cell.get_pos())
                depack_piece["team"] = piece.team
                depack_piece["cell"] = piece.cell.get_pos()
                depack_piece["max_hp"] = piece.max_hp
                depack_piece["hp"] = piece.hp
                depack_piece["accuracy"] = piece.accuracy
                depack_piece["min_damage"] = piece.min_damage
                depack_piece["max_damage"] = piece.max_damage
                depack_piece["radius_move"] = piece.radius_move
                depack_piece["radius_fov"] = piece.radius_fov
                depack_piece["AP"] = piece.AP
                depack_piece["shield"] = piece.shield
                depack_piece["active_turn"] = piece.active_turn
                depack_piece["effect_list"] = []
                for effect in piece.effect_list:
                    depack_effect = {}
                    depack_effect["id"] = effect.id
                    depack_effect["timer"] = effect.timer
                    depack_effect["strength"] = effect.strength
                    depack_piece["effect_list"].append(depack_effect)
                depack_piece["spell_list"] = []
                for spell in piece.spell_list:
                    depack_spell = {}
                    depack_spell["id"] = spell.id
                    depack_spell["cooldown_now"] = spell.cooldown_now
                    depack_piece["spell_list"].append(depack_spell)

                if isinstance(piece, Pawn):
                    depack_piece["rang"] = "pawn"
                elif isinstance(piece, Bishop):
                    depack_piece["rang"] = "bishop"
                elif isinstance(piece, Knight):
                    depack_piece["rang"] = "knignt"
                elif isinstance(piece, Rook):
                    depack_piece["rang"] = "rook"
                elif isinstance(piece, Queen):
                    depack_piece["rang"] = "queen"

                self.pieces.append(depack_piece)
                    

        self.kings = []
        for team in kings.keys():
            king = kings[team]
            depack_king = {}
            depack_king["controller"] = king.controller
            if depack_piece["controller"] == "comp":
                    depack_piece["action"] = piece.action
            depack_king["team"] = king.team
            depack_king["cell"] = king.cell.get_pos()
            depack_king["max_hp"] = king.max_hp
            depack_king["hp"] = king.hp
            depack_king["accuracy"] = king.accuracy
            depack_king["min_damage"] = king.min_damage
            depack_king["max_damage"] = king.max_damage
            depack_king["radius_move"] = king.radius_move
            depack_king["radius_fov"] = king.radius_fov
            depack_king["AP"] = king.AP
            depack_king["shield"] = king.shield
            depack_king["active_turn"] = king.active_turn
            depack_king["effect_list"] = []
            for effect in king.effect_list:
                depack_effect = {}
                depack_effect["id"] = effect.id
                depack_effect["timer"] = effect.timer
                depack_effect["strength"] = effect.strength
                depack_king["effect_list"].append(depack_effect)
            depack_king["spell_list"] = []
            for spell in king.spell_list:
                depack_spell = {}
                depack_spell["id"] = spell.id
                depack_spell["cooldown_now"] = spell.cooldown_now
                depack_king["spell_list"].append(depack_spell)

            self.kings.append(depack_king)

    def load(self, save_name: str) -> None:

        """
        :param save_load: Имя файла сохранения. Вызывать только существующее
        """

        with open(f"saves/{save_name}.json", "r") as save_file:
            data = json.load(save_file)

        self.field_map = data["field_map"]
        self.difficulty = data["difficulty"]
        self.pieces = data["pieces"]
        self.kings = data["kings"]

    def save(self, save_name: str) -> None:

        """
        :param save_name: имя для файла сохранения
        """

        data = {
            "field_map": self.field_map,
            "difficulty": self.difficulty,
            "pieces": self.pieces,
            "kings": self.kings
        }

        with open(f"saves/{save_name}.json", "w") as save_file:
            json.dump(data, save_file, indent=4)

    @staticmethod
    def format(save_name):
        """
        Воспомогательная функция для форматирования файла сохранения
        """

        with open(f"saves/{save_name}.json", "r") as save_file:
            data = json.load(save_file)

        print(type(data), data)
