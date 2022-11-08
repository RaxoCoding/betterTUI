import curses

from betterTUI.Screen import Screen

class Box:
    def __init__(self, screen: Screen, x:int, y: int, width: int, height: int, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parent = None

        for i in range(0, width+1):
            screen.addstr(y, x+i, "─", *args)
            screen.addstr(y+height, x+i, "─", *args)

        for i in range(0, height+1):
            screen.addstr(y+i, x, "│", *args)
            screen.addstr(y+i, x+width, "│", *args)

        screen.addstr(y, x, '┌', *args)
        screen.addstr(y+height, x, '└', *args)
        screen.addstr(y, x+width, '┐', *args)
        screen.addstr(y+height, x+width, '┘', *args)

    def clear(self):
        for i in range(1, self.width):
            for x in range(1, self.height):
                self.screen.addstr(self.y+x, self.x+i, " ")

    def delete(self):
        for i in range(0, self.width+1):
            self.screen.addstr(self.y, self.x+i, " ")
            self.screen.addstr(self.y+self.height, self.x+i, " ")

        for i in range(0, self.height+1):
            self.screen.addstr(self.y+i, self.x, " ")
            self.screen.addstr(self.y+i, self.x+self.width, " ")

        del self