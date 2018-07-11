#! /usr/bin/python3
import tcod
from player import Player, NPC
from game_object import DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST
from tile import GameMap
from room import RoomRect


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

LIMIT_FPS = 20

MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT
# MAP_WIDTH = 80
# MAP_HEIGHT = 40

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

MAX_ROOM_MONSTERS = 3


def handle_keys(player, game_map):
    key = tcod.console_wait_for_keypress(True)
    if key.vk == tcod.KEY_ENTER and key.lalt:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    elif key.vk == tcod.KEY_ESCAPE:
        return True

    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.move(*DIR_NORTH, game_map)
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.move(*DIR_SOUTH, game_map)
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.move(*DIR_WEST, game_map)
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player.move(*DIR_EAST, game_map)


def loadData(game_map):
    num_rooms = 0
    for r in range(MAX_ROOMS):
        # random width and height
        w = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = tcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = tcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = RoomRect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in game_map.rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            game_map.addRoom(new_room)
            if num_rooms == 0:
                # center coordinates of new room, will be useful later
                # new_x, new_y = new_room.center()
                # this is the first room, where the player starts at
                # player.x = new_x
                # player.y = new_y
                pass
            else:
                new_room.makeTunnel(game_map.rooms[num_rooms - 1], game_map)
            new_room.place_objects(MAX_ROOM_MONSTERS)

            # finally, append the new room to the list
            num_rooms += 1
    game_map.set_fov()


def main():
    tcod.console_set_custom_font(
        'arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,
    )
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Title')
    tcod.sys_set_fps(LIMIT_FPS)

    con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    loadData(game_map)

    # player = Player(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
    # npc = NPC(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
    player = Player(*game_map.rooms[0].center())
    npc = NPC(*game_map.rooms[1].center())

    objects = [npc, player]

    while not tcod.console_is_window_closed():
        tcod.console_set_default_foreground(con, tcod.white)

        tcod.console_put_char(con, player.x, player.y, '@', tcod.BKGND_NONE)

        if player.fov_recompute:
            # recompute FOV if needed (the player moved or something)
            player.fov_recompute = False
            tcod.map_compute_fov(game_map.fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS)
            game_map.draw(con)

        drawing = []
        for r in game_map.rooms:
            drawing.append(r.caption)
            drawing += r.objects
        drawing += objects
        for d in drawing:
            if tcod.map_is_in_fov(game_map.fov_map, d.x, d.y):
                d.draw(con)

        tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

        tcod.console_flush()

        for d in drawing:
            d.clear(con)

        exit = handle_keys(player, game_map)
        if exit:
            break
    else:
        print("exit")


if __name__ == "__main__":
    main()
