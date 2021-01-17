from EasyDraw import EasyDraw
from EasyDraw.Vector import *
import random

WIDTH = 1000
HEIGHT = 600

dt = 0.1
c = 50
G = 100
total = 50

app_hdl = None


class Particle:
    def __init__(self, x, y, dir):
        self.position = Vector(x, y)
        self.velocity = Vector(dir*c, 0)
        self.acceleration = Vector(0, 0)
        self.mass = 0.0001
        self.stopped = False
        self.history = []
        self.dir = dir

    def applyForce(self, force):
        f = force / self.mass
        self.acceleration += f

    def update(self):
        if not self.stopped:
            self.history.append(self.position.copy())
            self.acceleration *= dt
            self.velocity += self.acceleration
            self.velocity.limit(c)
            deltaV = self.velocity.copy()
            deltaV = deltaV * dt
            self.position += deltaV
            self.acceleration *= 0

        if len(self.history) > 500:
            self.history.pop(0)

    def stop(self):
        self.stopped = True

    def show(self):
        app_hdl.canvas.stroke('yellow')
        app_hdl.canvas.fill('yellow')
            
        for p in range(1, len(self.history)-1):
            app_hdl.canvas.line(self.history[p-1].x, self.history[p-1].y,
                                self.history[p].x, self.history[p].y)


class Blackhole:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.mass = 1000
        self.er = (2 * G * self.mass) / (c ** 2)

    def attract(self, particle):
        force = self.position.copy()
        force -= particle.position
        d = force.mag()
        
        if d < self.er:
            particle.stop()

        force.normalize()
        strength = (G * self.mass * particle.mass) / (d ** 2)
        force *= strength
        return force

    def show(self):
        app_hdl.canvas.fill('black')
        app_hdl.canvas.stroke('black')
        app_hdl.canvas.circle(self.position.x, self.position.y, math.floor(self.er))


def setup(app):
    global app_hdl
    app_hdl = app

    app.blackhole = Blackhole(500, HEIGHT // 2)

    app.light = []

    for i in range(0, total):
        app.light.append(Particle(1000, HEIGHT * i / total, -1))

    '''for i in range(0, total):
        app.light.append(Particle(0, HEIGHT * i / total, 1))'''


    app.stars = []
    for i in range(200):
        app.stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT)])


def draw(app):
    for s in app.stars:
        app.canvas.point(s[0], s[1], 'white')

    for p in app.light:
        if not p.stopped:
            force = app.blackhole.attract(p)
            p.applyForce(force)
        p.update()
        p.show()
    app.blackhole.show()


EasyDraw(width = WIDTH,
        height = HEIGHT,
        fps = 30,
        background = 'black',
        title = 'Blackhole',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
