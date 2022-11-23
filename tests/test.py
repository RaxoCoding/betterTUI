from betterTUI import *

def home(screen, child_obj=None):
    text_area = (TextArea(screen, 2, 1, 60, 15, "Text Area:", ["ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"]), vault)

    # text_area[0].move(10, 10)
    button = (Button(screen, 14, 20, "ENTER VAULT"), vault)

    return [[text_area], [button]]

def vault(screen, child_obj):

    searchbar = SearchBar(screen, 4, 2, 30, "Login: ", "Submit: ")

    return [[(searchbar, home)]]

def main(screen):
    curses.curs_set(0)
    screen.box()

    elements = home(screen)

    while(True):
        wrapper = Wrapper(screen, [0,0], elements)
        res = wrapper.on('ALT_Q')

        screen.clear()
        wrapper.delete()

        if(res in ['ALT_Q']): break
        else: elements = res[1](screen, res[0])
        screen.box()

Screen(main)