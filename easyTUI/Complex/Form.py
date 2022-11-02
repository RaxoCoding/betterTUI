import curses

from easyTUI.Screen import Screen
from easyTUI.Basic import Input, Counter, Box, Button

class Form:
    def __init__(self, screen: Screen, x: int, y: int, button_label: str, inputs: list, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.button_label = button_label
        self.inputs = inputs
        self.content = [ None for x in range(0, len(inputs)) ]
        self.pos = 0
        self.parent = None

        padding = 0
        for input in inputs:
            if(hasattr(input, "on")):
                input.parent = self
                input.move(x, y+padding)

                padding += input.height + 2
            else:
                raise Exception("Form: inputs must have an 'on' method")

        padding = 0

        for input in inputs:
            if(hasattr(input, "on")):
                input.parent = self
                input.move(x, y+padding)

                padding += input.height + 2
            else:
                raise Exception("Form: inputs must have an 'on' method")

        button = Button(screen, x, y+padding, button_label, *args)
        button.parent = self

        self.inputs.append(button)

    def on(self, *args) -> int:

        while(True):
            childArgs = args
            if (self.pos > 0):
                childArgs += ("KEY_UP", )
            if (self.pos < len(self.inputs) - 1):
                childArgs += ("KEY_DOWN", )
            
            childArgs += ("\n", )

            key_str = self.inputs[self.pos].on(*childArgs)
            if key_str in args:
                if not(key_str == "KEY_UP" or key_str == "KEY_DOWN" or (key_str == "\n" and self.pos < len(self.inputs) - 1)):
                    return key_str
                elif(key_str == "KEY_UP" and self.pos == 0):
                    return key_str
                elif(key_str == "KEY_DOWN" and self.pos == len(self.inputs) - 1):
                    return key_str
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            self.screen.refresh()


    def handle_key(self, key_str):
        pos = self.pos
        if not(len(self.inputs) - 1 == pos):
            self.content[pos] = self.inputs[self.pos].content

        if(key_str == "\n"):
            if not (pos == len(self.inputs) - 1):
                self.pos += 1

        elif(key_str == "KEY_UP"):
            if not (pos == 0):
                self.pos -= 1

        elif(key_str == "KEY_DOWN"):
            if not (pos == len(self.inputs) - 1):
                self.pos += 1


    def delete(self):
        for input in self.inputs:
            input.delete()

        del self