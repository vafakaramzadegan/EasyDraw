from EasyDraw import EasyDraw
from EasyDraw.Vector import *
from EasyDraw.Tools import *
import math

WIDTH = 600
HEIGHT = 600

count = 10
r = (WIDTH // 2) - 64

def get_vector(i):
    angle = map(i, 0, count, 0, 360)
    v = VectorFromAngle(angle)
    v.set_mag(-r)
    return v

def setup(app):
    app.canvas.translate(WIDTH // 2, HEIGHT // 2)
    app.canvas.stroke('yellow')

def draw(app):
    global count

    c = app.canvas

    c.no_fill()
    c.circle(0, 0, r)

    for i in range(0, count):
        v1 = get_vector(i)
        v2 = get_vector(i * 2)
        c.line(v1, v2)

    count += 1


EasyDraw(width = WIDTH,
        height = HEIGHT,
        fps = 20,
        background = 'black',
        title = 'Cardioid',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
