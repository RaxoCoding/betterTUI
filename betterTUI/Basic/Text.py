import curses

from betterTUI.Screen import Screen

class Text:
    def __init__(self, screen: Screen, x: int, y: int, content: str, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.content = content
        self.parent = None

        screen.addstr(y, x, content, *args)

    def delete(self):
        self.screen.addstr(self.y, self.x, " " * len(self.content))
        del self