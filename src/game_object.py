import tcod


DIR_NORTH = (0, -1)
DIR_SOUTH = (0, 1)
DIR_WEST = (-1, 0)
DIR_EAST = (1, 0)


class GameObject:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

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

        if game_map.data[newx][newy].blocked:
            return

        self.x = newx
        self.y = newy
        # self.x = max(min(self.x + dir[0], self.maxx), self.minx)
        # self.y = max(min(self.y + dir[1], self.maxy), self.miny)

    def draw(self, con):
        # set the color and then draw the character that represents this object at its position
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self, con):
        # erase the character that represents this object
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)