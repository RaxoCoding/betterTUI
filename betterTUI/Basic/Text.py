import curses
from betterTUI.Screen import Screen

class Text:
    def __init__(self, screen: Screen, x: int, y: int, content: str, color=0, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.content = content
        self.parent = None
        self.timer = None
        self.deleted = False
        self.color = color

        self.addstr(y, x, content)

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

    def delete(self):
        self.screen.addstr(self.y, self.x, " " * len(self.content))

        del self