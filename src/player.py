import tcod

from game_object import GameObject


class Player(GameObject):
    ACTION_WAIT = 1
    ACTION_MOVE = 2

    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'Player', tcod.white, True)
        self.action = None


class NPC(GameObject):
    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'NPC', tcod.yellow, True)


class Monster(GameObject):
    def __init__(self, x, y, char, name, color):
        GameObject.__init__(self, x, y, char, name, color, True)
        self.aggresive = True