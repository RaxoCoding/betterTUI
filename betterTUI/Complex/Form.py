import curses

from betterTUI.Screen import Screen
from betterTUI.Basic import Input, Counter, Box, Button

class Form:
    def __init__(self, screen: Screen, x: int, y: int, button_label: str, inputs: dict, extra_data={}, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.button_label = button_label
        self.inputs = inputs
        self.key_ind = [x for x in inputs.keys()]
        self.content = {}
        self.pos = 0
        self.parent = None

        for k, v in extra_data.items():
            self.content[k] = v

        padding = 0
        for input in inputs.values():
            if(hasattr(input, "on")):
                input.parent = self
                input.move(x, y+padding)

                padding += input.height + 2
            else:
                raise Exception("Form: inputs must have an 'on' method")

        padding = 0

        for input in inputs.values():
            if(hasattr(input, "on")):
                input.parent = self
                input.move(x, y+padding)

                padding += input.height + 2
            else:
                raise Exception("Form: inputs must have an 'on' method")

        button = Button(screen, x, y+padding, button_label, *args)
        button.parent = self

        self.inputs["submit"] = button
        self.key_ind.append("submit")

    def on(self, *args) -> int:

        while(True):
            childArgs = args
            if (self.pos > 0):
                childArgs += ("KEY_UP", )
            if (self.pos < len(self.inputs) - 1):
                childArgs += ("KEY_DOWN", )
            
            childArgs += ("\n", "KEY_ENTER", )

            key_str = self.inputs[self.key_ind[self.pos]].on(*childArgs)
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
            self.content[self.key_ind[self.pos]] = self.inputs[self.key_ind[self.pos]].content

        if(key_str in ["\n", "KEY_ENTER"]):
            if not (pos == len(self.inputs) - 1):
                self.pos += 1

        elif(key_str == "KEY_UP"):
            if not (pos == 0):
                self.pos -= 1

        elif(key_str == "KEY_DOWN"):
            if not (pos == len(self.inputs) - 1):
                self.pos += 1


    def delete(self):
        for input in self.inputs.values():
            input.delete()

        del self