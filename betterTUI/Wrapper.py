import curses
from typing import Any, Callable
from betterTUI import Screen

class Wrapper:
    def __init__(self, screen: Screen, start_pos: list, widgets: list):
        self.screen = screen
        self.matrix = widgets
        self.pos = start_pos

    def on(self, *args) -> int:
        self.on = True

        while(self.on == True):
            childArgs = args
            if (self.pos[0] > 0):
                childArgs += ("KEY_UP", )
            if (self.pos[0] < len(self.matrix)-1):
                childArgs += ("KEY_DOWN", )
            if (self.pos[1] > 0):
                childArgs += ("KEY_LEFT", )
            if (self.pos[1] < len(self.matrix[self.pos[0]])-1):
                childArgs += ("KEY_RIGHT", )
            
            childArgs += ("\n", "KEY_ENTER", )

            key_str = self.matrix[self.pos[0]][self.pos[1]][0].on(*childArgs)

            if key_str in args:
                if not(key_str == "KEY_RIGHT" or key_str == "KEY_LEFT" or key_str == "KEY_UP" or key_str == "KEY_DOWN"):
                    return key_str
                elif(key_str == "KEY_UP" and self.pos[0] == 0):
                    return key_str
                elif(key_str == "KEY_DOWN" and self.pos[0] == len(self.matrix)-1):
                    return key_str
                elif(key_str == "KEY_LEFT" and self.pos[1] == 0):
                    return key_str
                elif(key_str == "KEY_RIGHT" and self.pos[1] == len(self.matrix[self.pos[0]])-1):
                    return key_str
                else:
                    res = self.handle_key(key_str)
                    if(res):
                        return res
            else:
                res = self.handle_key(key_str)
                if(res):
                    return res

            self.screen.refresh()

    def handle_key(self, key_str):
        pos = self.pos

        if(key_str in ("\n", "KEY_ENTER")):
            return self.matrix[self.pos[0]][self.pos[1]]

        elif(key_str == "KEY_UP"):
            if not (pos[0] == 0):
                self.pos[0] -= 1

                if(pos[1] > len(self.matrix[self.pos[0]]) - 1):
                    self.pos[1] = len(self.matrix[self.pos[0]]) -1

        elif(key_str == "KEY_DOWN"):
            if not (pos[0] == len(self.matrix)-1):
                self.pos[0] += 1

                if(pos[1] > len(self.matrix[self.pos[0]]) - 1):
                    self.pos[1] = len(self.matrix[self.pos[0]]) - 1

        elif(key_str == "KEY_LEFT"):
            if not (pos[1] == 0):
                self.pos[1] -= 1

        elif(key_str == "KEY_RIGHT"):
            if not (pos[1] == len(self.matrix[self.pos[0]])-1):
                self.pos[1] += 1

    def insert(self, insert_pos: list, widget: Any, func: Callable):
        if(len(self.matrix)-1 < insert_pos[0]):
            self.matrix += ([(widget, func)], )
        else:
            self.matrix[insert_pos[0]].insert(insert_pos[1], (widget, func))

    def delete(self):
        for list in self.matrix:
            for element in list:
                element[0].delete()

        self.on = False

        del self