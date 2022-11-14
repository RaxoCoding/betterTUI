## Examples

### Music Player 
[Code](https://github.com/Gomez0015/betterTUI/tree/master/examples/musicPlayer)

![Demo_Screenshot](https://github.com/Gomez0015/betterTUI/blob/f7c04ba5d005b92d3084f69dbf703e725abc2346/examples/musicPlayer/image.png)

# betterTUI - collection of curses widgets for building TUI's

### Global Methods

```py
# initialize Any object
any = Any()

# (excludes: Screen) delete any object and all of its children
any.delete()
```

### Global Properties

* *screen* - Screen() object passed in when widget is initialized

## Screen(func: (screen: Any) -> None)
the Screen object is where all widgets will be added and needs to be instantiated and passed on to widgets for them to show up. It includes all of the methods from the Window object in curses. (i.e. box(), addstr(), ...)

#### Methods

```py
# initialize Screen object and pass it to func
Screen(func)

def func(screen):
    # example method from curses Window object
    screen.box()
```

## Wrapper(screen: Screen, start_pos: list, widgets: list)
the Wrapper object is special it helps you handle all of your widgets, moving between them, and returning their corresponding functions.
the Wrapper cannot handle normal widgets like "Text" its made to handle interactive objects which can be selected/clicked.
Wrapper object's can be used to handle switching screens, if you have 1 screen it can handle your whole TUI.

##### Arguments

* *screen* - Screen() Object
* *start_pos* - a list of 2 ints which represent the row and col of a widget to be "on" first (i.e. [2, 5] will turn "on" the object on the 2nd row and 5th col first)
* *widgets* - a 2D Matrix of widgets and their corresponding functions in a tuple (i.e [[(input, func), (button_1, func_1)], [(button_2, func_2)]])

##### Methods

```py
def func(child_obj, wrapper):
    Text(screen, child_obj.x, child_obj.y+3, "Clicked ^")

button = Button(screen, x, y, "Click Me 1!")
button_1 = Button(screen, x+15, y, "Click Me 2!")
button_2 = Button(screen, x+, y+6, "Click Me 3!")

# initialize Wrapper object
wrapper = Wrapper(screen, [0, 0], [[(button, func), (button_1, func)], [(button_2, func)]])

# insert widget after initilization
# insert: (insert_pos: list, widget: Any, func: (...) -> Any) -> None
# insert_pos is where the widget will be added in the matrix (row, col)
wrapper.insert([0, 2], button, button_func)

# turn wrapper on and recieve exit_key whenever wrapper is done
# on: (*args: Any) -> int
# args are the keys that when pressed, exit the wrapper and return the key
# if you provide no exit keys ENTER key will be the default exit
exit_func = wrapper.on("q", "Q")
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

##### Methods

```py
# initialize Box object
box = Box(screen, 4, 2, 30, 15)

# clear everything inside the box
box.clear()
```

### Input(screen: Screen, x: int, y: int, width: int, label: str, content: str = "", *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Input will start on x-axis
* *y* - where Input will start on y-axis
* *width* - width of the Input
* *label* - text for the Input label
* *content* - default Input content
* **args* - curses character cell attributes

##### Methods

```py
# initialize Input object
input = Input(screen, 5, 2, 30, "Input:")

# turn input on and recieve exit_key whenever input is done
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the input and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = input.on("KEY_UP", "KEY_DOWN")
```

##### Properties

* *content* - the string currently saved in the Input

### TextArea(screen: Screen, x: int, y: int, width: int, height: int, label: str, content: Any = [""], *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where TextArea will start on x-axis
* *y* - where TextArea will start on y-axis
* *width* - width of the TextArea
* *height* - height of the TextArea
* *label* - text for the TextArea label
* *content* - default TextArea content
* **args* - curses character cell attributes

##### Methods

```py
# initialize TextArea object
text_area = TextArea(screen, 5, 2, 30, 10, "TextArea:")

# turn text_area on and recieve exit_key whenever text_area is done
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the text_area and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = text_area.on("KEY_UP", "KEY_DOWN")
```

##### Properties

* *content* - the string currently saved in the Input

### File(screen: Screen, x: int, y: int, label: str, content: str = "", *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where File will start on x-axis
* *y* - where File will start on y-axis
* *label* - text for the File label
* *content* - default File content
* **args* - curses character cell attributes

##### Methods

```py
# initialize File object
file = File(screen, 5, 2, "File:")

# turn file on and recieve exit_key whenever file is done
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the file and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = file.on("KEY_UP", "KEY_DOWN")
```

##### Properties

* *content* - the string currently saved in the Input


### Counter(screen: Screen, x: int, y: int, min: int, max: int, label: str, content: str = "", *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Counter will start on x-axis
* *y* - where Counter will start on y-axis
* *min* - min number possible
* *max* - max number possible
* *label* - text for the Counter label
* *content* - default Counter content
* **args* - curses character cell attributes

##### Methods

```py
# initialize Counter object
counter = Counter(screen, 5, 2, -5, 15, "Counter: ")

# turn counter on and recieve exit_key whenever counter is done
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the counter and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = counter.on("KEY_UP", "KEY_DOWN")
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
exit_key = button.on("KEY_UP", "KEY_DOWN")
```

### Select(screen: Screen, x: int, y: int, label: str, options: list, content: str = "", *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where Select will start on x-axis
* *y* - where Select will start on y-axis
* *label* - text for the Select label
* *options* - options that can be selected
* *content* - default Selected option
* **args* - curses character cell attributes

##### Methods

```py
# initialize Select object
select = Select(screen, 5, 2, "Options: ", ["Option 1", "Option 2", "Option 3"])

# turn select on and recieve exit_key whenever select is exited
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the select and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = select.on("KEY_UP", "KEY_DOWN")
```

##### Properties

* *content* - the currently selected options

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
exit_key = search_bar.on("KEY_LEFT", "KEY_RIGHT")
```

##### Properties

* *content* - the string currently saved in the SearchBar

### Form(screen: Screen, x: int, y: int, button_label: str, inputs: dict, extra_data: dict, *args: Any)

##### Arguments

* *screen* - Screen() Object
* *x* - where SearchBar will start on x-axis
* *y* - where SearchBar will start on y-axis
* *button_label* - text for the submit Button label
* *inputs* - dict of the widgets to use in the Form and their keys (must have the "on" method)
* *extra_data* - dict of data and keys to pass after form is submitted ( think of it as a hidden input in HTML )
* **args* - curses character cell attributes

##### Methods

```py
# x and y of these objects don't matter, it will be moved
input_1 = Input(screen, 2, 2, 30, "Login: ")
input_2 = Input(screen, 2, 2, 30, "Password: ")
counter = Counter(screen, 2, 2, 0, 100, "Age: ")

# initialize Form object
form = Form(screen, 4, 2, "Login", {'login': input_1, 'password': input_2, 'age': counter})

# turn form on and recieve exit_key whenever form is exited
# on: (*args: Any) -> int
# args are the key_codes that when pressed, exit the form and return the key_code
# if you provide no exit keys ENTER key will be the default exit
exit_key = form.on("KEY_LEFT", "KEY_RIGHT")
```

##### Properties

* *content* - list of the input(s) content(s) in order

cats = gigachad