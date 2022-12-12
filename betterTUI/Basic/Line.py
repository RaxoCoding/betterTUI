import curses
from betterTUI.Screen import Screen

class Line:
    def __init__(self, screen: Screen, x:int, y: int, character: str, color=0, length=0, vertical=False, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.length = length
        self.character = character
        self.parent = None
        self.vertical = vertical
        self.color = color

        if(vertical):
            max_y, max_x = screen.getmaxyx()
            if self.length == 0: self.length = max_y-y-y
            for i in range(y, self.length+y):
                self.addstr(y+i, x, character, *args)
        else:
            max_y, max_x = screen.getmaxyx()
            if self.length == 0: self.length = max_x-x
            self.addstr(y, x, character*self.length, *args)

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

    def delete(self):
        if(self.vertical):
            for i in range(self.y, self.length+self.y):
                self.screen.addstr(i, self.x, " ")
        else:
            self.screen.addstr(self.y, self.x, " "*self.length)

        del self