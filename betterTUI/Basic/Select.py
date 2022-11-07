import curses

from betterTUI.Screen import Screen
from betterTUI.Basic import Box, Text

class Select:
    def __init__(self, screen: Screen, x: int, y: int, label: str, options: list, content="", *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.label = label
        self.height = 1
        self.options = options
        self.content = content
        self.pos = 0
        self.parent = None
        self.box = None
        self.texts = []

        screen.addstr(y, x, label)
        screen.addstr(y, x+len(label), self.content)

    def on(self, *args) -> int:
        if(len(args) == 0):
            args = ["\n", "KEY_ENTER"]

        self.screen.addstr(self.y, self.x, self.label, curses.A_REVERSE)

        while(True):

            key_str = self.screen.getkey()
            
            self.screen.addstr(self.y, self.x, self.label)
            self.screen.addstr(self.y, self.x+len(self.label), self.content)

            if key_str in args: 
                if not(key_str == "KEY_UP" or key_str == "KEY_DOWN" or key_str == "KEY_LEFT" or key_str == "KEY_RIGHT" or key_str in ["\n", "KEY_ENTER"]):
                    self.screen.addstr(self.y, self.x+len(self.label), self.content)
                    return key_str
                elif(key_str in ["\n", "KEY_ENTER"] and self.pos == 0):
                    self.screen.addstr(self.y, self.x, self.label)
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
                elif(key_str == "KEY_RIGHT" and self.pos > 0):
                    self.screen.addstr(self.y-1, self.x+len(self.label)+int(len(self.content)/2), "▲")
                    self.screen.addstr(self.y+1, self.x+len(self.label)+int(len(self.content)/2), "▼")
                    return key_str
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            if self.pos == 0:

                try:
                    self.box.delete()
                    for text in self.texts:
                        text.delete()
                    self.texts = []
                except:
                    pass

                self.screen.addstr(self.y, self.x, self.label, curses.A_REVERSE)
                self.screen.addstr(self.y, self.x+len(self.label), self.content)
            else:
                self.screen.addstr(self.y, self.x+len(self.label), " "*len(self.content))

                self.box = Box(self.screen, self.x+len(self.label), self.y, len(max(self.options,key=len))+2, len(self.options)+2)

                for i, option in enumerate(self.options):
                    if(i == self.pos-1):
                        self.texts.append(Text(self.screen, self.x+len(self.label)+1, self.y+i+1, str(option), curses.A_REVERSE))
                    else:
                        self.texts.append(Text(self.screen, self.x+len(self.label)+1, self.y+i+1, str(option)))


            self.screen.refresh()

    def handle_key(self, key_str):
        pos = self.pos

        if(key_str in ["\n", "KEY_ENTER"]):
            self.content = self.options[pos-1]
            self.pos = 0

        elif(key_str == "KEY_RIGHT"):
            if (pos == 0):
                self.pos += 1

        elif(key_str == "KEY_LEFT"):
            if not (pos == 0):
                self.pos = 0
                
        elif(key_str == "KEY_UP"):
            if (pos > 1):
                self.pos -= 1

        elif(key_str == "KEY_DOWN"):
            if (pos < len(self.options)):
                self.pos += 1

    def move(self, x ,y):
        try:
            self.box.move(x, y)
            for text in self.texts:
                text.move(x, y)
        except:
            pass

        self.screen.addstr(self.y, self.x, " "*len(self.label))
        self.screen.addstr(y, x, self.label)

        self.x = x
        self.y = y

    def delete(self):

        try:
            self.box.delete()
            for text in self.texts:
                text.delete()
        except:
            pass

        self.screen.addstr(self.y, self.x, " "*len(self.label))

        del self