# easyTUI - collection of curses widgets for building TUI's

### Global Methods

```py
# initialize Any object
any = Any()

# (excludes: Screen) delete any object and all of its children
any.delete()
```

### Global Properties

* *screen* - Screen() object passed in when widget is initialized

## Screen()
the Screen object is where all widgets will be added and needs to be instantiated and passed on to widgets for them to show up. It includes all of the methods from the Window object in curses. (i.e. box(), addstr(), ...)

#### Methods

```py
# initialize Screen object
screen = Screen()

# close Screen object and all widgets in it
screen.close()

# example method from curses Window object
screen.box()
```

## Wrapper(screen: Screen, start_pos: list, *args: list)
the Wrapper object is special it helps you handle all of your widgets, moving between them, and trigerring their corresponding functions.
the Wrapper cannot handle normal widgets like "Text" its made to handle interactive objects which can be selected/clicked.
Wrapper object's can be used to handle switching screens, if you have 1 screen it can handle your whole TUI.

##### Arguments

* *screen* - Screen() Object
* *start_pos* - a list of 2 ints which represent the row and col of a widget to be "on" first (i.e. [2, 5] will turn "on" the object on the 2nd row and 5th col first)
* **args* - a 2D Matrix of widgets and their corresponding functions in a tuple (i.e [(input, func), (button_1, func_1)], [(button_2, func_2)])

##### Methods

```py
def func(child_obj, wrapper):
    Text(screen, child_obj.x, child_obj.y+3, "Clicked ^")

button = Button(screen, x, y, "Click Me 1!")
button_1 = Button(screen, x+15, y, "Click Me 2!")
button_2 = Button(screen, x+, y+6, "Click Me 3!")

# initialize Wrapper object
wrapper = Wrapper(screen, [0, 0], [(button, func), (button_1, func)], [(button_2, func)])

# insert widget after initilization
# insert: (insert_pos: list, widget: Any, func: (...) -> Any) -> None
# insert_pos is where the widget will be added in the matrix (row, col)
wrapper.insert([0, 2], button, button_func)

# turn wrapper on and recieve exit_key whenever wrapper is done
# on: (*args: Any) -> int
# args are the keys that when pressed, exit the wrapper and return the key
# if you provide no exit keys ENTER key will be the default exit
exit_key = wrapper.on("q", "Q")
```

## Simple Widgets

### Text(screen: Screen, x: int, y: int, content: str, *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Text will start on x-axis
* *y* - where Text will start on y-axis
* *content* - Text you want to display
* **args* - curses character cell attributes

### Line(screen: Screen, x: int, y: int, character: str, length: int = 0, vertical: bool = False, *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Line will start on x-axis
* *y* - where Line will start on y-axis
* *character* - character to draw the Line with
* *length=0* - length of the Line (0=max)
* *vertical=False* - if the Line is vertical or not
* **args* - curses character cell attributes

### Box(screen: Screen, x: int, y: int, width: int, height: int, *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Box will start on x-axis
* *y* - where Box will start on y-axis
* *width* - width of the Box
* *height* - height of the Box
* **args* - curses character cell attributes

### Input(screen: Screen, x: int, y: int, width: int, label: str, *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Input will start on x-axis
* *y* - where Input will start on y-axis
* *width* - width of the Input
* *label* - text for the Input label
* **args* - curses character cell attributes

##### Methods

```py
# initialize Input object
input = Input(screen, 5, 2, 30, "Input:")

# turn input on and recieve exit_key whenever input is done
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the input and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = input.on(key_codes().KEY_UP, key_codes().KEY_DOWN)
```

##### Properties

* *content* - the string currently saved in the Input

### Button(screen: Screen, x: int, y: int, label: str, *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Button will start on x-axis
* *y* - where Button will start on y-axis
* *label* - text for the Button label
* **args* - curses character cell attributes

##### Methods

```py
# initialize Button object
button = Button(screen, 5, 2, "Click Me!")

# turn button on and recieve exit_key whenever button is exited
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the button and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = button.on(key_codes().KEY_UP, key_codes().KEY_DOWN)
```

## Complex Widgets

### SearchBar(screen: Screen, x: int, y: int, width: int, input_label: str, button_label: str, *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where SearchBar will start on x-axis
* *y* - where SearchBar will start on y-axis
* *width* - width of the whole SearchBar (needs to atleast be bigger than len(button_label) + 1)
* *input_label* - text for the Input label
* *button_label* - text for the Button label
* **args* - curses character cell attributes

##### Methods

```py
# initialize SearchBar object
search_bar = SearchBar(screen, 5, 2, 20, "Search: ", "Enter")

# turn search_bar on and recieve exit_key whenever search_bar is exited
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the search_bar and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = search_bar.on(key_codes().KEY_LEFT, key_codes().KEY_RIGHT)
```

##### Properties

* *content* - the string currently saved in the SearchBar