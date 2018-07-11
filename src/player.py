import tcod

from game_object import GameObject


class Player(GameObject):
    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', tcod.white)


class NPC(GameObject):
    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', tcod.yellow)