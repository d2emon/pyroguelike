import tcod


class Tile:
    color_dark_wall = tcod.Color(0, 0, 100)
    color_dark_ground = tcod.Color(50, 50, 150)

    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

    @property
    def color(self):
        if self.block_sight:
            return self.color_dark_wall
        return self.color_dark_ground


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # fill map with "unblocked" tiles
        self.data = [
            [
                Tile(True)
                for y in range(self.height)
            ]
            for x in range(self.width)
        ]

    def draw(self, con):
        #go through all tiles, and set their background color
        for y in range(self.height):
            for x in range(self.width):
                tcod.console_set_char_background(con, x, y, self.data[x][y].color, tcod.BKGND_SET)

    def addRoom(self, room):
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.data[x][y].blocked = False
                self.data[x][y].block_sight = False

    def addHTunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.data[x][y].blocked = False
            self.data[x][y].block_sight = False

    def addVTunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.data[x][y].blocked = False
            self.data[x][y].block_sight = False