import tcod

from game_object import GameObject


class Player(GameObject):
    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'Player', tcod.white, True)


class NPC(GameObject):
    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'NPC', tcod.yellow, True)