from betterTUI import *

def home(screen):
    button = (Button(screen, 4, 2, "ENTER VAULT"), vault)

    return [[button]]

def vault(screen, child_obj):

    input = Input(screen, 2, 2, 30, "Login: ")
    select = Select(screen, 2, 2, "Profession: ", ["Student", "Teacher", "News"])
    counter = Counter(screen, 2, 2, 0, 100, "Age: ")
    form = Form(screen, 4, 2, "Login", [input, select, counter])

    return [(form, home)]

def main():
    screen = Screen()

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
    
    screen.close()

main()