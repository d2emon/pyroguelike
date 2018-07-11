import tcod

from game_object import GameObject


class Tile:
    color_dark_wall = tcod.Color(0, 0, 100)
    color_dark_ground = tcod.Color(50, 50, 150)
    color_light_wall = tcod.Color(130, 110, 50)
    color_light_ground = tcod.Color(200, 180, 50)

    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

    def color(self, visible=True):
        if self.block_sight:
            if visible:
                return self.color_light_wall
            return self.color_dark_wall

        if visible:
            return self.color_light_ground
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
        self.rooms = []
        self.fov_map = tcod.map_new(self.width, self.height)

    def set_fov(self):
        for y in range(self.height):
            for x in range(self.width):
                # tcod.map_set_properties(self.fov_map, x, y, True, True)
                tcod.map_set_properties(self.fov_map, x, y, not self.data[x][y].block_sight, not self.data[x][y].blocked)

    def draw(self, con):
        #go through all tiles, and set their background color
        for y in range(self.height):
            for x in range(self.width):
                visible = tcod.map_is_in_fov(self.fov_map, x, y)
                tcod.console_set_char_background(con, x, y, self.data[x][y].color(visible), tcod.BKGND_SET)

    def addRoom(self, room):
        x, y = room.center()
        room.caption = GameObject(x, y, chr(65 + len(self.rooms)), tcod.white)
        self.rooms.append(room)

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