from betterTUI import *
from screens import *

def main(screen):
    curses.curs_set(0)
    screen.box()

    elements = home(screen, None)

    while(True):

        wrapper = Wrapper(screen, [0,0], *elements)
        res = wrapper.on('ALT_Q')

        screen.clear()
        wrapper.delete()

        if(res in ['ALT_Q']): break
        else: elements = res[1](screen, res[0])
        screen.box()

Screen(main)