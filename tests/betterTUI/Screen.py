import curses

class Screen:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(True)     

    def center(self):
        max_y, max_x = self.screen.getmaxyx()
        return (int(max_x/2), int(max_y/2))

    def close(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    def __getattr__(self, attr): 
        if attr not in self.__dict__: 
            return getattr(self.screen, attr) 
        return super().__getattr__(attr)