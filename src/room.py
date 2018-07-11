import tcod

from game_object import GameObject


class RoomRect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.caption = None
        self.objects = []

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

    def place_objects(self, monsters):
        # choose random number of monsters
        # num_monsters = tcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
        num_monsters = tcod.random_get_int(0, 0, monsters)

        for i in range(num_monsters):
            # choose random spot for this monster
            x = tcod.random_get_int(0, self.x1 + 1, self.x2 - 1)
            y = tcod.random_get_int(0, self.y1 + 1, self.y2 - 1)

            # chances: 20% monster A, 40% monster B, 10% monster C, 30% monster D:
            choice = tcod.random_get_int(0, 0, 100)
            # if choice < 80:
            if choice < 75:
                # 80% chance of getting an orc
                # create an orc
                monster = GameObject(x, y, 'o', tcod.desaturated_green)
            else:
                # create a troll
                monster = GameObject(x, y, 'T', tcod.darker_green)

            # if choice < 20:
            # elif choice < 20 + 40:
            # elif choice < 20 + 40 + 10:
            # else:

            self.objects.append(monster)