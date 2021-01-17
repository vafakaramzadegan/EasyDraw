from EasyDraw import EasyDraw
import random

WIDTH = 600
HEIGHT = 600

COUNT = 40
xdist = WIDTH // COUNT
ydist = HEIGHT // COUNT

class Population:
    def make2dArray(self):
        arr = []
        for i in range(COUNT):
            arr.append([])
            for j in range(COUNT):
                arr[i].append(random.randint(0, 1))
        return arr

    def countLiveNeighbors(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (i + x + COUNT) % COUNT
                row = (j + y + COUNT) % COUNT
                count += self.cells[col][row]
        count -= self.cells[x][y]
        return count

    def __init__(self):
        self.cells = self.make2dArray()

    def draw(self, canvas):
        next_gen = self.make2dArray()
        for i in range(COUNT):
            for j in range(COUNT):
                state = self.cells[i][j]
                if state == 1:
                    color = 'yellow'
                else:
                    color = 'black'
                canvas.fill(color)
                canvas.rect(i * xdist, j * ydist, (i+1) * xdist, (j+1) * ydist)

                count = self.countLiveNeighbors(i, j)

                if state == 1 and (count < 2 or count > 3):
                    next_gen[i][j] = 0
                elif state == 0 and count == 3:
                    next_gen[i][j] = 1
                else:
                    next_gen[i][j] = state

        self.cells = next_gen

def setup(app):
    app.pop = Population()
    app.canvas.stroke('black')

def draw(app):
    app.pop.draw(app.canvas)


EasyDraw(width = WIDTH,
        height = HEIGHT,
        fps = 24,
        background = 'black',
        title = 'Game of Life',
        autoClear = True,
        setupFunc = setup,
        drawFunc = draw)
