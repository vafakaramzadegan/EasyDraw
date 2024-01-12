# EasyDraw - Professional Documentation

Welcome to EasyDraw, an advanced graphical library designed for visual arts. Built on top of Tkinter, EasyDraw offers enhanced functionalities, making it an excellent choice for artists and developers alike.

![Rotating Polygon](https://raw.githubusercontent.com/vafakaramzadegan/EasyDraw/master/images/rotating-polygon.gif)

- [EasyDraw - Professional Documentation](#easydraw---professional-documentation)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Coordinate System](#coordinate-system)
  - [Callbacks](#callbacks)
    - [Mouse Moving on Canvas](#mouse-moving-on-canvas)
    - [Mouse Click](#mouse-click)
    - [KeyPress and KeyRelease Events](#keypress-and-keyrelease-events)
  - [Canvas Properties](#canvas-properties)
    - [Clearing Canvas](#clearing-canvas)
    - [Push and Pop Methods](#push-and-pop-methods)
    - [Transforming Coordinates](#transforming-coordinates)
    - [Rotating Canvas](#rotating-canvas)
    - [Flipping Canvas](#flipping-canvas)
    - [Zoom](#zoom)
    - [Font Family and Color](#font-family-and-color)
    - [Writing Text on Canvas](#writing-text-on-canvas)
    - [Drawing Image on Canvas](#drawing-image-on-canvas)
    - [Fill and Stroke Colors](#fill-and-stroke-colors)
    - [Stroke Width](#stroke-width)
    - [Creating Shapes and Lines](#creating-shapes-and-lines)
      - [Circle](#circle)
      - [Rectangle](#rectangle)
      - [Polygon](#polygon)
      - [Triangle](#triangle)
      - [Arc](#arc)
      - [Line](#line)
        - [Getting the Value of a Pixel](#getting-the-value-of-a-pixel)
    - [Colors](#colors)
    - [Vectors - Simplifying Geometry Operations](#vectors---simplifying-geometry-operations)
      - [Random Vector](#random-vector)
      - [Create a Vector from an Angle](#create-a-vector-from-an-angle)


## Requirements
To utilize EasyDraw, ensure that you have the required dependencies installed. EasyDraw automatically installs the necessary packages: `Pillow`, `multipledispatch`, and `pyscreenshot`.

## Installation
Get started with EasyDraw effortlessly using the following **pip** command:

```bash
$ python3 -m pip install --upgrade EasyDraw
```

If you have a previous version installed, running this command will seamlessly upgrade EasyDraw.

## Getting Started
EasyDraw simplifies the process of visualizing your ideas on a 2D canvas. Begin by importing the library:

```python
from EasyDraw import EasyDraw
```

Declare two functions, `setup` and `draw`, to initialize and handle animations, respectively.

```python
def setup(app):
    ''' Write your setup code here.
        This function executes once on app launch. '''
    
def draw(app):
    ''' Codes written here execute in each frame, allowing you to create animations. '''
```

Create an instance of the EasyDraw class:

```python
EasyDraw(
    width=800,
    height=800,
    fps=30,
    background='black',
    exportPath='/path/to/your/file.gif',
    title='App Title',
    autoClear=True,
    fullscreen=True,
    showStats=True,
    setupFunc=setup,
    drawFunc=draw
)
```

## Coordinate System
EasyDraw provides a canvas where the top-left pixel is (0, 0), and values increase going down to the bottom right. Customize the origin using the `translate(x, y)` command. Alternatively, define boundaries and change the Domain and Range:

```python
EasyDraw(
    ...
    bounds=(-5, -5, 5, 5),
    showGrid=True
    ...
)
```

## Callbacks
Define callbacks to capture mouse and keyboard events:

### Mouse Moving on Canvas
```python
def motion(app):
    # Mouse position relative to the top-left pixel of the canvas
    print(app.mouse_left, app.mouse_top)
    # Mouse position relative to the canvas center when translation is applied
    print(app.mouse_x, app.mouse_y)

EasyDraw(
    ...
    mouseMoveFunc=motion
    ...
)
```

### Mouse Click
```python
def mouseClick(app, button):
    # Access mouse position from "app" parameter
    # "button" parameter indicates which button was pressed: "left", "middle", or "right"
    ...

EasyDraw(
    ...
    clickFunc=mouseClick
    ...
)
```

### KeyPress and KeyRelease Events
```python
def keyPress(app, e):
    # Access key information from the "e" parameter
    print(e)
    ...

def keyRelease(app, e):
    # Access key information from the "e" parameter
    print(e)
    ...

EasyDraw(
    ...
    keyPressFunc=keyPress,
    keyReleaseFunc=keyRelease
    ...
)
```

## Canvas Properties
Manipulate the canvas using the `app.canvas` object. For Tkinter's default methods, use `app.canvas.handle`.

### Clearing Canvas
Use the `clear()` method to delete objects on the canvas. Pass `'all'` as an argument to delete all objects or a specific reference.

```python
app.canvas.clear('all')

circle = app.canvas.circle(0, 0, 100)
app.canvas.clear(circle)
```

### Push and Pop Methods
`push()` saves current styles and transformations, while `pop()` restores them.

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

### Transforming Coordinates
Move the origin using `app.canvas.translate(new_x, new_y)`.

```python
app.canvas.translate(200, 200)
```

### Rotating Canvas
Rotate the canvas and all its elements.

```python
app.canvas.rotate(45)
```

### Flipping Canvas
Flip the canvas vertically, horizontally, or both.

```python
# Horizontal
app.canvas.flip('x')
# Vertical
app.canvas.flip('y')
# Both
app.canvas.flip('xy')
```

### Zoom
Apply a zoom value to scale all canvas elements.

```python
app.canvas.zoom(2)
```

### Font Family and Color
Specify the font family and color.

```python
app.canvas.font_family('Tahoma 20 italic bold')
app.canvas.font_color('white')
app.canvas.font_color('#000000')
app.canvas.font_color(app.color.rgb(255, 0, 0))
app.canvas.font_color(app.color.hsv(100, 200, 255))
```

### Writing Text on Canvas
Use the `text` method to write text on the canvas.

```python
app.canvas.text(100, 100, 'Hello World!')
```

### Drawing Image on Canvas
Load and draw an image on the canvas.

```python
# Absolute position
app.canvas.create_image(int x, int y, path_to_file)

# Using vector
app.canvas.create_image(Vector v, path_to_file)

v = Vector(100, 100)
app.canvas.create_image(v, "/path/to/an/image.jpeg")
```

Change the scale if needed:

```python
app.canvas.create_image(0, 0, 'c:\my_img.png', scale=0.5)
```

### Fill and Stroke Colors
Specify fill and stroke colors for shapes.

```python
app.canvas.fill(COLOR)
app.canvas.stroke(COLOR)
```

### Stroke Width
Alter the width/thickness of strokes.

```python
app.canvas.stroke_width(2)
```

### Creating Shapes and Lines
Create various shapes using EasyDraw's intuitive methods:

#### Circle
```python
app.canvas.circle(0, 0, 100)
```

#### Rectangle
```python
app.canvas.rect(0, 0, 100, 100)
```

#### Polygon
Create custom shapes by defining vertices.

```python
c = app.canvas

c.begin_shape()
c.vertex(0, 0)
c.vertex(100, 0)
c.vertex(100, 100)
c.vertex(0, 100)
c.end_shape()
```

#### Triangle
Draw a triangle by defining the vertices.

```python
app.canvas.triangle(0, -20, 20, 20, -20, 20)
```

#### Arc
Draw an arc on the canvas.

```python
app.canvas.arc(-30, 30, 30, -30, 0, 180)
```

#### Line
Create lines using coordinates or vectors.

```python
# Between two coordinates
app.canvas.line(0, 0, 100, 100)

# Between two vectors
app.canvas.line(Vector(0, 0), Vector(100, 100))

# From the origin to a vector
app.canvas.line

#### Pixels and Color Manipulation

EasyDraw provides powerful methods for manipulating pixels on the canvas and supports various color representation formats.

##### Setting a Pixel
Set a pixel value using the following:

```python
app.canvas.point(int x, int y, color)

# Absolute position
app.canvas.point(20, 40, 'red')

# Vector position
v = Vector(100, 200)
app.canvas.point(v, RGB(0, 255, 0))
```

##### Getting the Value of a Pixel
Retrieve the RGB value of a pixel with:

```python
app.canvas.get_pixel(int x, int y)
```

The returned value is a tuple of RGB values: `(Red, Green, Blue)`.

### Colors
EasyDraw provides multiple methods for defining colors, including RGB, HSV, and random colors.

```python
from EasyDraw.Color import RGB, HSV, RandomColor

# Fill with RGB color
app.canvas.fill(RGB(255, 0, 0))
app.canvas.circle(0, 0, 100)

# Fill with HSV color
app.canvas.fill(HSV(150, 200, 255))
app.canvas.rect(0, 0, 100, 100)

# Fill with a random color
app.canvas.fill(RandomColor())
app.canvas.rect(100, 100, 200, 200)
```

### Vectors - Simplifying Geometry Operations
![Vector car](https://raw.githubusercontent.com/vafakaramzadegan/EasyDraw/master/images/vector_car.gif)

EasyDraw supports vector operations, simplifying geometric calculations.

```python
from EasyDraw.Vector import Vector

v1 = Vector(0, 0)
v2 = Vector(200, 0)
v3 = Vector(-100, -100)

# Vector addition
print(v1 + v2)
# Vector subtraction
print(v1 - v2)
# Dot product
print(v1 * v2)
# Negation
print(-v1)
# Accessing vector components
print(v1.x, v1.y)
```

Retrieve useful information about vectors:

```python
v1 = Vector(200, 0)
v2 = Vector(0, -200)

# Vector length
print(v1.length())
# or
print(v1.mag())

# Squared vector magnitude
print(v1.mag_square())

# Angle between v1 and v2
print(v1.angle_between(v2))

# Distance between v1 and v2
print(v1.distance_from(v2))

# Heading angle of v1
print(v1.heading)

# Linear interpolation between two vectors
v1.lerp(v2, 0.5)
```

Vector manipulation is also possible:

```python
vec = Vector(200, 0)

# Get a copy of a vector
vec2 = vec1.copy()

# Set vector magnitude
vec.set_mag(0.5)

# Limit vector length to a value
vec.limit(20)

# Normalize a vector
vec.normalize()
```

#### Random Vector
Generate a random unit vector:

```python
from EasyDraw.Vector import RandomVector

# A random unit vector with a length of 1
# All vector operations can be applied to a RandomVector
vec = RandomVector()
```

#### Create a Vector from an Angle
Create a vector from a specific angle:

```python
from EasyDraw.Vector import VectorFromAngle

# Creates a 45-degree vector with a length of 1
vec = VectorFromAngle(45)

# Set the length of a vector
# Creates a 90-degree vector with a length of 10
vec = VectorFromAngle(90, 10)
```