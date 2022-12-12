import curses
from betterTUI.Screen import Screen

class TextArea:
    def __init__(self, screen: Screen, x: int, y: int, width: int, height: int, label: str, color=0, commands={}, content=[""], *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.control = False
        self.controlStartPos = [0, 0]
        self.controlPos = 0
        self.controlMatches = []
        self.controlCommands = commands
        self.color = color

        for i, line in enumerate(content):
            if(len(line) > self.width-4):
                if not(line[self.width-3] == '-'):
                    content[i] = line[:self.width-3] + '-'
                    content.insert(i+1, line[self.width-3:])
                else:
                    content[i] = line[:self.width-2]
                    content.insert(i+1, line[self.width-2:])

        if(len(content[0]) > 0):
            self.content = content
        else:
            self.content = [""]
        self.pos = [0, 0]
        self.content_start = 0
        self.parent = None

        self.screen.attron(curses.color_pair(self.color))

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
            self.addstr(self.y+2+i, self.x+2, content)
            i += 1

        self.screen.attroff(curses.color_pair(color))

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

    def on(self, *args) -> int:

        self.addstr(self.y, self.x, self.label, True)
        
        self.screen.move(self.y+2+self.pos[1], self.x+2+self.pos[0])

        curses.curs_set(1)
        
        args += ("ALT_DOWN", )

        def exit_widget(key_str):
            self.addstr(self.y, self.x, self.label)
            curses.curs_set(0)
            return key_str

        while(True):

            key_str = self.screen.getkey()

            if key_str in args: 
                if not(key_str == "KEY_RIGHT" or key_str == "KEY_LEFT" or key_str == "KEY_DOWN" or key_str == "ALT_DOWN" or key_str == "KEY_UP" or key_str in ["\n", "KEY_ENTER"]):
                    return exit_widget(key_str)
                elif(key_str == "KEY_RIGHT") and (self.pos[0] == self.width-3):
                    return exit_widget(key_str)
                elif((key_str == "KEY_LEFT") and (self.pos[0] == 0)):
                    return exit_widget(key_str)
                elif((key_str == "KEY_UP") and (self.pos[1] == 0 and not self.control)):
                    return exit_widget(key_str)
                elif((key_str == "KEY_DOWN") and (self.pos[1] == len(self.content)-1 and not self.control)):
                    return exit_widget(key_str)
                elif((key_str == "ALT_DOWN")):
                    return exit_widget("KEY_DOWN")
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            for i in range(0, self.height-2):
                self.addstr(self.y+2+i, self.x+2, " "*(self.width-2))

            i = 0
            for content in self.content[self.content_start:self.height-2+self.content_start]:
                self.addstr(self.y+2+i, self.x+2, content)
                i += 1

            if (self.control):
                self.controlMatches = []
                content = self.content[self.controlStartPos[1]][self.controlStartPos[0]+1:].split(" ")[0]

                for k in self.controlCommands.keys():
                    if(k.startswith(content)):
                        self.controlMatches.append(k)
                if (len(self.controlMatches) > 0): 
                    max_len = len(max(self.controlMatches, key=len)) + 1
                    for i, key in enumerate(self.controlMatches):
                        rev = True
                        if (self.controlPos == i): rev = False
                        self.addstr(self.y+2+self.pos[1]+i+1, self.x+2+self.controlStartPos[0], " "+key+(" "*(max_len-len(key))), rev)

            self.screen.move(self.y+2+self.pos[1], self.x+2+self.pos[0])
            self.screen.move(self.y+2+self.pos[1], self.x+2+self.pos[0])

            self.screen.refresh()

    def handle_key(self, key_str):
        pos = self.pos
        combined_pos = self.pos[1] + self.content_start
        input_length = self.width-3
        input_height = self.height-3

        if(key_str in ["\b", "KEY_BACKSPACE"]):

            if (self.control):
                if(self.pos[0]-1 == self.controlStartPos[0]):
                    self.control = False

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
            if(self.control):
                if (self.controlPos > 0):
                    self.controlPos -= 1
            else:
                if (combined_pos > 0):
                    self.pos[0] = 0

                    if(pos[1] > 0):
                        self.pos[1] -= 1
                    else:
                        self.content_start -= 1

        elif(key_str == "KEY_DOWN"):
            
            if(self.control):

                if (self.controlPos < len(self.controlMatches)-1):
                    self.controlPos += 1

            else:
            
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

            if (self.control and self.pos[0]-1 == self.controlStartPos[0]):
                self.control = False
                line = self.content[self.controlStartPos[1]]

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

            if(self.control):
                try:
                    key = self.controlMatches[self.controlPos]
                    value = self.controlCommands[key]

                    line = self.content[self.controlStartPos[1]]
                    self.content[self.controlStartPos[1]] = line[0:self.controlStartPos[0]] + line[self.controlStartPos[0]+1+len(line[self.controlStartPos[0]+1:].split(" ")[0]):] 

                    for line in value[::-1]:
                        self.content.insert(self.controlStartPos[1], line)

                    self.control = False
                except:
                    self.control = False
            else:

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
                if (key_str == "/"):
                    self.control = True
                    self.controlStartPos = self.pos.copy()
                
                if(self.control):
                    self.controlPos = 0
                    if(key_str == " "):
                        self.control = False
                        line = self.content[self.controlStartPos[1]]
                                
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
            self.addstr(y+1, x+i, "─")
            self.addstr(y+self.height, x+i, "─")

        self.addstr(y+1, x, "┌")
        self.addstr(y+1, x+self.width, "┐")

        for i in range(1, self.height):
            self.addstr(y+1+i, x, "│")
            self.addstr(y+1+i, x+self.width, "│")

        self.addstr(y+self.height, x, "└")
        self.addstr(y+self.height, x+self.width, "┘")

        self.addstr(y, x, self.label)

        i = 0
        for content in self.content[self.content_start:self.height-2+self.content_start]:
            self.addstr(y+2+i, x+2, content)
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
