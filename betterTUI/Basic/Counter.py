import curses
from betterTUI.Screen import Screen

class Counter:
    def __init__(self, screen: Screen, x: int, y: int, min: int, max: int, label: str, color=0, content="0", *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = 3
        self.min = min
        self.max = max
        self.label = label
        self.content = content
        self.pos = 0
        self.parent = None
        self.color = color

        self.addstr(y+1, x, label)
        self.addstr(y+1, x+len(label), self.content)
        self.addstr(y, x+len(label)+int(len(self.content)/2), "▲")
        self.addstr(y+2, x+len(label)+int(len(self.content)/2), "▼")

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

    def on(self, *args) -> int:
        if(len(args) == 0):
            args = ["\n", "KEY_ENTER"]

        self.addstr(self.y+1, self.x, self.label, curses.A_REVERSE)

        while(True):

            key_str = self.screen.getkey()

            self.addstr(self.y, self.x+len(self.label), " "*len(str(max)))
            self.addstr(self.y+2, self.x+len(self.label), " "*len(str(max)))
            self.addstr(self.y+1, self.x+len(self.label), " "*len(str(max)))
            
            self.addstr(self.y+1, self.x, self.label)
            self.addstr(self.y+1, self.x+len(self.label), self.content)
            self.addstr(self.y, self.x+len(self.label)+int(len(self.content)/2), "▲")
            self.addstr(self.y+2, self.x+len(self.label)+int(len(self.content)/2), "▼")

            if key_str in args: 
                if not(key_str == "KEY_UP" or key_str == "KEY_DOWN" or key_str == "KEY_LEFT" or key_str == "KEY_RIGHT"):
                    self.addstr(self.y+1, self.x+len(self.label), self.content)
                    return key_str
                elif(key_str == "KEY_UP" and self.pos == 0):
                    self.addstr(self.y+1, self.x, self.label)
                    return key_str
                elif(key_str == "KEY_DOWN" and self.pos == 0):
                    self.addstr(self.y+1, self.x, self.label)
                    return key_str
                elif(key_str == "KEY_LEFT" and self.pos == 0):
                    self.addstr(self.y+1, self.x, self.label)
                    return key_str
                elif(key_str == "KEY_RIGHT" and self.pos in (-1, 1)):
                    self.addstr(self.y, self.x+len(self.label)+int(len(self.content)/2), "▲")
                    self.addstr(self.y+2, self.x+len(self.label)+int(len(self.content)/2), "▼")
                    return key_str
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            match self.pos:
                case 0:
                    self.addstr(self.y+1, self.x, self.label, curses.A_REVERSE)

                case 1:
                    self.addstr(self.y, self.x+len(self.label)+int(len(self.content)/2), "▲", curses.A_REVERSE)

                case -1:
                    self.addstr(self.y+2, self.x+len(self.label)+int(len(self.content)/2), "▼", curses.A_REVERSE)

            self.addstr(self.y+1, self.x+len(self.label), self.content)
            self.screen.refresh()

    def handle_key(self, key_str):
        pos = self.pos
        content = self.content

        if(key_str == "KEY_RIGHT"):
            if (pos == 0):
                self.pos += 1

        elif(key_str == "KEY_LEFT"):
            if not (pos == 0):
                self.pos = 0
        elif(key_str == "KEY_UP"):
            if (pos == 1 and (int(self.content) + 1) <= self.max):
                self.content = str(int(self.content) + 1)
            elif (pos == -1):
                self.pos = 1

        elif(key_str == "KEY_DOWN"):
            if (pos == -1 and (int(self.content) - 1) >= self.min):
                self.content = str(int(self.content) - 1)
            elif (pos == 1):
                self.pos = -1

    def move(self, x ,y):
        self.screen.addstr(self.y, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+2, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+1, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+1, self.x, " "*len(self.label))

        self.addstr(y+1, x, self.label)
        self.addstr(y+1, x+len(self.label), self.content)
        self.addstr(y, x+len(self.label)+int(len(self.content)/2), "▲")
        self.addstr(y+2, x+len(self.label)+int(len(self.content)/2), "▼")

        self.x = x
        self.y = y

    def delete(self):
        self.screen.addstr(self.y, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+2, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+1, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+1, self.x, " "*len(self.label))

        del self