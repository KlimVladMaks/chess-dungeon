import typing as tp
if tp.TYPE_CHECKING:
    from piece import Piece

class Effect:

    def __init__(self, id: str, name: str, timer: int, strength: int):

        self.id = id
        self.timer = timer
        self.strength = strength
        self.name = name

    def get_effect(self, piece: "Piece", strength: int):
        pass

    def remove_effect(self, piece: "Piece", strength: int):
        pass

    @staticmethod
    def give_effect_by_id(id: str, timer: int, strength: int) -> "Effect":
        if id == "speed_reduction":
            return Speed_reduction(timer, strength)
        elif id == "accuracy_reduction":
            return Accuracy_reduction(timer, strength)

class Speed_reduction(Effect):

    def __init__(self, timer: int, strength: int):
        super().__init__("speed_reduction", "Снижение скорости", timer, strength)

    def get_effect(self, piece: "Piece"):
        piece.radius_move -= self.strength

    def remove_effect(self, piece: "Piece"):
        piece.radius_move += self.strength

class Accuracy_reduction(Effect):

    def __init__(self, timer: int, strength: int):
        super().__init__("accuracy_reduction", "Снижение меткости", timer, strength)

    def get_effect(self, piece: "Piece"):
        piece.accuracy -= self.strength

    def remove_effect(self, piece: "Piece"):
        piece.accuracy += self.strength