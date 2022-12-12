import curses
from betterTUI.Screen import Screen

class SlimButton:
    def __init__(self, screen: Screen, x: int, y: int, label: str, color=0, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = len(label)
        self.height = 1
        self.label = label
        self.parent = None
        self.color = color

        self.addstr(y, x, label)

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

    def on(self, *args) -> int:
        if(len(args) == 0):
            args =  ["\n", "KEY_ENTER"]
            
        self.addstr(self.y, self.x, self.label, curses.A_REVERSE)

        while(True):
            key_str = self.screen.getkey()

            if key_str in args:
                self.addstr(self.y, self.x, self.label)
                curses.curs_set(0)
                return key_str

            self.screen.refresh()

    def move(self, x ,y):

        self.screen.addstr(self.y, self.x, " "*len(self.label))

        self.addstr(y, x, self.label)

        self.x = x
        self.y = y

    def delete(self):
        self.screen.addstr(self.y, self.x, " "*len(self.label))

        del self