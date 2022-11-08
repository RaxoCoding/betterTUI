from betterTUI import *

def home(screen, child_obj=None):
    button = Button(screen, 3, 2, "ENTER VAULT")
    box = Box(screen, 2, 1, 20, 10)
    box.clear()

    button = (Button(screen, 14, 20, "ENTER VAULT"), vault)

    if(child_obj):
        print(child_obj.content)

    return [[button]]

def vault(screen, child_obj):

    searchbar = SearchBar(screen, 4, 2, 30, "Login: ", "Submit: ")

    return [[(searchbar, home)]]

def main(screen):
    curses.curs_set(0)
    screen.box()

    elements = home(screen)

    while(True):

        wrapper = Wrapper(screen, [0,0], *elements)
        res = wrapper.on('ALT_Q')

        screen.clear()
        wrapper.delete()

        if(res in ['ALT_Q']): break
        else: elements = res[1](screen, res[0])
        screen.box()

Screen(main)