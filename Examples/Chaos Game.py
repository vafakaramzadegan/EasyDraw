import EasyDraw as ed
import random
import math

width = 600
height = 600

count = 5
jump = 0.5

def setup(app):
    app.x = random.randint(0, width)
    app.y = random.randint(0, height)
    
    app.canvas.translate(width // 2, height // 2)

    app.points = {}

    radius = width // 2
    deg = (2 * math.pi) / count

    app.canvas.rotate(45)

    for i in range(0, count):
        app.points[i] = {}
        app.points[i]['x'] = math.cos(i * deg) * radius
        app.points[i]['y'] = math.sin(i * deg) * radius
        app.points[i]['color'] = 'white'#app.color.random()

    app.lastVertex = 0

def draw(app):
    for i in range(0, 500):
        r = random.randint(0, count - 1)
        
        if r == app.lastVertex: continue

        app.x = app.tools.lerp(app.x, app.points[r]['x'], jump)
        app.y = app.tools.lerp(app.y, app.points[r]['y'], jump)

        app.canvas.point(app.x, app.y, app.points[r]['color'])

        app.lastVertex = r
    

ed.EasyDraw(width = width,
            height = height,
            setupFunc = setup,
            drawFunc = draw,
            fps = 30,
            background = 'black',
            autoClear = False)
