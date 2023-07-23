import typing as tp
from level_editor.edit_field import EditSquare
import json

SPELL_FOR_RANG: dict[str, list[dict[str, any]]] = {
    "pawn": [
        {
            "id": "move",
            "cooldown": 0
        },
        {
            "id": "attack",
            "cooldown": 1
        },
        {
            "id": "lunge_move",
            "cooldown": 2
        },
        {
            "id": "just_pawn",
            "cooldown": 3
        }
    ],

    "bishop": [
        {
            "id": "move",
            "cooldown": 0
        },
        {
            "id": "shot",
            "cooldown": 1
        },
        {
            "id": "poisoned_arrow",
            "cooldown": 2
        },
        {
            "id": "emergency_care",
            "cooldown": 3
        }
    ],

    "knight": [
        {
            "id": "move",
            "cooldown": 0
        },
        {
            "id": "swift_attack_move",
            "cooldown": 1
        },
        {
            "id": "tactical_retreat",
            "cooldown": 2
        },
        {
            "id": "sabotage",
            "cooldown": 3
        }
    ],

    "rook": [
        {
            "id": "move",
            "cooldown": 0
        },
        {
            "id": "tactical_offensive",
            "cooldown": 1
        },
        {
            "id": "shield_strike",
            "cooldown": 2
        },
        {
            "id": "fortress",
            "cooldown": 3
        }
    ],

    "queen": [
        {
            "id": "move",
            "cooldown": 0
        },
        {
            "id": "into_the_heart",
            "cooldown": 1
        },
        {
            "id": "bitchiness",
            "cooldown": 2
        }
    ],

    "king": [
        {
            "id": "royal_grace",
            "cooldown": 2
        },
        {
            "id": "a_volley_of_arrows",
            "cooldown": 3
        }
    ]
}

class EditSpell():
    
    def __init__(self, id, cooldown) -> None:
        self.id = id
        self.cooldown_now = cooldown
        
class EditPiece():

    def __init__(self, team: str, cell: "EditSquare", rang: str, controller: str, action: str = 'patrol', pos_patrol: int = 0, way_patrol: list["EditSquare"] = []) -> None:
        
        """
        :param team: Команда к которой пренадлежит фигура
        :param cell: Клетка на которой находится фигура
        :param rang: Вид фигуры
        :param controler: 'player' или 'comp' определяет кто управляет фигурой
        :param action: Создаётся только при controler == 'comp'; Определяет поведение фигуры
        :param way_patrol: Создаётся только при controler == 'comp'; Определяет марштур патруля
        :param pos_patrol: Создаётся только при controler == 'comp'; Определяет положение фигуры на маршруте патруля
        """

        self.rang = rang
        self.team = team
        self.cell = cell
        self.controller = controller
        
        with open("settings/settings_of_pieces.json") as pieces_stats:
            stats = json.load(pieces_stats)[self.rang]
        self.radius_fov = stats["radius_fov"]
        self.radius_move = stats["radius_move"]
        self.max_hp = stats["max_hp"]
        self.hp = stats["max_hp"]
        self.accuracy = stats["accuracy"]
        self.min_damage = stats["min_damage"]
        self.max_damage = stats["max_damage"]

        self.AP = 2
        self.shield = 0

        if self.controller == 'player':
            self.active_turn = True
        elif self.controller == 'comp':
            self.active_turn = False

        self.effect_list = []
        self.spell_list = []
        for spell in SPELL_FOR_RANG[self.rang]:
            self.spell_list.append(EditSpell(spell["id"], 0))

        if self.controller == 'comp':
            self.action = action
            self.pos_patrol = pos_patrol
            self.way_patrol = way_patrol
