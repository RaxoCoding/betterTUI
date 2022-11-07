import curses

from betterTUI.Screen import Screen

class Counter:
    def __init__(self, screen: Screen, x: int, y: int, min: int, max:int, label: str, content="0", *args):
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

        screen.addstr(y, x, label)
        screen.addstr(y, x+len(label), self.content)
        screen.addstr(y-1, x+len(label)+int(len(self.content)/2), "▲")
        screen.addstr(y+1, x+len(label)+int(len(self.content)/2), "▼")

    def on(self, *args) -> int:
        if(len(args) == 0):
            args = ["\n", "KEY_ENTER"]

        self.screen.addstr(self.y, self.x, self.label, curses.A_REVERSE)

        while(True):

            key_str = self.screen.getkey()

            self.screen.addstr(self.y-1, self.x+len(self.label), " "*len(str(max)))
            self.screen.addstr(self.y+1, self.x+len(self.label), " "*len(str(max)))
            self.screen.addstr(self.y, self.x+len(self.label), " "*len(str(max)))
            
            self.screen.addstr(self.y, self.x, self.label)
            self.screen.addstr(self.y, self.x+len(self.label), self.content)
            self.screen.addstr(self.y-1, self.x+len(self.label)+int(len(self.content)/2), "▲")
            self.screen.addstr(self.y+1, self.x+len(self.label)+int(len(self.content)/2), "▼")

            if key_str in args: 
                if not(key_str == "KEY_UP" or key_str == "KEY_DOWN" or key_str == "KEY_LEFT" or key_str == "KEY_RIGHT"):
                    self.screen.addstr(self.y, self.x+len(self.label), self.content)
                    return key_str
                elif(key_str == "KEY_UP" and self.pos == 0):
                    self.screen.addstr(self.y, self.x, self.label)
                    return key_str
                elif(key_str == "KEY_DOWN" and self.pos == 0):
                    self.screen.addstr(self.y, self.x, self.label)
                    return key_str
                elif(key_str == "KEY_LEFT" and self.pos == 0):
                    self.screen.addstr(self.y, self.x, self.label)
                    return key_str
                elif(key_str == "KEY_RIGHT" and self.pos in (-1, 1)):
                    self.screen.addstr(self.y-1, self.x+len(self.label)+int(len(self.content)/2), "▲")
                    self.screen.addstr(self.y+1, self.x+len(self.label)+int(len(self.content)/2), "▼")
                    return key_str
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            match self.pos:
                case 0:
                    self.screen.addstr(self.y, self.x, self.label, curses.A_REVERSE)

                case 1:
                    self.screen.addstr(self.y-1, self.x+len(self.label)+int(len(self.content)/2), "▲", curses.A_REVERSE)

                case -1:
                    self.screen.addstr(self.y+1, self.x+len(self.label)+int(len(self.content)/2), "▼", curses.A_REVERSE)

            self.screen.addstr(self.y, self.x+len(self.label), self.content)
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
        self.screen.addstr(self.y-1, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+1, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y, self.x, " "*len(self.label))

        self.screen.addstr(y, x, self.label)
        self.screen.addstr(y, x+len(self.label), self.content)
        self.screen.addstr(y-1, x+len(self.label)+int(len(self.content)/2), "▲")
        self.screen.addstr(y+1, x+len(self.label)+int(len(self.content)/2), "▼")

        self.x = x
        self.y = y

    def delete(self):
        self.screen.addstr(self.y-1, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y+1, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y, self.x+len(self.label), " "*len(str(max)))
        self.screen.addstr(self.y, self.x, " "*len(self.label))

        del self