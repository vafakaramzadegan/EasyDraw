# EasyDraw
A graphical library built for visual arts. EasyDraw is built on top of tkinter and has more functionalities.

![Rotating Polygon](https://raw.githubusercontent.com/vafakaramzadegan/EasyDraw/master/images/rotating-polygon.gif)

## Prequisites
EasyDraw requires `Pillow` and `pyscreenshot`. these packages will be automatically installed along with EasyDraw.

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

You can also define a callback to get the position of mouse moving on the canavs:

```python
def motion(app):
    # position of mouse relative to top left pixel of canvas
    print(app.mouse_left)
    print(app.mouse_top)
    # position of mouse relative to canvas center when translation
    # is applied
    print(app.mouse_x)
    print(app.mouse_y)    
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
        # pass setup function callback
        setupFunc = setup,
        # pass draw function callback
        drawFunc = draw,
        # pass mouse move function callback
        motionFunc = motion)
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
app.canvas.fill(app.color.rgb(255, 0, 0)
app.canvas.circle(0, 0, 100)

app.canvas.fill(app.color.hsv(150, 200, 255)
app.canvas.rect(0, 0, 100, 100)
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
```

You can also find the angle between two vectors:

```python
v1 = Vector(200, 0)
v2 = Vector(0, -200)

print(v1.angle_between(v2))
```
