#!/usr/bin/env python3

from betterTUI import *

def home(screen, child_obj=None):
    text_area = (TextArea(screen, 2, 1, 60, 15, "Text Area:", commands={"table": ["Header 1 | Header 2", "Data 1 | Data 2"], "li": ["*"], "h1": ["**"]}, content=["ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDE-", "FGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ", "", "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"]), vault)

    # text_area[0].move(10, 10)
    button = (Button(screen, 14, 20, "ENTER VAULT", color=screen.COLOR_BLUE), vault)

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
