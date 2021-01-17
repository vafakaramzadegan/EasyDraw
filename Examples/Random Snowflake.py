from EasyDraw import EasyDraw
from EasyDraw.Vector import Vector
from EasyDraw.Color import RGB

import random
import math

width = 600
height = 600

particle_radius = 10
particle_range_of_motion = 10
snowflake_sides = 6

center_pos = Vector(0, 0)

class Particle:
    def __init__(self, app):
        self.app = app
        self.pos = Vector(width // 2, 0)
        self.collided = False

    def move(self):
        self.pos.x -= 1
        self.pos.y += random.randint(-particle_range_of_motion, particle_range_of_motion)

        if self.pos.heading() < -45:
            self.pos.y += particle_range_of_motion

        if self.pos.heading() > 0:
            self.pos.y -= particle_range_of_motion

        for p in self.app.points[:-1]:
            if p.pos.distance_from(self.pos) <= (particle_radius * 2):
                self.collided = True

    def draw(self):
        r = math.floor(self.app.tools.map(self.pos.distance_from(center_pos), 0, width // 2, 0, 255))
        
        color = RGB(r, r, 255)

        self.app.canvas.fill(color)
        self.app.canvas.stroke(color)
        self.app.canvas.circle(self.pos.x, self.pos.y, particle_radius)

def setup(app):
    app.canvas.translate(width // 2, height // 2)
    app.points = []
    app.points.append(Particle(app))


def draw(app):
    p = app.points[-1]

    while p.pos.x > 0 and p.collided == False:
        p.move()

    app.points.append(Particle(app))

    for p in app.points:
        for i in range(snowflake_sides):
            app.canvas.rotate(i * (360/snowflake_sides))
            p.draw()
            app.canvas.flip('y')
            p.draw()


EasyDraw(width = width,
        height = height,
        fps = 30,
        background = 'black',
        title = 'Snowflake',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
