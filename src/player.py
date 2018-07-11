import tcod

from game_object import GameObject


class Weapon:
    def __init__(self, owner, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.owner = owner

    def take_damage(self, damage, game_map):
        #apply damage if possible
        if damage > 0:
            self.hp -= damage

        # check for death. if there's a death function, call it
        if self.hp <= 0:
            if self.owner.death is not None:
                self.owner.death(game_map)

    def attack(self, target, game_map):
        # a simple formula for attack damage
        damage = self.power - target.weapon.defense

        if damage > 0:
            # make the target take some damage
            print(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.weapon.take_damage(damage, game_map)
        else:
            print(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

class AI:
    def __init__(self, owner):
        self.owner = owner

    def turn(self, player, game_map):
        # a basic monster takes its turn. If you can see it, it can see you
        if not self.owner.aggresive:
            return
        # print('The ' + self.owner.name + ' growls!')
        if not tcod.map_is_in_fov(game_map.fov_map, self.owner.x, self.owner.y):
            return
        # move towards player if far away
        if self.owner.distance(player) >= 2:
            self.owner.move_to(player.x, player.y, game_map)
        # close enough, attack! (if the player is still alive.)
        elif player.weapon.hp > 0:
            print('The attack of the ' + self.owner.name + ' bounces off your shiny metal armor!')
            self.owner.weapon.attack(player, game_map)

    def attacked(self, enemy, game_map):
        if not self.owner.aggresive:
            return
        print('The ' + self.owner.name + ' laughs at your puny efforts to attack him!')
        enemy.weapon.attack(self.owner, game_map)


class Player(GameObject):
    ACTION_WAIT = 1
    ACTION_MOVE = 2
    ACTION_DEAD = -1

    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'Player', tcod.white, True)
        self.action = None
        self.weapon = Weapon(self, hp=30, defense=2, power=5)

    def death(self, game_map):
        # the game ended!
        print('You died!')
        self.action = self.ACTION_DEAD

        # for added effect, transform the player into a corpse!
        self.char = '%'
        self.color = tcod.dark_red

        game_map.send_to_back(self)

class NPC(GameObject):
    def __init__(self, x=0, y=0):
        GameObject.__init__(self, x, y, '@', 'NPC', tcod.yellow, True)


class Monster(GameObject):
    def __init__(self, x, y, char, name, color, weapon=None):
        GameObject.__init__(self, x, y, char, name, color, True)
        self.aggresive = True
        self.weapon = weapon
        self.weapon.owner = self
        self.ai = AI(self)

    def death(self, game_map):
        # transform it into a nasty corpse! it doesn't block, can't be
        # attacked and doesn't move
        print(self.name.capitalize() + ' is dead!')

        # for added effect, transform the player into a corpse!
        self.char = '%'
        self.color = tcod.dark_red
        self.blocks = False
        self.weapon = None
        self.ai = None
        self.name = 'remains of ' + self.name

        game_map.send_to_back(self)