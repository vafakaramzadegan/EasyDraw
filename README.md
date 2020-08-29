# EasyDraw
A graphical library build for visual arts. EasyDraw is built on top of tkinter and has more functionalities.


## Installation
EasyDraw can be installed with **pip**:

`python3 -m pip install EasyDraw`


## Using EasyDraw
EasyDraw helps you visualize your ideas easily on a 2D Canvas.

First, import the library:

```python
import EasyDraw as ed
```

now you need two functions:

```python
def setup(app):
    # write your setup codes
    # only executed once on app launch
    
def draw(app):
    # codes written in this function are executed
    # repeatedly in each frame, which allows you to 
    # create animations.

```

after defining the above functions, you should call EasyDraw class:

```python
ed.EasyDraw(width = 800, # width of the canvas
        height = 800, # height of the canvas
        fps = 30, # frames per second (1 - 1000)
        backgroundColor = 'black', # background color 
        title = 'App Title', # your app title
        autoClear = True, # clear canvas after each frame
        setupFunc = setup, # setup function callback
        drawFunc = draw) # draw function callback
```
