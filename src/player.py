DIR_NORTH = (0, -1)
DIR_SOUTH = (0, 1)
DIR_WEST = (-1, 0)
DIR_EAST = (1, 0)


class Player:
    def __init__(self, maxx=10, maxy=10):
        self.minx = 0
        self.maxx = maxx

        self.miny = 0
        self.maxy = maxy

        self.x = int(self.maxx / 2)
        self.y = int(self.maxy / 2)

    def go(self, dir=(0, 0)):
        self.x = max(min(self.x + dir[0], self.maxx), self.minx)
        self.y = max(min(self.y + dir[1], self.maxy), self.miny)