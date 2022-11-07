import curses

class Screen:
    def __init__(self, func):
        curses.wrapper(func)