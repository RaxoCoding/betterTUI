import curses

from betterTUI.Screen import Screen

class TextArea:
    def __init__(self, screen: Screen, x: int, y: int, width: int, height: int, label: str, content=[""], *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label

        for i, line in enumerate(content):
            if(len(line) > self.width-4):
                content[i] = line[:self.width-3] + '-'
                content.insert(i+1, line[self.width-3:])

        if(len(content[0]) > 0):
            self.content = content
        else:
            self.content = [""]
        self.pos = [0, 0]
        self.content_start = 0
        self.parent = None

        for i in range(0, width+1):
            screen.addstr(y+1, x+i, "─")
            screen.addstr(y+height, x+i, "─")

        screen.addstr(y+1, x, "┌")
        screen.addstr(y+1, x+width, "┐")

        for i in range(1, height):
            screen.addstr(y+1+i, x, "│")
            screen.addstr(y+1+i, x+width, "│")

        screen.addstr(y+height, x, "└")
        screen.addstr(y+height, x+width, "┘")

        screen.addstr(y, x, label)

        i = 0
        for content in self.content[0:self.height-2]:
            self.screen.addstr(self.y+2+i, self.x+2, content)
            i += 1

    def on(self, *args) -> int:

        self.screen.addstr(self.y, self.x, self.label, curses.A_REVERSE)
        self.screen.move(self.y+2+self.pos[1], self.x+2+self.pos[0])
        curses.curs_set(1)

        args += ("ALT_DOWN", )

        while(True):
            key_str = self.screen.getkey()

            if key_str in args: 
                if not(key_str == "KEY_RIGHT" or key_str == "KEY_LEFT" or key_str == "KEY_DOWN" or key_str == "ALT_DOWN" or key_str == "KEY_UP" or key_str in ["\n", "KEY_ENTER"]):
                    self.screen.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif(key_str == "KEY_RIGHT") and (self.pos[0] == self.width-3):
                    self.screen.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif((key_str == "KEY_LEFT") and (self.pos[0] == 0)):
                    self.screen.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif((key_str == "KEY_UP") and (self.pos[1] == 0)):
                    self.screen.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif((key_str == "KEY_DOWN") and (self.pos[1] == len(self.content)-1)):
                    self.screen.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif((key_str == "ALT_DOWN")):
                    self.screen.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return "KEY_DOWN"
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            for i in range(0, self.height-2):
                self.screen.addstr(self.y+2+i, self.x+2, " "*(self.width-2))

            i = 0
            for content in self.content[self.content_start:self.height-2+self.content_start]:
                self.screen.addstr(self.y+2+i, self.x+2, content)
                i += 1

            self.screen.move(self.y+2+self.pos[1], self.x+2+self.pos[0])
            self.screen.refresh()

    def handle_key(self, key_str):
        pos = self.pos
        combined_pos = self.pos[1] + self.content_start
        input_length = self.width-3
        input_height = self.height-3

        if(key_str in ["\b", "KEY_BACKSPACE"]):

            # if not at the start
            if not([pos[0], combined_pos] == [0, 0]):

                if(pos[0] == 0):
                    
                    if(pos[1] > 0):
                        self.pos[1] -= 1
                    else:
                        self.content_start -= 1

                    combined_pos = self.pos[1] + self.content_start

                    self.pos[0] = len(self.content[combined_pos])

                    if(len(self.content[combined_pos+1]) == 0 and not combined_pos == 0):
                        self.content.pop(combined_pos+1)

                    elif(len(self.content[combined_pos]) == 0):
                        self.content[combined_pos] = self.content[combined_pos+1]
                        self.content.pop(combined_pos+1)

                    elif(self.content[combined_pos][-1] == '-'):
                        self.content[combined_pos] = self.content[combined_pos][:-1]
                        self.pos[0] -= 1

                else:

                    if(len(self.content[combined_pos]) == pos[0]):
                        self.pos[0] -= 1
                        self.content[combined_pos] = self.content[combined_pos][:-1]

                    else:
                        self.pos[0] -= 1
                        self.content[combined_pos] = self.content[combined_pos][:self.pos[0]] + self.content[combined_pos][self.pos[0]+1:]

        elif(key_str == "KEY_UP"):
            # TRAVEL INPUT TO UP
            if (combined_pos > 0):
                self.pos[0] = 0

                if(pos[1] > 0):
                    self.pos[1] -= 1
                else:
                    self.content_start -= 1

        elif(key_str == "KEY_DOWN"):

            if (combined_pos+1 < len(self.content)):
                self.pos[0] = 0

                if(pos[1] < input_height):
                    self.pos[1] += 1
                else:
                    self.content_start += 1

        elif(key_str == "KEY_RIGHT"):
            # TRAVEL INPUT TO RIGHT
            if (pos[0] < len(self.content[combined_pos])):
                self.pos[0] += 1

            elif(pos[0] == input_length and combined_pos+1 < len(self.content)):
                self.pos = [0, self.pos[1]+1]

        elif(key_str == "KEY_LEFT"):

            # TRAVEL INPUT TO LEFT
            if not([pos[0], combined_pos] == [0, 0]):
                if(pos[0] == 0):

                    if(pos[1] > 0):
                        self.pos[1] -= 1
                    else:
                        self.content_start -= 1
                    combined_pos = self.pos[1] + self.content_start

                    self.pos[0] = len(self.content[combined_pos])
                else:
                    self.pos[0] -= 1

        elif(key_str in ["\n", "KEY_ENTER"]):

            if(pos[0] == 0):
                self.content.insert(combined_pos, "")
                if(pos[1] < input_height):
                    self.pos[1] += 1
                else:
                    self.content_start += 1

            elif(pos[0] < len(self.content[combined_pos])):
                self.content.insert(self.pos[1], self.content[self.pos[1]][:pos[0]])

                if(pos[1] < input_height):
                    self.pos[1] += 1
                else:
                    self.content_start += 1
                combined_pos = self.pos[1] + self.content_start

                self.content[combined_pos] = self.content[combined_pos][pos[0]:]
                self.pos[0] = 0
            else:
                if(pos[1] < input_height):
                    self.pos[1] += 1
                else:
                    self.content_start += 1

                self.pos[0] = 0
                self.content.append("")

        elif(len(key_str) == 1):
            if(key_str.isprintable()):
                if (pos[0] < input_length):
                    if(len(self.content[combined_pos]) == pos[0]):
                        self.content[combined_pos] += key_str
                        self.pos[0] += 1
                    elif(len(self.content[combined_pos]) <= input_length):
                        self.content[combined_pos] = self.content[combined_pos][:self.pos[0]] + key_str + self.content[combined_pos][self.pos[0]:]
                        self.pos[0] += 1
                    else:
                        if(self.content[combined_pos][-1] == '-'):
                            if(len(self.content) > combined_pos+1):
                                if(len(self.content[combined_pos+1]) < input_length):
                                    self.content[combined_pos+1] = self.content[combined_pos][-2] + self.content[combined_pos+1]
                                else:
                                    self.content.insert(combined_pos+1, self.content[combined_pos][-2] + "-")
                            else:
                                self.content.insert(combined_pos+1, self.content[combined_pos][-2])

                            self.content[combined_pos] = self.content[combined_pos][:self.pos[0]] + key_str + self.content[combined_pos][self.pos[0]:-2]
                            self.pos[0] += 1
                            self.content[combined_pos] += '-'

                        else:
                            self.content.insert(combined_pos+1, self.content[combined_pos][-1])
                            
                            self.content[combined_pos] = self.content[combined_pos][:self.pos[0]] + key_str + self.content[combined_pos][self.pos[0]:-1]
                            self.pos[0] += 1

                            self.content[combined_pos] += '-'

                elif(pos[0] == input_length):
                    if not(self.content[combined_pos][-1] == '-'):
                        self.content[combined_pos] += '-'
                    else:
                        key_str += '-'

                    if not(key_str in ['-', '--']):
                        
                        self.content.insert(combined_pos+1, key_str)
                        
                        if(pos[1] < input_height):
                            self.pos[1] += 1
                        else:
                            self.content_start += 1

                        self.pos = [1, self.pos[1]]


    def move(self, x ,y):

        for i in range(0, self.width+1):
            self.screen.addstr(self.y+1, self.x+i, " ")
            self.screen.addstr(self.y+self.height, self.x+i, " ")

        self.screen.addstr(self.y+1, self.x, " ")
        self.screen.addstr(self.y+1, self.x+self.width, " ")

        for i in range(1, self.height):
            self.screen.addstr(self.y+1+i, self.x, " ")
            self.screen.addstr(self.y+1+i, self.x+self.width, " ")

        self.screen.addstr(self.y+self.height, self.x, " ")
        self.screen.addstr(self.y+self.height, self.x+self.width, " ")

        self.screen.addstr(self.y, self.x, " "*len(self.label))

        for i in range(0, self.height-2):
            self.screen.addstr(self.y+2+i, self.x+2, " "*(self.width-2))

        for i in range(0, self.width+1):
            self.screen.addstr(y+1, x+i, "─")
            self.screen.addstr(y+self.height, x+i, "─")

        self.screen.addstr(y+1, x, "┌")
        self.screen.addstr(y+1, x+self.width, "┐")

        for i in range(1, self.height):
            self.screen.addstr(y+1+i, x, "│")
            self.screen.addstr(y+1+i, x+self.width, "│")

        self.screen.addstr(y+self.height, x, "└")
        self.screen.addstr(y+self.height, x+self.width, "┘")

        self.screen.addstr(y, x, self.label)

        i = 0
        for content in self.content[self.content_start:self.height-2+self.content_start]:
            self.screen.addstr(y+2+i, x+2, content)
            i += 1

        self.x = x
        self.y = y

    def delete(self):

        for i in range(0, self.width+1):
            self.screen.addstr(self.y+1, self.x+i, " ")
            self.screen.addstr(self.y+self.height, self.x+i, " ")

        self.screen.addstr(self.y+1, self.x, " ")
        self.screen.addstr(self.y+1, self.x+self.width, " ")

        for i in range(1, self.height):
            self.screen.addstr(self.y+1+i, self.x, " ")
            self.screen.addstr(self.y+1+i, self.x+self.width, " ")

        self.screen.addstr(self.y+self.height, self.x, " ")
        self.screen.addstr(self.y+self.height, self.x+self.width, " ")

        self.screen.addstr(self.y, self.x, " "*len(self.label))

        for i in range(0, self.height-2):
            self.screen.addstr(self.y+2+i, self.x+2, " "*(self.width-2))

        del self