from easyTUI import *

def home(screen):
    line = Line(screen, 5, 0, "|", 0, True)
    button = Button(screen, 4, 2, "ENTER VAULT")
    wrapper = Wrapper(screen, [0, 0], [(button, vault)])
    wrapper.on("q", "Q")

def vault(wrapper, child_obj):
    screen = wrapper.screen
    screen.clear()
    wrapper.delete()

    input = Input(screen, 2, 2, 30, "Login: ")
    select = Select(screen, 2, 2, "Profession: ", ["Student", "Teacher", "News"])
    counter = Counter(screen, 2, 2, 0, 100, "Age: ")
    form = Form(screen, 4, 2, "Login", {'login': input, 'profession': select, 'age': counter})

    wrapper = Wrapper(screen, [0, 0], [(form, withdraw)])
    wrapper.on("q", "Q")

def withdraw(wrapper, child_obj):
    print(child_obj.content)
    screen = wrapper.screen
    screen.clear()
    wrapper.delete()
    

def main():
    screen = Screen()

    home(screen)
    
    screen.close()

main()
