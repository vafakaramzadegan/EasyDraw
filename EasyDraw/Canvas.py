import tkinter as tk
from multipledispatch import dispatch

import math

from PIL import Image, ImageTk, ImageDraw, ImageColor
from pyscreenshot import grab

from EasyDraw import Vector

class Canvas:
    '''Extends functionality of tk.canvas'''
    def __init__(self, master, **kwargs):
        # frames to export as a GIF file
        self.__frames = []
        # canvas origin position
        self.__center_x        = 0
        self.__center_y        = 0
        # rotation degree
        self.__rotate_deg      = 0
        # fill and stroke color
        self.__fill_color      = 'white'
        self.__stroke_color    = 'black'
        # stroke thickness
        self.__stroke_width    = 1
        self.__stroke_disabled = False
        # vertices data to create polygon
        self.__vertices        = []

        self.__width           = kwargs.get('width', 0)
        self.__height          = kwargs.get('height', 0)
        # list of shapes drawn on PhotoImage
        self.__alpha_shapes    = []
        # font styles
        self.__font_family     = 'Tahoma 20'
        self.__font_color      = 'black'

        # tkinter's default methods are available in handle
        self.handle = tk.Canvas(master,
                                width              = self.__width,
                                height             = self.__height,
                                background         = kwargs.get('background', 'black'),
                                highlightthickness = 0)
        # no transparent background
        self.handle.create_rectangle(0, 0,
                                     self.__width, self.__height,
                                     fill = kwargs.get('background', 'black'),
                                     outline = kwargs.get('background', 'black'))
        self.handle.pack(expand = 1)

    # clear content data
    def clear_data(self):
        self.__alpha_shapes.clear()
        self.__vertices.clear()

    # take a screenshot of the app window
    def __pack(self):
        if self.handle.winfo_width() < 10: return False

        return grab(bbox=(self.handle.winfo_rootx(),
                          self.handle.winfo_rooty(),
                          self.handle.winfo_rootx() + self.handle.winfo_width(),
                          self.handle.winfo_rooty() + self.handle.winfo_height()))

    # append current frame to list
    def export_frame(self):
        im = self.__pack()
        if im: self.__frames.append(im)

    def save_frames(self, path, interval):
        try:
            self.__frames[0].save(path,
                                  format = 'GIF',
                                  append_images = self.__frames[1:],
                                  save_all = True,
                                  duration = interval,
                                  loop = 1)
            return True
        except:
            raise Exception('ExportError: unable to save frames to GIF file!')

    # transform coordinates based on origin and rotation value
    def __transform_coords(self, coords, offset=None):
        if offset is not None:
            cx = offset[0]
            cy = offset[1]
        else:
            cx = self.__center_x
            cy = self.__center_y          
        angle = math.radians(self.__rotate_deg)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        new_coords = []
        for x_old, y_old in coords:
            x_new = math.floor(x_old * cos_val - y_old * sin_val)
            y_new = math.floor(x_old * sin_val + y_old * cos_val)
            new_coords.append((x_new + cx, y_new + cy))
        return new_coords

    # get center position
    def get_center_pos(self):
        return (self.__center_x, self.__center_y)

    # set the coordinates of canvas origin
    # all objects on the canvas are placed relative to these
    # values.
    def translate(self, x, y):
        self.__center_x = math.floor(x)
        self.__center_y = math.floor(y)

    # set rotation value
    def rotate(self, deg):
        self.__rotate_deg = deg

    # set fill color
    def fill(self, color):
        self.__fill_color = color

    def no_fill(self):
        self.__fill_color = ''

    # set stroke color
    def stroke(self, color):
        self.__stroke_color = color
        self.__stroke_disabled = False

    def no_stroke(self):
        self.__stroke_disabled = True

    def stroke_width(self, width):
        self.__stroke_width = width

    # create circle
    def circle(self, x, y, radius, **kwargs):
        points = self.__transform_coords([[x - radius, y - radius],
                                          [x + radius, y + radius]])
        x1, y1 = points[0]
        x2, y2 = points[1]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        size = ((radius * 2) + 1, (radius * 2) + 1)
        alpha = int(kwargs.get('alpha', 1) * 255)
        bgAlpha = alpha

        if (self.__fill_color == ''):
            self.__fill_color = '#000'
            bgAlpha = 0

        fill = ImageColor.getrgb(self.__fill_color) + (bgAlpha,)

        if self.__stroke_disabled: self.__stroke_color = self.__fill_color

        stroke = ImageColor.getrgb(self.__stroke_color) + (alpha,)
        image = Image.new('RGBA', size)

        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, size), fill = fill, outline = stroke)

        self.__alpha_shapes.append(ImageTk.PhotoImage(image.rotate(-self.__rotate_deg, expand = True)))
            
        return self.handle.create_image(cx, cy,
                                        image=self.__alpha_shapes[-1],
                                        anchor = 'center')

    # create rectangle
    def rect(self, x1, y1, x2, y2, **kwargs):
        dx = x2 - x1
        dy = y2 - y1
        alpha = int(kwargs.get('alpha', 1) * 255)
        bgAlpha = alpha

        if (self.__fill_color == ''):
            self.__fill_color = '#000'
            bgAlpha = 0

        if self.__stroke_disabled: self.__stroke_color = self.__fill_color

        fill = ImageColor.getrgb(self.__fill_color) + (bgAlpha,)
        stroke = ImageColor.getrgb(self.__stroke_color) + (alpha,)
        image = Image.new('RGBA', (dx, dy))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, dx, dy), fill = fill, outline = stroke, width = self.__stroke_width)
        self.__alpha_shapes.append(ImageTk.PhotoImage(image.rotate(-self.__rotate_deg, expand = True)))
        return self.handle.create_image(self.__transform_coords([[x1 + (dx / 2), y1 + (dy / 2)]]),
                                        image=self.__alpha_shapes[-1],
                                        anchor = 'center')

    # create line
    # this method accepts two types of input
    # the x and y values of start and end positions
    # and also two vectors
    @dispatch(int, int, int, int)
    def line(self, x1, y1, x2, y2):
        return self.handle.create_line(self.__transform_coords([
                                        [x1, y1],
                                        [x2, y2]]),
                                        fill = self.__stroke_color,
                                        width = self.__stroke_width)
    @dispatch(Vector.Vector, Vector.Vector)
    def line(self, v1, v2):
        return self.line(int(v1.a), int(v1.b), int(v2.a), int(v2.b))

    # draw triangle on canvas using customShape
    def triangle(self, x1, y1, x2, y2, x3, y3):
        tmp = self.__vertices
        self.begin_shape()
        self.vertex(x1, y1)
        self.vertex(x2, y2)
        self.vertex(x3, y3)
        obj = self.end_shape()
        self.__vertices = tmp
        return obj

    # draw arc on canvas
    def arc(self, x1, y1, x2, y2, start, extend):
        return self.handle.create_arc(self.__transform_coords([[x1, y1], [x2, y2]]),
                                      extent = -extend,
                                      start = -start,
                                      style = tk.ARC,
                                      outline = self.__stroke_color,
                                      width = self.__stroke_width)

    '''create polygons---------------------------------------------------------------'''
    def begin_shape(self):
        self.__vertices.clear()

    def vertex(self, x, y):
        self.__vertices.append((round(x), round(y)))

    def end_shape(self, **kwargs):
        if len(self.__vertices) > 1:
            # get polygon bounding box
            xs = [x[0] for x in self.__vertices]
            ys = [y[1] for y in self.__vertices]
            w = max(xs) * 2
            h = max(ys) * 2
            # set width and height of polygon
            size = (max(w, h), max(w, h))
            alpha = int(kwargs.get('alpha', 1) * 255)
            bgAlpha = alpha

            if (self.__fill_color == ''):
                self.__fill_color = '#000'
                bgAlpha = 0

            fill = ImageColor.getrgb(self.__fill_color) + (bgAlpha,)

            if self.__stroke_disabled: self.__stroke_color = self.__fill_color
            
            stroke = ImageColor.getrgb(self.__stroke_color) + (alpha,)
            
            image = Image.new('RGBA', size)
            draw = ImageDraw.Draw(image)

            draw.polygon(self.__transform_coords(self.__vertices, (size[0] // 2, size[1] // 2)),
                        fill = fill,
                        outline = stroke)

            self.__alpha_shapes.append(ImageTk.PhotoImage(image))

            return self.handle.create_image(self.__center_x, self.__center_y,
                                            image=self.__alpha_shapes[-1],
                                            anchor = 'center')
    '''------------------------------------------------------------------------------'''

    def font_family(self, family):
        self.__font_family = family

    def font_color(self, color):
        self.__font_color = color

    # put text on canvas
    def text(self, x, y, text):
        return self.handle.create_text(self.__transform_coords([[x, y]]),
                                       fill = self.__font_color,
                                       font = self.__font_family,
                                       text = text)

    # set a pixel
    def point(self, x, y, color):
        for point_x, point_y in self.__transform_coords([[x, y]]):
            if point_x >= 0 and point_y >= 0:
                return self.handle.create_line(self.__transform_coords([
                                        [x, y],
                                        [x + 1, y + 1]]),
                                        fill = color)
                                        
    # get RGB value of a pixel
    def get_pixel(self, x, y):
        x += self.__center_x
        y += self.__center_y
        try:
            im = self.__pack()
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((x, y))
            return (r, g, b)
        except:
            return (0, 0, 0)


    # clear canvas
    def clear(self, target):
        self.handle.delete(target)