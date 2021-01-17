from EasyDraw import EasyDraw
from EasyDraw.Vector import Vector
from opensimplex import OpenSimplex

import random
import math

width = 600
height = 600

count = 15
dist = width // (count - 1)

noise_inc = 0.5
os = OpenSimplex(seed=1)

def bin2dec(a, b, c, d):
    return a*8 + b*4 + c*2 + d*1

def setup(app):
    app.zoff = 0

def draw(app):
    app.points = []
    xoff = 0
    for i in range(0, count):
        xoff += noise_inc
        yoff = 0
        app.points.append([])
        for j in range(0, count):
            app.points[i].append(os.noise3d(x=xoff, y=yoff, z = app.zoff))
            yoff += noise_inc
    
    app.zoff += 0.01

    app.canvas.stroke('white')
    for i in range(0, count):
        for j in range(0, count):
            if app.points[i][j] == 1:
                app.canvas.fill('white')
            else:
                app.canvas.fill('black')
            app.canvas.circle(i * dist, j * dist, 2)

    app.canvas.stroke_width(2)

    for i in range(0, count - 1):
        for j in range(0, count - 1):
            x = i * dist
            y = j * dist

            a = Vector(x + dist * 0.5, y)
            b = Vector(x + dist      , y + dist * 0.5)
            c = Vector(x + dist * 0.5, y + dist)
            d = Vector(x             , y + dist * 0.5)

            val = bin2dec(math.ceil(app.points[i][j]),
                    math.ceil(app.points[i + 1][j]),
                    math.ceil(app.points[i + 1][j + 1]),
                    math.ceil(app.points[i][j + 1]))

            if val == 1:
                app.canvas.line(c, d)
            elif val == 2:
                app.canvas.line(c, b)
            elif val == 3:
                app.canvas.line(b, d)
            elif val == 4:
                app.canvas.line(a, b)
            elif val == 5:
                app.canvas.line(a, d)
                app.canvas.line(b, c)
            elif val == 6:
                app.canvas.line(a, c)
            elif val == 7:
                app.canvas.line(a, d)
            elif val == 8:
                app.canvas.line(a, d)
            elif val == 9:
                app.canvas.line(a, c)
            elif val == 10:
                app.canvas.line(a, b)
                app.canvas.line(c, d)
            elif val == 11:
                app.canvas.line(a, b)
            elif val == 12:
                app.canvas.line(b, d)
            elif val == 13:
                app.canvas.line(b, c)
            elif val == 14:
                app.canvas.line(c, d)
            
            

            

EasyDraw(width = width,
         height = height,
         fps = 30,
         title = 'Marching Squares',
         background = 'black',
         setupFunc = setup,
         autoClear = True,
         drawFunc = draw)
