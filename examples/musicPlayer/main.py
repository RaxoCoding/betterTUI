from betterTUI import *
from screens import *
import globals, sys, time
globals.initialize()

def main(screen):
    
    curses.curs_set(0)

    screen.timeout(1000)

    state = home(screen, None)

    last_pos = [0,0]

    while(True):

        wrapper = Wrapper(screen, last_pos, state['elements'])

        res = None
        try:
            res = wrapper.on('ALT_Q')
        except:
            res = -1

        if not(res == -1):
            screen.clear()
            wrapper.delete()

            if(res in ['ALT_Q']): break
            else: state = res[1](screen, res[0])
        else:
            state = home(screen, None)
            last_pos = wrapper.pos

try:
    Screen(main)
except Exception as e:
    sys.exit(e)