import curses

from betterTUI.Screen import Screen
from betterTUI.Basic import Input, Button

class SearchBar:
    def __init__(self, screen: Screen, x: int, y: int, width: int, input_label: str, button_label: str, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.input_label = input_label
        self.content = ""
        self.pos = 0
        self.parent = None

        if(width < len(button_label)+1):
            raise Exception("SearchBar: width to small!")

        self.input = Input(screen, x, y, width-(len(button_label)+1), input_label, *args)
        self.input.parent = self

        self.button = Button(screen, x+width-(len(button_label)+1), y+1, button_label, *args)
        self.button.parent = self

    def on(self, *args) -> int:

        while(True):
            if(self.pos == 0):
                key_str = self.input.on("KEY_RIGHT", *args)
                self.content = self.input.content
            elif(self.pos == 1):
                key_str = self.button.on("KEY_LEFT", *args)

            if key_str in args:
                if not(key_str == "KEY_RIGHT" or key_str == "KEY_LEFT"):
                    return key_str
                elif(key_str == "KEY_RIGHT" and self.pos == 1):
                    return key_str
                elif(key_str == "KEY_LEFT" and self.pos == 0):
                    return key_str
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            self.screen.refresh()


    def handle_key(self, key_str):
        pos = self.pos

        if(key_str == "KEY_RIGHT"):
            # TRAVEL INPUT TO RIGHT
            if not (pos == 1):
                self.pos += 1

        elif(key_str == "KEY_LEFT"):
            # TRAVEL INPUT TO LEFT
            if not (pos == 0):
                self.pos -= 1


    def delete(self):
        self.input.delete()
        self.button.delete()

        del self