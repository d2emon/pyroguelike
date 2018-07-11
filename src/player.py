import tcod

from game_object import GameObject


class Weapon:
    def __init__(self, hp, defense, power):
        self.hp = hp
        self.defense = defense
        self.power = power


class AI:
    def __init__(self, owner):
        self.owner = owner

    def turn(self, player, game_map):
        # a basic monster takes its turn. If you can see it, it can see you
        if not self.owner.aggresive:
            return
        print('The ' + self.owner.name + ' growls!')
        monster = self.owner
        if not tcod.map_is_in_fov(game_map.fov_map, self.owner.x, self.owner.y):
            return
        # move towards player if far away
        if self.owner.distance(player) >= 2:
            self.owner.move_to(player.x, player.y, game_map)
        # close enough, attack! (if the player is still alive.)
        elif player.weapon.hp > 0:
            print('The attack of the ' + self.owner.name + ' bounces off your shiny metal armor!')

    def attacked(self, enemy):
        if not self.owner.aggresive:
            return
        print('The ' + self.owner.name + ' laughs at your puny efforts to attack him!')


class Player(GameObject):
    ACTION_WAIT = 1
    ACTION_MOVE = 2

    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'Player', tcod.white, True)
        self.action = None
        self.weapon = Weapon(hp=30, defense=2, power=5)


class NPC(GameObject):
    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'NPC', tcod.yellow, True)


class Monster(GameObject):
    def __init__(self, x, y, char, name, color, weapon=None):
        GameObject.__init__(self, x, y, char, name, color, True)
        self.aggresive = True
        self.weapon = weapon
        self.ai = AI(self)