import curses
from betterTUI.Screen import Screen

class Box:
    def __init__(self, screen: Screen, x:int, y: int, width: int, height: int, color=0, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parent = None
        self.color = color

        for i in range(0, width+1):
            self.addstr(y, x+i, "─", *args)
            self.addstr(y+height, x+i, "─", *args)

        for i in range(0, height+1):
            self.addstr(y+i, x, "│", *args)
            self.addstr(y+i, x+width, "│", *args)

        self.addstr(y, x, '┌', *args)
        self.addstr(y+height, x, '└', *args)
        self.addstr(y, x+width, '┐', *args)
        self.addstr(y+height, x+width, '┘', *args)

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

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