import EasyDraw as ed
import random
import math

outside_radius = 250
inside_radius = 200

def setup(app):
    c = app.canvas

    c.translate(400, 400)
    app.fill_color = app.color.random()
    c.stroke_width(3)
    c.stroke('#ffffff')
    app.angle = 0

def draw(app):
    c = app.canvas

    num_points = math.floor(app.tools.map(app.mouse_left, 0, app.width, 6, 60))
    angle = 0
    angle_step = 180.0 / num_points

    c.fill(app.fill_color)
    c.begin_shape()
    for i in range(0, num_points):
        px = math.cos(math.radians(angle)) * outside_radius
        py = math.sin(math.radians(angle)) * outside_radius
        angle += angle_step
        c.vertex(px, py)
        px = math.cos(math.radians(angle)) * inside_radius
        py = math.sin(math.radians(angle)) * inside_radius
        c.vertex(px, py)
        angle += angle_step
    c.end_shape()

    c.fill('black')
    c.circle(0, 0, 150)

    app.angle += 1

    c.rotate(app.angle)

ed.EasyDraw(width = 800,
        height = 800,
        fps = 60,
        background = 'black',
        title = 'Polygon',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
