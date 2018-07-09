#! /usr/bin/python

import tcod


def handle_keys():
    global playerx, playery
    key = tcod.console_wait_for_keypress(True)
    if key.vk == tcod.KEY_ENTER and key.lalt:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    elif key.vk == tcod.KEY_ESCAPE:
        return True

    if tcod.console_is_key_pressed(tcod.KEY_UP):
        playery -= 1
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        playery += 1
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        playerx -= 1
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        playerx -= 1


SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

LIMIT_FPS = 20

playerx = int(SCREEN_WIDTH / 2)
playery = int(SCREEN_HEIGHT / 2)


def main():
    tcod.console_set_custom_font(
        'arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,
    )
    with tcod.console_init_root(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        'Title'
    ) as root_console:
        tcod.sys_set_fps(LIMIT_FPS)
        while not tcod.console_is_window_closed():
            print(tcod.console_is_window_closed())
            tcod.console_set_default_foreground(0, tcod.white)
            root_console.print_(x=0, y=0, string='Hello World')
            tcod.console_put_char(0, playerx, playery, '@', tcod.BKGND_NONE)
            tcod.console_flush()
            tcod.console_put_char(0, playerx, playery, ' ', tcod.BKGND_NONE)
            exit = handle_keys()
            if exit:
                break
        else:
            print("exit")


if __name__ == "__main__":
    main()
