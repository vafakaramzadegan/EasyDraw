import tkinter as tk
import math
from io import BytesIO
from PIL import Image
from EasyDraw import color
from EasyDraw import tools

class Canvas:
    '''Extends functionality of tk.canvas'''
    def __init__(self, master, **kwargs):
        self.center_x = 0
        self.center_y = 0
        self.rotate_deg = 0
        self.fill_color = 'white'
        self.stroke_color = 'black'
        self._stroke_width = 1
        self.vertices = []
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)
        self.tools = tools.Tools()
        self.color = color.Color()
        self.handle = tk.Canvas(master,
                                width              = self.width,
                                height             = self.height,
                                background         = kwargs.get('background', 'black'),
                                highlightthickness = 0)
        # no transparent background
        self.handle.create_rectangle(0, 0,
                                     self.width, self.height,
                                     fill = kwargs.get('background', 'black'),
                                     outline = kwargs.get('background', 'black'))
        self.handle.pack(expand = 1)

    # transform coordinates based on canvas center and rotation value
    def __transform_coords(self, coords):
        angle = math.radians(self.rotate_deg)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        new_coords = []
        for x_old, y_old in coords:
            x_new = math.floor(x_old * cos_val - y_old * sin_val)
            y_new = math.floor(x_old * sin_val + y_old * cos_val)
            new_coords.append([x_new + self.center_x, y_new + self.center_y])
        return new_coords

    def __pack(self):
        ps = self.handle.postscript(colormode='color', 
                                    x = 0, y = 0,
                                    height = self.height, width = self.width,
                                    pageheight = self.height, pagewidth = self.width)
        return Image.open(BytesIO(ps.encode('utf-8')))

    # set translation coordinates
    def translate(self, x, y):
        self.center_x = math.floor(x)
        self.center_y = math.floor(y)

    # set rotation value
    def rotate(self, deg):
        self.rotate_deg = deg

    # set fill color
    def fill(self, color):
        self.fill_color = color

    def no_fill(self):
        self.fill_color = ''

    # set stroke color
    def stroke(self, color):
        self.stroke_color = color

    def stroke_width(self, width):
        self._stroke_width = width

    # create circle
    def circle(self, x, y, radius):
        points = self.__transform_coords([[x - radius, y - radius],
                                          [x + radius, y + radius]])
        x1, y1 = points[0]
        x2, y2 = points[1]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        return self.handle.create_oval(cx - radius, cy - radius,
                                       cx + radius, cy + radius,
                                       fill = self.fill_color,
                                       outline = self.stroke_color)

    # create rectangle
    # rectangle is simply a polygon
    def rect(self, x1, y1, x2, y2):
        return self.handle.create_polygon(self.__transform_coords([
                                            [x1, y1], [x2, y1],
                                            [x2, y2], [x1, y2]]),
                                            fill = self.fill_color,
                                            outline = self.stroke_color)

    # create line
    def line(self, x1, y1, x2, y2):
        return self.handle.create_line(self.__transform_coords([
                                        [x1, y1],
                                        [x2, y2]]),
                                        fill = self.stroke_color,
                                        width = self._stroke_width)

    # set a pixel
    def point(self, x, y, color):
        for point_x, point_y in self.__transform_coords([[x, y]]):
            if point_x >= 0 and point_y >= 0:
                return self.handle.create_line(self.__transform_coords([
                                        [x, y],
                                        [x + 1, y + 1]]),
                                        fill = color)
                                        
    # set a pixel with alpha value
    def point_alpha(self, x, y, rgb_color, alpha):
        for point_x, point_y in self.__transform_coords([[x, y]]):
            if point_x >= 0 and point_y >= 0:
                c2 = self.get_pixel(x, y) + (.1, )
                c_mix = self.color.blend_colors(rgb_color + (alpha, ), c2)
                return self.handle.create_line(self.__transform_coords([
                                        [x, y],
                                        [x + 1, y + 1]]),
                                        fill = self.color.rgb(c_mix[0], c_mix[1], c_mix[2]))

    # get RGB value of a pixel
    def get_pixel(self, x, y):
        x += self.center_x
        y += self.center_y
        try:
            im = self.__pack()
            #im.save('/home/vafa/Documents/Python/Chaos Game/pic.png')
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((x, y))
            return (r, g, b)
        except:
            return (0, 0, 0)


    '''create polygons---------------------------------------------------------------'''
    def begin_shape(self):
        self.vertices.clear()

    def vertex(self, x, y):
        self.vertices.append([x, y])

    def end_shape(self):
        if len(self.vertices) > 1:
            return self.handle.create_polygon(self.__transform_coords(self.vertices),
                                              fill = self.fill_color,
                                              outline = self.stroke_color,
                                              width = self._stroke_width)
    '''------------------------------------------------------------------------------'''

    # clear canvas
    def clear(self, target):
        self.handle.delete(target)