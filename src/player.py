DIR_NORTH = (0, -1)
DIR_SOUTH = (0, 1)
DIR_WEST = (-1, 0)
DIR_EAST = (1, 0)


class Player:
    def __init__(self):
        self.x = 10
        self.y = 10

    def go(self, dir=(0, 0)):
        self.x += dir[0]
        self.y += dir[1]