from easyTUI import *

def home(screen):
    button = Button(screen, 30, 5, "ENTER VAULT")
    Text(screen, 20, 8, "ENETER AT YOUR OWN RISK")

    wrapper = Wrapper(screen, [0, 0], [(button, vault)])
    wrapper.on("q", "Q")

def vault(wrapper, child_obj):
    screen = wrapper.screen
    screen.clear()
    wrapper.delete()

    search_bar = SearchBar(screen, 30, 5, 30, "Withdraw Amount:", "Enter")
    Box(screen, 30, 8, 30, 5)
    Text(screen, 45, 10, "100000$")

    wrapper = Wrapper(screen, [0, 0], [(search_bar, withdraw)])
    wrapper.on("q", "Q")

def withdraw(wrapper, child_obj):
    screen = wrapper.screen
    screen.clear()
    wrapper.delete()
    

def main():
    screen = Screen()
    screen.box()

    home(screen)

    screen.close()

main()