import math
import tcod


DIR_NORTH = (0, -1)
DIR_SOUTH = (0, 1)
DIR_WEST = (-1, 0)
DIR_EAST = (1, 0)


class GameObject:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fov_recompute = True
        self.aggresive = False

        self.weapon = None
        self.ai = None

    def move(self, dx, dy, game_map):
        # move by the given amount
        newx = self.x + dx
        newy = self.y + dy

        if newx < 0:
            return
        if newy < 0:
            return

        if newx >= game_map.width:
            return
        if newy >= game_map.height:
            return

        target = game_map.objects_at(newx, newy)
        # attack if target found, move otherwise
        if target is not None:
            if target.ai is not None:
                target.ai.attacked(self)

        if self.is_blocked(newx, newy, game_map):
            return

        self.x = newx
        self.y = newy
        # self.x = max(min(self.x + dir[0], self.maxx), self.minx)
        # self.y = max(min(self.y + dir[1], self.maxy), self.miny)

        self.fov_recompute = True

    def distance(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_to(self, x, y, game_map):
        # vector from this object to the target, and distance
        dx = x - self.x
        dy = y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy, game_map)

    def draw(self, con):
        # set the color and then draw the character that represents this object at its position
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, con):
        # erase the character that represents this object
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)

    def is_blocked(self, x, y, game_map):
        # first test the map tile
        if game_map.data[x][y].blocked:
            return True

        # now check for any blocking objects
        for object in game_map.objects:
            if object.blocks and object.x == x and object.y == y:
                return True

        return False