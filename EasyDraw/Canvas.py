import tkinter as tk
from multipledispatch import dispatch

import math

from PIL import Image, ImageTk, ImageDraw, ImageColor
from pyscreenshot import grab

from EasyDraw import Vector

class Canvas:
    '''Extends functionality of tk.canvas'''
    def __init__(self, master, **kwargs):
        # stores pushed parameters
        self.__hist = []
        self.__hist.append({})
        # frames to export as a GIF file
        self.__frames = []
        # canvas origin position
        self.__parameters()['center_x']        = 0
        self.__parameters()['center_y']        = 0
        # rotation degree
        self.__parameters()['rotate_deg']      = 0
        # fill and stroke color
        self.__parameters()['fill_color']      = 'white'
        self.__parameters()['stroke_color']    = 'black'
        # stroke thickness
        self.__parameters()['stroke_width']    = 1
        self.__parameters()['stroke_disabled'] = False
        # vertices data to create polygon
        self.__vertices        = []
        self.__width           = kwargs.get('width', 0)
        self.__height          = kwargs.get('height', 0)
        # list of shapes drawn on PhotoImage
        self.__alpha_shapes    = []
        # font styles
        self.__parameters()['font_family']     = 'Tahoma 20'
        self.__parameters()['font_color']      = 'black'

        # tkinter's default methods are available in handle
        self.handle = tk.Canvas(master,
                                width              = self.__width,
                                height             = self.__height,
                                background         = kwargs.get('background', 'black'),
                                highlightthickness = 0)
        self.app = kwargs.get('app', None)
        self.__showGrid = kwargs.get('showGrid', False)
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

    # save frames to file
    def save_frames(self, path, interval):
        try:
            self.__frames[0].save(path,
                                  format = 'GIF',
                                  append_images = self.__frames[1:],
                                  save_all = True,
                                  optimize = True,
                                  duration = interval,
                                  loop = 0)
            return True
        except:
            raise Exception('ExportError: unable to save frames to GIF file!')

    # transform coordinates based on origin and rotation value
    def transform_coords(self, coords, offset=None):
        if offset is not None:
            cx = offset[0]
            cy = offset[1]
        else:
            cx = self.__parameters()['center_x']
            cy = self.__parameters()['center_y']

        if self.app.useBounds:
            cx = self.app.bound_center[0] + (cx * self.app.scale_x)
            cy = self.app.bound_center[1] + (cy * self.app.scale_y)

        angle = math.radians(self.__parameters()['rotate_deg'])
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        new_coords = []
        for x_old, y_old in coords:
            x_new = (x_old * cos_val - y_old * sin_val)
            y_new = (x_old * sin_val + y_old * cos_val)

            if self.app.useBounds:
                x_new *= self.app.scale_x
                y_new *= -self.app.scale_y

            new_coords.append((x_new + cx, y_new + cy))

        return new_coords

    # get center position
    def get_center_pos(self):
        return (self.__parameters()['center_x'], self.__parameters()['center_y'])

    # set the coordinates of canvas origin
    # all objects on the canvas are placed relative to these
    # values.
    def translate(self, x, y):
        self.__parameters()['center_x'] = x
        self.__parameters()['center_y'] = y

    # set rotation value
    def rotate(self, deg):
        self.__parameters()['rotate_deg'] = deg

    # set fill color
    def fill(self, color):
        self.__parameters()['fill_color'] = color

    # empty fill value
    def no_fill(self):
        self.__parameters()['fill_color'] = ''

    # set stroke color
    def stroke(self, color):
        self.__parameters()['stroke_color'] = color
        self.__parameters()['stroke_disabled'] = False

    # disable stroke
    def no_stroke(self):
        self.__parameters()['stroke_disabled'] = True

    # set stroke width
    def stroke_width(self, width):
        self.__parameters()['stroke_width'] = width

    # create circle
    def circle(self, x, y, radius, **kwargs):
        points = self.transform_coords([[x - radius, y - radius],
                                          [x + radius, y + radius]])
        x1, y1 = (math.floor(points[0][0]), math.floor(points[0][1]))
        x2, y2 = (math.floor(points[1][0]), math.floor(points[1][1]))
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if self.app.useBounds:
            size = ((radius * 2 * self.app.scale_x), (radius * 2 * self.app.scale_y))
        else:
            size = ((radius * 2), (radius * 2))

        alpha = int(kwargs.get('alpha', 1) * 255)
        bgAlpha = alpha

        if (self.__parameters()['fill_color'] == ''):
            self.__parameters()['fill_color'] = '#000'
            bgAlpha = 0

        fill = ImageColor.getrgb(self.__parameters()['fill_color']) + (bgAlpha,)

        if self.__parameters()['stroke_disabled']:
            self.__parameters()['stroke_color'] = self.__parameters()['fill_color']

        stroke = ImageColor.getrgb(self.__parameters()['stroke_color']) + (alpha,)
        image = Image.new('RGBA', size)

        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, size), fill = fill, outline = stroke)

        self.__alpha_shapes.append(ImageTk.PhotoImage(image.rotate(-self.__parameters()['rotate_deg'], expand = True)))
            
        return self.handle.create_image(cx, cy,
                                        image=self.__alpha_shapes[-1],
                                        anchor = 'center')

    # create rectangle
    def rect(self, x1, y1, x2, y2, **kwargs):
        points = self.transform_coords([[x1, y1], [x2, y2]])
        dx = (x2 - x1)
        dy = (y2 - y1)
      
        if self.app.useBounds:
            dx *= self.app.scale_x
            dy *= self.app.scale_y

        cx = (points[0][0] + points[1][0]) // 2
        cy = (points[0][1] + points[1][1]) // 2

        alpha = int(kwargs.get('alpha', 1) * 255)
        bgAlpha = alpha

        if (self.__parameters()['fill_color'] == ''):
            self.__parameters()['fill_color'] = '#000'
            bgAlpha = 0

        if self.__parameters()['stroke_disabled']:
            self.__parameters()['stroke_color'] = self.__parameters()['fill_color']

        fill = ImageColor.getrgb(self.__parameters()['fill_color']) + (bgAlpha,)
        stroke = ImageColor.getrgb(self.__parameters()['stroke_color']) + (alpha,)
        image = Image.new('RGBA', (math.floor(dx), math.floor(dy)))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, dx, dy), fill = fill, outline = stroke, width = self.__parameters()['stroke_width'])
        self.__alpha_shapes.append(ImageTk.PhotoImage(image.rotate(self.__parameters()['rotate_deg'], expand = True)))
        return self.handle.create_image(cx, cy,
                                        image = self.__alpha_shapes[-1],
                                        anchor = 'center')

    # create line
    # this method accepts two types of .
    # 1) starting and ending X & Ys
    # 2) two vectors
    @dispatch(object, object, object, object)
    def line(self, x1, y1, x2, y2):
        return self.handle.create_line(self.transform_coords([
                                        [x1, y1],
                                        [x2, y2]]),
                                        fill = self.__parameters()['stroke_color'],
                                        width = self.__parameters()['stroke_width'])
    @dispatch(Vector.Vector, Vector.Vector)
    def line(self, v1, v2):
        return self.line(int(v1.a), int(v1.b), int(v2.a), int(v2.b))

    # draw triangle on canvas using customShape
    @dispatch(object, object, object, object, object, object)
    def triangle(self, x1, y1, x2, y2, x3, y3):
        tmp = self.__vertices
        self.begin_shape()
        self.vertex(x1, y1)
        self.vertex(x2, y2)
        self.vertex(x3, y3)
        obj = self.end_shape()
        self.__vertices = tmp
        return obj
    @dispatch(Vector.Vector, Vector.Vector, Vector.Vector)
    def triangle(self, v1, v2, v3):
        return self.triangle(v1.a, v1.b,
                             v2.a, v2.b,
                             v3.a, v3.b)

    # draw arc on canvas
    def arc(self, x1, y1, x2, y2, start, extend):
        return self.handle.create_arc(self.transform_coords([[x1, y1], [x2, y2]]),
                                      extent = -extend,
                                      start = -start,
                                      style = tk.ARC,
                                      outline = self.__parameters()['stroke_color'],
                                      width = self.__parameters()['stroke_width'])

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
            w = max(xs) * 3
            h = max(ys) * 3

            cx = self.__parameters()['center_x']
            cy = self.__parameters()['center_y']
            
            if self.app.useBounds:
                w = self.__width
                h = self.__height
                cx = self.app.bound_center[0]
                cy = self.app.bound_center[1]

            size = (max(w, h), max(w, h))
            offset = None if self.app.useBounds else (size[0] // 2, size[1] // 2)

            # set width and height of polygon
            alpha = int(kwargs.get('alpha', 1) * 255)
            bgAlpha = alpha

            if (self.__parameters()['fill_color'] == ''):
                self.__parameters()['fill_color'] = '#000'
                bgAlpha = 0

            fill = ImageColor.getrgb(self.__parameters()['fill_color']) + (bgAlpha,)

            if self.__parameters()['stroke_disabled']:
                self.__parameters()['stroke_color'] = self.__parameters()['fill_color']
            
            stroke = ImageColor.getrgb(self.__parameters()['stroke_color']) + (alpha,)
            
            image = Image.new('RGBA', size)
            draw = ImageDraw.Draw(image)

            draw.polygon(self.transform_coords(self.__vertices, offset),
                        fill = fill,
                        outline = stroke)

            self.__alpha_shapes.append(ImageTk.PhotoImage(image))

            return self.handle.create_image(cx, cy,
                                            image = self.__alpha_shapes[-1],
                                            anchor = 'center')
    '''------------------------------------------------------------------------------'''

    def font_family(self, family):
        self.__parameters()['font_family'] = family

    def font_color(self, color):
        self.__parameters()['font_color'] = color

    # put text on canvas
    def text(self, x, y, text):
        return self.handle.create_text(self.transform_coords([[x, y]]),
                                       fill = self.__parameters()['font_color'],
                                       font = self.__parameters()['font_family'],
                                       angle = -self.__parameters()['rotate_deg'],
                                       text = text)

    # set a pixel
    def point(self, x, y, color):
        for point_x, point_y in self.transform_coords([[x, y]]):
            if point_x >= 0 and point_y >= 0:
                return self.handle.create_line(self.transform_coords([
                                        [x, y],
                                        [x + 1, y + 1]]),
                                        fill = color)
                                        
    # get RGB value of a pixel
    def get_pixel(self, x, y):
        x += self.__parameters()['center_x']
        y += self.__parameters()['center_y']
        try:
            im = self.__pack()
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((x, y))
            return (r, g, b)
        except:
            return (0, 0, 0)

    def create_image(self, x, y, path, **kwargs):
        im = Image.open(path)

        scale = kwargs.get('scale', None)
        if scale != None:
            width, height = im.size
            newWidth = math.floor(width * scale)
            newheight = math.floor(height * scale)
            im = im.resize((newWidth, newheight), Image.ANTIALIAS)

        self.__alpha_shapes.append(ImageTk.PhotoImage(im.rotate(self.__parameters()['rotate_deg'], expand = True)))
        return self.handle.create_image(self.transform_coords([[x, y]]),
                                        image = self.__alpha_shapes[-1],
                                        anchor = 'center')

    # return the latest parameters
    def __parameters(self):
        return self.__hist[len(self.__hist) - 1]

    # push current parameters
    def push(self):
        self.__hist.append(self.__parameters().copy())

    # pop last parameters
    def pop(self):
        if len(self.__hist) == 1:
            raise Exception('Cannot go back any furthur. List is empty!')
        self.__hist.pop(len(self.__hist) - 1)

    # draw grid on screen.
    # requires boundaries to be set first
    def showGrid(self):
        if type(self.app.bounds) is tuple:
            self.push()
            self.stroke('#333')
            self.stroke_width(1)
            self.handle.create_rectangle(0, 0,
                                         self.__width, self.__height,
                                         fill = self.app.bg_color,
                                         outline = self.app.bg_color)
            
            for i in range(self.app.bounds[0], self.app.bounds[2] + 1):
                self.line(i, self.app.bounds[1], i, self.app.bounds[3])
                
            for i in range(self.app.bounds[1], self.app.bounds[3] + 1):
                self.line(self.app.bounds[0], i, self.app.bounds[2], i)

            self.pop()

    # clear canvas
    def clear(self, target):
        self.handle.delete(target)
        if self.__showGrid:
            self.showGrid()