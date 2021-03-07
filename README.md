# EasyDraw
A graphical library built for visual arts. EasyDraw is built on top of tkinter and has more functionalities.

EasyDraw is inspired by Processing.

![Rotating Polygon](https://raw.githubusercontent.com/vafakaramzadegan/EasyDraw/master/images/rotating-polygon.gif)

## Prequisites
EasyDraw requires `Pillow`, `multipledispatch` and `pyscreenshot`. these packages will be automatically installed along with EasyDraw.

## Installation
EasyDraw can be installed with **pip**:

`$ python3 -m pip install --upgrade EasyDraw`

If you already have previous versions installed, running the above command automatically upgrades EasyDraw.

## Using EasyDraw
EasyDraw helps you visualize your ideas easily on a 2D Canvas.

First, import the library:

```python
from EasyDraw import EasyDraw
```

Then, you simply need to declare two functions:

```python
def setup(app):
    ''' write your setup codes here. 
        This function only executes once on app launch. '''
    
def draw(app):
    ''' codes written in this function are executed
        in each frame. This allows you to 
        create animations. '''
```

The name of functions and their parameters can be anything of your choice.
After declaring the functions, simply create an instance of EasyDraw class:

```python
EasyDraw(
        # width of the window/canvas
        width = 800,
        # height of the window/canvas
        height = 800,
        # frames per second (1 - 1000)
        fps = 30,
        # background color
        background = 'black',
        # export all frames to a GIF file when app terminates
        exportPath = '/path/to/your/file.gif',
        # your app title
        title = 'App Title',
        # clear canvas after each frame
        autoClear = True,
        # switch to fullscreen view
        fullscreen = True,
        # show runtime information on screen
        showStats = True,
        # pass setup function callback
        setupFunc = setup,
        # pass draw function callback
        drawFunc = draw)
```

### Coordinate System
EasyDraw provides a canvas for drawing where the top left pixel is (0, 0). The values increase as you go down to bottom right pixel.
the origin can be changed using `translate(x, y)` command.

But, you can also define boundaries for the canvas and change the Domain and Range.
Consider having a 400x400 px canvas, setting the `bounds` as following divides the canvas to 10 horizontal and vertical units.
```python
EasyDraw(
        ...
        # (min x, min y, max y, max y)
        bounds = (-5, -5, 5, 5)
        # whether to show the Grid or not
        showGrid = True
        ...
        )
```


### Callbacks
You can also define a callbacks to get mouse/pointer information:

#### Mouse moving on canvas
```python
def motion(app):
    # position of mouse relative to top left pixel of canvas
    print(app.mouse_left)
    print(app.mouse_top)
    # position of mouse relative to canvas center when translation
    # is applied
    print(app.mouse_x)
    print(app.mouse_y)
    
EasyDraw(
        ...
        mouseMoveFunc = motion
        ...
        )
```

#### Mouse click
```python
def mouseClick(app, button):
    # you can access mouse position from "app" parameter
    # "button" parameter indicates which button was pressed
    # either of "left", "middle" or "right" is returned
    ...
    
EasyDraw(
        ...
        clickFunc = mouseClick
        ...
        )
```

#### Mouse button down
```python
def mouseButtonDown(app, button):
    # you can access mouse position from "app" parameter
    # "button" parameter indicates which button was pressed
    # either "left" or "right" is returned
    ...
    
EasyDraw(
        ...
        mouseDownFunc = mouseButtonDown
        ...
        )
```

#### Mouse button up
```python
def mouseButtonUp(app, button):
    # you can access mouse position from "app" parameter
    # "button" parameter indicates which button was released
    # either "left" or "right" is returned
    ...
    
EasyDraw(
        ...
        mouseUpFunc = mouseButtonUp
        ...
        )
```

#### KeyPress Event
```python
    def keyPress(app, e):
        print(e)
        ...
        
EasyDraw(
        ...
        keyPressFunc = keyPress
        ...
        )
```

#### keyRelease Event
```python
    def keyRelease(app, e):
        print(e)
        ...
        
EasyDraw(
        ...
        keyReleaseFunc = keyPress
        ...
        )
```

### Canvas property
The `app.canvas` allows you to access EasyDraw methods for canvas manipulation.
In case you want to use tkinter's default methods, use `app.canvas.handle`.

```python
app.canvas.handle.create_oval(x1, y1, x2, y2, ...)
```

#### Clearing Canvas
You can use `clear()` method to delete objects on canvas.
This invokes tkinter's `canvas.clear()` command directly.
you can whether pass `'all'` as the argument to delete all objects, or pass the refrence to a specific one.

```python
app.canvas.clear('all')

circle = app.canvas.circle(0, 0, 100)
app.canvas.clear(circle)
```

#### Push and Pop Methods
The `push()` function saves current styles and transformations, while `pop()` restores them,

```python
def draw(app):
    c = app.canvas
    
    c.translate(100, 100)
    c.line(0, 0, 100, 0)
    
    c.push()
    c.translate(0, 0)
    c.line(100, 100, 100, 200)
    c.pop()
```

#### Translating Coordinates
You can use this method to simply move the origin (0, 0) to a custom position:

`app.canvas.translate(int new_x, int new_y)`

the following command moves the origin to pixel 200, 200:

```python
app.canvas.translate(200, 200)
```

#### Rotating Canvas
This will rotate canvas and all elements on it:

`app.canvas.rotate(int deg)`

The following command represents a 45 degree rotation:

```python
app.canvas.rotate(45)
```

#### Flipping Canvas
You can flip canvas vertically and horizontally:

```python
# horizontal
app.canvas.flip('x')
# vertical
app.canvas.flip('y')
# both
app.canvas.flip('xy')
```
#### Zoom
You can apply a zoom value to scale all the elements of the canvas:
```python
# 2x magnification
app.canvas.zoom(2)
```

#### Font Family and color
You can specify font family and color as following:

```python
app.canvas.font_family('Tahoma 20 italic bold')
app.canvas.font_color('white')
app.canvas.font_color('#000000')
app.canvas.font_color(app.color.rgb(255, 0, 0))
app.canvas.font_color(app.color.hsv(100, 200, 255)
```

#### Writing text on Canvas
Use `text` method to write text on canvas:

```python
app.canvas.text(100, 100, 'Hello World!')
```

All text objects on the canvas have an `anchor` property which defines their alignment:
```python
# nw, n, ne, center, w, e, sw, s, se
app.canvas.text_anchor('nw')
```

#### Draw image on canvas
You can load an image from file and draw it on canvas:
```python
# using absolute position
app.canvas.create_image(int x, int y, path_to_file)

# using vector
app.canvas.create_image(Vector v, path_to_file)
```
You can also change the scale:

```python
app.canvas.create_image(0, 0, 'c:\my_img.png', scale = 0.5)
'''

#### Fill and Stroke colors
You can specify fill and stroke colors for shapes including: polygons, rectangles and circles.
This can be done using:

```python
app.canvas.fill(COLOR)
app.canvas.stroke(COLOR)
```

Colors can be defined in three ways. information on colors is available furthur down the page.

#### Stroke Width
The with/thickness of strokes can be altered as following:

```python
app.canvas.stroke_width(int val)
```

For example, this command sets the width to 2 pixels:
```python
app.canvas.stroke_width(2)
```

#### Creating Shapes and Lines
You can create a circle:

##### Circle

```python
app.canvas.circle(int x, int y, int radius)
```

This creates a circle with radius of 100 pixels on origin of canvas:

```python
app.canvas.circle(0, 0, 100)
```

##### Rectangle

```python
app.canvas.rect(int x1, int y1, int x2, int y2)
```

Creating a rectangle from 0, 0 to 100, 100:

```python
app.canvas.rect(0, 0, 100, 100)
```

##### Polygon

You can create custom shapes by defining vertices.

```python
app.canvas.begin_shape()
...
app.canvas.vertex(int x, int y)
...
app.canvas.end_shape()
```

This creates a rectangle:

```python
c = app.canvas

c.begin_shape()
c.vertex(0, 0)
c.vertex(100, 0)
c.vertex(100, 100)
c.vertex(0, 100)
c.end_shape()
```

##### Triangle
You can draw a triangle by defining the vertices:

```python
app.canvas.triangle(int x1, int y1, int x2, int y2, int x3, int y3)

app.canvas.triangle(0, -20, 20, 20, -20, 20)
```

##### Arc
Draw arc on canvas using following command:

```python
app.canvas.arc(int x1, int y1, int x2, int y2, int start, int extend)

app.canvas.translate(100, 100)
app.canvas.arc(-30, 30, 30, -30, 0, 180)
```

The outline color can be set with `app.canvas.stroke()` command. also the outline width can be set with `app.canvas.stroke_width()`.

##### Line
For creating lines, simply use:

```python
app.canvas.line(int x1, int y1, int x2, int y2)
```

you can also pass two vectors as start and end points:

```python
v1 = Vector(0, 0)
v2 = Vector(200, 0)

app.canvas.line(v1, v2)
```

#### Pixels
EasyDraw provides methods for manipulating pixels of the canvas.

##### Setting a Pixel
you can set a pixel value using:

```python
app.canvas.point(int x, int y, color)

app.canvas.point(20, 40, 'red')
```

#### Getting the value of a Pixel
You can get the RGB value of a pixel using:

```python
app.canvas.get_pixel(int x, int y)
```

The returning value is a tuple of RGB values: `(Red, Green, Blue)`

### Colors
In addition to HEX values and the locally defined standard color names, EasyDraw provides methods for defining RGB and HSV colors:

```python
from EasyDraw.Color import RGB, HSV, RandomColor

app.canvas.fill(RGB(255, 0, 0))
app.canvas.circle(0, 0, 100)

app.canvas.fill(HSV(150, 200, 255))
app.canvas.rect(0, 0, 100, 100)

app.canvas.fill(RandomColor())
app.canvas.rect(100, 100, 200, 200)
```

### Vectors
![Angle between two vectors](https://raw.githubusercontent.com/vafakaramzadegan/EasyDraw/master/images/vectors-angle.gif)

EasyDraw supports vector operations.

```python
from EasyDraw.Vector import Vector

v1 = Vector(0, 0)
v2 = Vector(200, 0)
v3 = Vector(-100, -100)

print(v1 + v2)
print(v1 - v2)
print(v1 * v2)
print(-v1)
print(v1.x, v1.y)
```

You can also get other useful information on vectors:

```python
v1 = Vector(200, 0)
v2 = Vector(0, -200)

# vector length
print(v1.length())
# or
print(v1.mag())

# suqared vector magnitude
print(v1.mag_square())

# angle between v1 & v2
print(v1.angle_between(v2))

# distance between v1 & v2
print(v1.distance_from(v2))

# heading angle of v1
print(v1.heading)

# get linear interpolation between two vectors
v1.lerp(v2, 0.5)
```

And, for vector manipulation:

```python
vec = Vector(200, 0)

# get a copy of a vector
vec2 = vec1.copy()

# set vector magnitude
vec.set_mag(0.5)

# limit vector length to a value
vec.limit(20)

# normalize a vector
vec.normalize()

```

####Random Vector

You can create a random unit vector:

```python
from EasyDraw.Vector import RandomVector

# a random unit vector with the length equals to 1
# all vector operations can be used on a RandomVector
vec = RandomVector()
```

####Create a vector from angle

You can create a vector from specific angle:

```python
from EasyDraw.Vector import VectorFromAngle

# creates a 45-degree vector with its length equal to 1
vec = VectorFromAngle(45)

# you can set the length of the vector
# this creates a 90-degree vector with a length of 10
vec = VectorFromAngle(90, 10)
```
