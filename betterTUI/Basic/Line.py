import curses

from betterTUI.Screen import Screen

class Line:
    def __init__(self, screen: Screen, x:int, y: int, character: str, length=0, vertical=False, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.length = length
        self.character = character
        self.parent = None
        self.vertical = vertical

        if(vertical):
            max_y, max_x = screen.getmaxyx()
            if self.length == 0: self.length = max_y-y-y
            for i in range(y, self.length+y):
                screen.addstr(y+i, x, character, *args)
        else:
            max_y, max_x = screen.getmaxyx()
            if self.length == 0: self.length = max_x-x
            screen.addstr(y, x, character*self.length, *args)

    def delete(self):
        if(self.vertical):
            for i in range(self.y, self.length+self.y):
                self.screen.addstr(i, self.x, " ")
        else:
            self.screen.addstr(self.y, self.x, " "*self.length)

        del self