import typing as tp

class Effect:

    def __init__(self, id: str, get_effect, remove_effect, timer: int, strength: int):

        self.id = id
        self.get_effect = get_effect
        self.remove_effect = remove_effect
        self.timer = timer
        self.strength = strength

#Эффект "speed_reduction"
def get_speed_reduction(self, strength):
    """
    self: Piece
    """
    print(type(self))

    self.radius_move -= strength

def remove_speed_reduction(self, strength):
    """
    self: Piece
    """

    self.radius_move += strength

speed_reduction = Effect('speed_reduction', get_speed_reduction, remove_speed_reduction, 0, 0)