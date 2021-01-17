from EasyDraw import EasyDraw
from time import localtime

def setup(app):
    app.canvas.translate(300, 300)

def draw(app):
    c = app.canvas
    c.stroke_width(5)
    c.circle(0, 0, 200)
    c.push()
    for i in range(60):
        c.rotate(i * (360/60))
        if i % 5 == 0:
            c.fill('black')
            c.stroke('black')
            c.rect(-3, -200, 3, -180)
            c.text(0, -160, i // 5 if i > 0 else 12) 
        else:
            c.fill('grey')
            c.stroke('grey')
            c.rect(-1, -196, 1, -190)
    min_deg = localtime().tm_min * (360/60)
    hour_deg = ((localtime().tm_hour-12) * (360/12)) + ((min_deg / 360) * (360/12))
    sec_deg = localtime().tm_sec * (360/60)

    c.rotate(hour_deg)
    c.fill('black')
    c.stroke('black')
    c.circle(0, 0, 15)
    c.rect(-8, -80, 8, 0)
    c.circle(0, -80, 8)

    c.rotate(min_deg)
    c.rect(-5, -120, 5, 0)
    c.circle(0, -120, 5)

    c.fill('red')
    c.stroke('red')
    c.circle(0, 0, 5)
    c.rotate(sec_deg)
    c.rect(-2, -180, 2, 30)
    c.circle(0, -120, 2)

    c.pop()



EasyDraw(width = 600,
        height = 600,
        fps = 5,
        background = 'skyblue',
        title = 'Clock',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
