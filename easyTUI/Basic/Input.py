import curses

from easyTUI.Screen import Screen

class Input:
    def __init__(self, screen: Screen, x: int, y: int, width: int, label: str, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.label = label
        self.content = ""
        self.pos = 0
        self.parent = None

        for i in range(0, width+1):
            screen.addstr(y, x+i, "─")
            screen.addstr(y+2, x+i, "─")

        screen.addstr(y, x, "┌")
        screen.addstr(y, x+width, "┐")
        screen.addstr(y+1, x, "│")
        screen.addstr(y+1, x+width, "│")
        screen.addstr(y+2, x, "└")
        screen.addstr(y+2, x+width, "┘")

        screen.addstr(y-1, x, label)

    def on(self, *args) -> int:
        if(len(args) == 0):
            args = "\n"

        self.screen.addstr(self.y-1, self.x, self.label, curses.A_STANDOUT)
        self.screen.move(self.y+1, self.x+2+self.pos)
        curses.curs_set(1)

        while(True):
            key_str = self.screen.getkey()
            if key_str in args: 
                if not(key_str == "KEY_RIGHT" or key_str == "KEY_LEFT"):
                    self.screen.addstr(self.y-1, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif(key_str == "KEY_RIGHT" and self.pos == len(self.content)):
                    self.screen.addstr(self.y-1, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif(key_str == "KEY_LEFT" and self.pos == 0):
                    self.screen.addstr(self.y-1, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            self.screen.addstr(self.y+1, self.x+2, " "*(self.width-2))
            self.screen.addstr(self.y+1, self.x+2, self.content)
            self.screen.move(self.y+1, self.x+2+self.pos)
            self.screen.refresh()

    def handle_key(self, key_str):
        pos = self.pos
        content = self.content

        if(key_str  == "\b"):
            if(pos < len(content)):
                input_left = content[:pos]
                input_right = content[-(len(content)-pos):]
                print(input_left, input_right)
                input_left = input_left[:-1]

                self.content = input_left + input_right
                self.pos -=1
            elif (pos > 0):
                self.content = content[:-1]
                self.pos -=1

        elif(key_str == "KEY_RIGHT"):
            # TRAVEL INPUT TO RIGHT
            if not (pos == len(content)):
                self.pos += 1

        elif(key_str == "KEY_LEFT"):
            # TRAVEL INPUT TO LEFT
            if not (pos == 0):
                self.pos -= 1

        elif(key_str.isprintable()):
            if(pos < len(content)):
                input_left = content[:pos]
                input_right = content[-(len(content)-pos):]
                input_left += key_str
                
                self.content = input_left + input_right
                self.pos += 1
            elif (pos < self.width-3):
                self.content += key_str
                self.pos += 1

    def delete(self):
        for i in range(0, self.width+1):
            self.screen.addstr(self.y, self.x+i, " ")
            self.screen.addstr(self.y+2, self.x+i, " ")

        self.screen.addstr(self.y+1, self.x, " ")
        self.screen.addstr(self.y+1, self.x+self.width, " ")

        self.screen.addstr(self.y+1, self.x+2, " "*(self.width-2))
        self.screen.addstr(self.y-1, self.x, " "*len(self.label))

        del self