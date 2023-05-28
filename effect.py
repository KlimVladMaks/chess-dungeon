import typing as tp
if tp.TYPE_CHECKING:
    from piece import Piece

class Effect:

    def __init__(self, id: str, timer: int, strength: int):

        self.id = id
        self.timer = timer
        self.strength = strength

    def get_effect(self, piece: "Piece", strength: int):
        pass

    def remove_effect(self, piece: "Piece", strength: int):
        pass

class Speed_reduction(Effect):

    def __init__(self, timer: int, strength: int):
        super().__init__('speed_reduction', timer, strength)

    def get_effect(self, piece: "Piece"):
        piece.radius_move -= self.strength

    def remove_effect(self, piece: "Piece"):
        piece.radius_move += self.strength