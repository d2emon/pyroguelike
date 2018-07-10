import tcod


class RoomRect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def makeTunnel(self, other, game_map):
        x, y = self.center()
        # all rooms after the first:
        # connect it to the previous room with a tunnel

        # center coordinates of previous room
        prev_x, prev_y = other.center()

        # draw a coin (random number that is either 0 or 1)
        if tcod.random_get_int(0, 0, 1) == 1:
            # first move horizontally, then vertically
            game_map.addHTunnel(prev_x, x, y)
            game_map.addVTunnel(prev_y, y, prev_x)
        else:
            # first move vertically, then horizontally
            game_map.addVTunnel(prev_y, y, x)
            game_map.addHTunnel(prev_x, x, prev_y)