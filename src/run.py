#! /usr/bin/python3
import tcod
from player import Player, DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST


def handle_keys(player):
    key = tcod.console_wait_for_keypress(True)
    if key.vk == tcod.KEY_ENTER and key.lalt:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    elif key.vk == tcod.KEY_ESCAPE:
        return True

    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.go(DIR_NORTH)
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.go(DIR_SOUTH)
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.go(DIR_WEST)
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player.go(DIR_EAST)


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

LIMIT_FPS = 20


def main():
    tcod.console_set_custom_font(
        'arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,
    )
    player = Player()
    player.x = int(SCREEN_WIDTH / 2)
    player.y = int(SCREEN_HEIGHT / 2)
    with tcod.console_init_root(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        'Title'
    ) as root_console:
        while not tcod.console_is_window_closed():
            tcod.sys_set_fps(LIMIT_FPS)
            tcod.console_set_default_foreground(0, tcod.white)
            root_console.print_(x=0, y=0, string='Hello World')
            tcod.console_put_char(0, player.x, player.y, '@', tcod.BKGND_NONE)
            tcod.console_flush()
            tcod.console_put_char(0, player.x, player.y, ' ', tcod.BKGND_NONE)
            exit = handle_keys(player)
            if exit:
                break
        else:
            print("exit")


if __name__ == "__main__":
    main()
