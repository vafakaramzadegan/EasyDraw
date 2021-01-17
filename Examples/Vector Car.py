from EasyDraw import EasyDraw
from EasyDraw.Vector import Vector
import math

# Load car image from URL
# you can download and save the image on your computer
# for faster loading speed
import requests
from io import BytesIO
car_image_url = requests.get('https://storage.scriptshot.ir/white-car-small.png')

WIDTH = 700
HEIGHT = 700

class Car:
    def __init__(self):
        self.pos = Vector(WIDTH // 2, HEIGHT // 2)
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.dest = Vector(0, 0)

    def update(self, app):
        app.canvas.translate(self.pos.x, self.pos.y)
        self.dest = Vector(app.mouse_x, app.mouse_y)
        self.acc = Vector(app.mouse_x / WIDTH, app.mouse_y / HEIGHT)
        self.vel += self.acc
        self.pos += self.vel
        app.canvas.push()
        app.canvas.translate(0, HEIGHT)
        app.canvas.font_color('white')
        app.canvas.font_family('Tahoma 14')
        app.canvas.text_anchor('sw')
        app.canvas.text(16, -16, f'Speed: {math.floor(self.vel.length())} px/sec')
        app.canvas.pop()
        self.acc *= 0

    def show(self, c):
        c.push()
        c.stroke('yellow')
        c.fill('yellow')
        c.line(0, 0, self.dest.x, self.dest.y)
        c.circle(self.dest.x, self.dest.y, 5)
        c.rotate(self.vel.heading())
        c.create_image(0, 0, BytesIO(car_image_url.content), scale=1)
        c.pop()

def setup(app):
    app.car = Car()

def draw(app):
    app.car.update(app)
    app.car.show(app.canvas)

EasyDraw(width = WIDTH,
        height = HEIGHT,
        fps = 60,
        background = 'black',
        title = 'Vector Car',
        autoClear = True,
        fullscreen = True,
        showStats = True,
        setupFunc = setup,
        drawFunc = draw)
