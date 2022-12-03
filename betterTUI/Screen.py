import curses

class Screen:
    def __init__(self, func):
        screen = curses.initscr()
        screen.keypad(True)
        self.screen = screen

        if (curses.has_colors()):
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # 1: Black on White
            self.COLOR_BLACK_WHITE = 1

            if (curses.can_change_color()):
                curses.init_color(10, 600, 600, 600) # LIGHT GREY
                curses.init_color(11, 50, 50, 50) # DARK GREY
                curses.init_pair(2, 11, 10)# 2: Dark Grey on Light Grey
               
                self.COLOR_DARKGREY_LIGHTGREY = 2

                curses.init_pair(3, 10, 11) # 3: Light Grey on Dark Grey
 
                self.COLOR_LIGHTGREY_DARKGREY = 3

                curses.init_color(13, 0, 0, 800) # BLUE
                curses.init_pair(4, 13, 0)

                self.COLOR_BLUE = 4

                curses.init_pair(5, 0, 13)

                self.COLOR_BLUE_REVERSE = 5

                curses.init_color(14, 0, 800, 0) # GREEN
                curses.init_pair(6, 14, 0)

                self.COLOR_GREEN = 6

                curses.init_pair(7, 0, 14)

                self.COLOR_GREEN_REVERSE = 7

            else:
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) # 2: Yellow on Green

        try:
            func(self)
        finally:
            curses.endwin()

    def __getattr__(self, attr): 
        if attr not in self.__dict__: 
            return getattr(self.screen, attr) 
        return super().__getattr__(attr) 
