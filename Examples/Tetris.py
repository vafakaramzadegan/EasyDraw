from EasyDraw import *
from EasyDraw.Color import *

import random


WIDTH = 1000
HEIGHT = 600

# a shape is a 2d list
# there is no limit on the size of them
shapes = [
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 0], [1, 1], [0, 1]],
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

# the number of colors must match the number of shapes
colors = [
    [RGB(53, 115, 174), RGB(3, 65, 174)],
    [RGB(64, 153, 9),   RGB(114, 203, 59)],
    [RGB(205, 163, 0),  RGB(255, 213, 0)],
    [RGB(205, 101, 0),  RGB(255, 151, 28)],
    [RGB(205, 0, 0),    RGB(255, 50, 19)]    
]

class Board:
    # next random shape to play
    next_piece_index = random.randint(0, len(shapes)-1)
    block_dim = 0
    score = 0

    def __init__(self):
        self.border_width = 15
        self.border_color = RGB(84, 84, 252)
        # clock cycles for moving each piece across board
        self.speed_factor = 3
        # board dimensions
        self.hblocks_cnt = 12
        self.vblocks_cnt = 18
        # set default board height
        # calculate each block's dimensions
        # set width according to height
        self.height = HEIGHT * 90 // 100
        self.block_dim = self.height // self.vblocks_cnt
        self.width = self.hblocks_cnt * self.block_dim
        # position of the board on screen
        self.margin_left = 64
        self.margin_top = (HEIGHT - self.height) // 2
        # create square blocks on board (a 2d list)
        self.blocks = []
        for i in range(self.hblocks_cnt):
            self.blocks.append([])
            for j in range(self.vblocks_cnt):
                self.blocks[i].append(-1)

        # create starting piece on board
        self.create_piece()


    def create_piece(self):
        # index used to get shape and color from lists
        self.cp_ind = self.next_piece_index
        self.cp = shapes[self.cp_ind]
        # rotate piece randomly
        for i in range(random.randint(0, 3)):
            self.cp = list(zip(*self.cp[::-1]))
        # optional - flip piece randomly
        for i in range(random.randint(0, 2)):
            self.cp = self.cp[::-1]
        # set the starting position randomly
        self.cp_l = random.randint(0, self.hblocks_cnt - len(self.cp))
        self.cp_t = 0

        self.speed_factor = 3
        self.next_piece_index = random.randint(0, len(shapes)-1)


    def check_collision(self):
        collision = False
                
        for i, x in enumerate(self.cp):
            for j, y in enumerate(x):
                if self.cp_t + j + 1 >= self.vblocks_cnt:
                    collision = True
                    break
                else:
                    if y == 1 and self.blocks[self.cp_l + i][self.cp_t + j + 1] > -1:
                        collision = True
                        break
            if collision:
                break

        if collision:
            for i, x in enumerate(self.cp):
                for j, y in enumerate(x):
                    if y == 1:
                        self.blocks[self.cp_l + i][self.cp_t + j] = self.cp_ind

            # check if there are complete rows to be cleared
            for row in range(self.vblocks_cnt):
                complete = True
                for cindex, col in enumerate(self.blocks):
                    if self.blocks[cindex][row] < 0:
                        complete = False
                if complete:
                    for cindex, col in enumerate(self.blocks):
                        self.blocks[cindex][row] = -2

                    self.score += 100
                
            self.score += 5
            self.create_piece()


    def shift_left(self):
        self.cp_l -= 1


    def shift_right(self):
        self.cp_l += 1


    def rotate_piece(self):
        self.cp = list(zip(*self.cp[::-1]))


    def fast_drop(self):
        self.speed_factor = 1


    def draw(self, app):
        c = app.canvas

        # draw the borders of the board
        c.push()
        c.no_fill()
        c.stroke(self.border_color)
        c.stroke_width(self.border_width)
        c.translate(self.margin_left + self.width//2, self.height//2)
        c.rect(
            (-self.width // 2) - self.border_width,
            (-self.height // 2) - self.border_width,
            (self.width // 2) + self.border_width,
            (self.height // 2) + self.border_width
        )
        c.pop()

        # draw blocks
        c.push()
        for col_index, col in enumerate(self.blocks):
            for row_index, row in enumerate(col):
                c.translate(
                    self.margin_left + (col_index * self.block_dim),
                    (row_index * self.block_dim)
                )
                # blocks with value -1 are empty
                if row == -2:
                    c.stroke('white')
                    c.fill('white')            
                elif row == -1:
                    c.stroke(RGB(60, 60, 60))
                    c.fill(RGB(10, 10, 10))
                else:
                    c.stroke(colors[row][0])
                    c.fill(colors[row][1])

                c.rect(0, 0, self.block_dim, self.block_dim)

        # remove rows that are completed
        for col_index, col in enumerate(self.blocks):
            for row_index, row in enumerate(col):
                if row == -2:
                    self.blocks[col_index].pop(row_index)
                    self.blocks[col_index].insert(0, -1)
        c.pop()

        # draw current moving shape
        c.push()
        c.stroke(colors[self.cp_ind][0])
        c.fill(colors[self.cp_ind][1])

        for i, x in enumerate(self.cp):
            for j, y in enumerate(x):
                if y == 1:
                    if i + self.cp_l < 0:
                        self.cp_l += 1
                    elif i + self.cp_l > self.hblocks_cnt - 1:
                        self.cp_l -= 1

        for i, x in enumerate(self.cp):
            for j, y in enumerate(x):
                if y == 1:
                    c.translate(
                        self.margin_left + ((self.cp_l+i) * self.block_dim),
                        ((self.cp_t+j) * self.block_dim)
                    )
                    c.rect(0, 0, self.block_dim, self.block_dim)
        c.pop()

        # move piece and check for collision
        self.check_collision()
        # game clock
        if app.tick % self.speed_factor == 0:
            self.cp_t += 1



def setup(app):
    app.board = Board()


def draw(app):
    app.board.draw(app)

    c = app.canvas

    c.font_color('white')
    c.font_family("Courier 32 bold")
    c.text_anchor('nw')
    c.text(470, 32, "Tetris")

    c.font_family("Courier 12")
    c.text(470, 80, "Created using EasyDraw for Python\nhttps://github.com/vafakaramzadegan")

    c.text(470, 160, "Help:\n\nLeft & Right arrow keys: moves piece\nUp arrow key:            rotate\nDown arrow key:          fast move")

    # show next piece
    c.text(470, 300, "Next piece:")
    c.push()
    shape = shapes[app.board.next_piece_index]
    color = colors[app.board.next_piece_index]
    c.stroke(color[0])
    c.fill(color[1])
    dim = app.board.block_dim
    offset_left = 470
    offset_top = 340
    for i, x in enumerate(shape):
        for j, y in enumerate(x):
            if y == 1:
                c.translate(offset_left + (j * dim), offset_top + (i * dim))
                c.rect(0, 0, dim, dim)
    c.pop()

    c.font_family("Courier 24 bold")
    c.text(470, 500, f"Score: {app.board.score}")


def keyrelease(app, e):
    if e.keysym == "Left":
        app.board.shift_left()
    elif e.keysym == "Right":
        app.board.shift_right()
    elif e.keysym == "Up":
        app.board.rotate_piece()
    elif e.keysym == "Down":
        app.board.fast_drop()


EasyDraw(
    width=WIDTH,
    height=HEIGHT,
    drawFunc=draw,
    setupFunc=setup,
    fps=16,
    background="black",
    title="tetris",
    autoClear=True,
    keyReleaseFunc=keyrelease
)
