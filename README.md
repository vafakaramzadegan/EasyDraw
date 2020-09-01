# EasyDraw
A graphical library built for visual arts. EasyDraw is built on top of tkinter and has more functionalities.

## Prerequisites
EasyDraw requires Pillow to be installed. this can be done using:

`python3 -m pip install --upgrade Pillow`

for more information, read the instructions [here!](https://pillow.readthedocs.io/en/stable/installation.html)

## Installation
EasyDraw can be installed with **pip**:

`python3 -m pip install EasyDraw`


## Using EasyDraw
EasyDraw helps you visualize your ideas easily on a 2D Canvas.

First, import the library:

```python
import EasyDraw as ed
```

Then, you simply need to declare two functions:

```python
def setup(app):
    ''' write your setup codes here. 
        This function only executes once on app launch. '''
    # move canvas center position
    app.canvas.translate(400, 400)
    # set fill value to a random color
    app.canvas.fill(app.color.random())
    # set stroke color to black
    app.canvas.stroke('black')
    # set stroke width
    app.canvas.stroke_width(2)
    
def draw(app):
    ''' codes written in this function are executed
        in each frame. This allows you to 
        create animations. '''
    # draw a rectangle
    app.canvas.rect(0, 0, 100, 100)
    # draw a circle
    app.canvas.circle(0, 0, 100)
    # rotate canvas
    app.canvas.rotate(90)
    # set a pixel value
    # RGB
    app.canvas.point(50, 50, app.color.rgb(255, 0, 0))
    # HSV
    app.canvas.point(50, 50, app.color.hsv(100, 255, 255))
    # HEX
    app.canvas.point(50, 50, '#ffffff')
    
    # you can build custom shapes:
    app.canvas.begin_shape()
    app.canvas.vertex(0, 0)
    app.canvas.vertex(100, 100)
    app.canvas.vertex(0, 100)
    app.canvas.vertex(0, 0)
    app.canvas.end_shape()
```

after declaring the functions, create an instance of EasyDraw class:

```python
ed.EasyDraw(width = 800, # width of the canvas
        height = 800, # height of the canvas
        fps = 30, # frames per second (1 - 1000)
        background = 'black', # background color
        exportPath = '/path/to/your/file.gif', # export all frames to a GIF file when app terminates
        title = 'App Title', # your app title
        autoClear = True, # clear canvas after each frame
        setupFunc = setup, # setup function callback
        drawFunc = draw) # draw function callback
```
