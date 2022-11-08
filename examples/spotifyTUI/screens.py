import betterTUI

def custom_exit(screen, child_obj):
    exit()

def home(screen, child_obj):

    max_y, max_x = screen.getmaxyx()

    quit_button = (betterTUI.Button(screen, 2, 2, "Quit"), custom_exit)
    search_bar = (betterTUI.SearchBar(screen, int(max_x/2-30), 2, 30, "Search Song:", "Go"), custom_exit)

    elements = [[quit_button, search_bar]]
    return elements