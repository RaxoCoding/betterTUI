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

    input = Input(screen, 2, 2, 30, "Login: ")
    select = Select(screen, 2, 2, "Profession: ", ["Student", "Teacher", "News"])
    counter = Counter(screen, 2, 2, 0, 100, "Age: ")
    form = Form(screen, 4, 2, "Login", {'login': input, 'profession': select, 'age': counter })

    return [[(form, home)]]

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