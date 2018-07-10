#! /usr/bin/python3
import tcod
from player import Player, NPC
from game_object import DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST
from tile import GameMap


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


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 40


def main():
    tcod.console_set_custom_font(
        'arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,
    )
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Title')
    tcod.sys_set_fps(LIMIT_FPS)

    con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    player = Player(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
    npc = NPC(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))

    objects = [npc, player, npc]

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    game_map.data[30][22].blocked = True
    game_map.data[30][22].block_sight = True
    game_map.data[50][22].blocked = True
    game_map.data[50][22].block_sight = True

    while not tcod.console_is_window_closed():
        tcod.console_set_default_foreground(con, tcod.white)

        con.print_(x=0, y=0, string='Hello World')
        tcod.console_put_char(con, player.x, player.y, '@', tcod.BKGND_NONE)

        game_map.draw(con)
        for o in objects:
            o.draw(con)

        tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

        tcod.console_flush()

        for o in objects:
            o.clear(con)

        exit = handle_keys(player, game_map)
        if exit:
            break
    else:
        print("exit")


if __name__ == "__main__":
    main()
