import tcod

from game_object import GameObject


class Player(GameObject):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.char = '@'
        self.color = tcod.white


class NPC(GameObject):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.char = '@'
        self.color = tcod.yellow