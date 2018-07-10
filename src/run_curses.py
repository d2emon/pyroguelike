#! /usr/bin/python3
import curses
from player import Player, DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST


def handle_keys(stdscr, player):
    key = stdscr.getch()

    if key == 27:
        return True

    stdscr.addstr(player.y, player.x, " ")
    if key == curses.KEY_UP:
        player.go(DIR_NORTH)
    elif key == curses.KEY_DOWN:
        player.go(DIR_SOUTH)
    elif key == curses.KEY_LEFT:
        player.go(DIR_WEST)
    elif key == curses.KEY_RIGHT:
        player.go(DIR_EAST)


def main(stdscr):
    # Clear screen
    stdscr.clear()

    player = Player()

    # This raises ZeroDivisionError when i == 10.
    # for i in range(0, 10):
    #     v = i - 10
    #     stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10 / v))

    while True:
        stdscr.addstr(0, 0, "Hello World")
        stdscr.addstr(player.y, player.x, "@")
        stdscr.refresh()

        exit = handle_keys(stdscr, player)
        if exit:
            break


if __name__ == "__main__":
    curses.wrapper(main)