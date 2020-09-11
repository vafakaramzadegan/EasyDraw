'''
    EasyDraw
    -------------------------------
    A graphical library built for visual arts.
    EasyDraw is built on top of tkinter and has more functionalities.

    Author: Vafa Karamzadegan
    https://github.com/vafakaramzadegan/EasyDraw
'''

import tkinter as tk
from EasyDraw import Color
from EasyDraw import Canvas
from EasyDraw import Tools

class EasyDraw(object):
    '''EasyDraw main class'''
    def __init__(self, **kwargs):
        print('Hello from EasyDraw!')
        self.width        = kwargs.get('width', 400)
        self.height       = kwargs.get('height', 400)
        self.autoClear    = kwargs.get('autoClear', True)  
        self.interval     = kwargs.get('fps', 30)
        self.export_path  = kwargs.get('exportPath', '')
        if self.export_path != '':
            print('Recording frames...')
        self.mouse_x      = 0
        self.mouse_y      = 0
        self.mouse_left   = 0
        self.mouse_top    = 0

        self.useBounds    = False
        self.bounds       = (-5, -5, 5, 5)
        self.scale_x      = 0
        self.scale_y      = 0
        self.bound_center = (0, 0)

        if self.interval not in range(0, 1001):
            raise ValueError("invalid fps value should be between 1 and 1000 but '%d' was entered." % self.interval)
        self.interval  = 1000 // self.interval
        
        master         = tk.Tk()
        self.master    = master

        # bind mouse event handlers
        master.bind('<Motion>'         , self.__motion_event)
        master.bind('<Button-1>'       , self.__mouse_left_btn_click)
        master.bind('<Button-2>'       , self.__mouse_middle_btn_click)
        master.bind('<Button-3>'       , self.__mouse_right_btn_click)
        master.bind('<B1-Motion>'      , self.__left_mouse_btn_down)
        master.bind('<B3-Motion>'      , self.__right_mouse_btn_down)
        master.bind('<ButtonRelease-1>', self.__left_mouse_btn_up)
        master.bind('<ButtonRelease-3>', self.__right_mouse_btn_up)
        
        master.title(kwargs.get('title', 'EasyDraw App'))
        master.protocol("WM_DELETE_WINDOW", self.__on_closing)

        self.bg_color = kwargs.get('background', 'silver')
        self.canvas = Canvas.Canvas(master,
                            app = self,
                            width = self.width,
                            height = self.height,
                            background = self.bg_color,
                            showGrid = kwargs.get('showGrid', False))

        self.tools = Tools.Tools()
        self.color = Color.Color()

        self.setupFunction  = kwargs.get('setupFunc', None)
        self.drawFunction   = kwargs.get('drawFunc', None)
        self.mouseMoveFunction = kwargs.get('mouseMoveFunc', None)
        self.clickFunction = kwargs.get('clickFunc', None)
        self.mouseDownFunction = kwargs.get('mouseDownFunc', None)
        self.mouseUpFunction = kwargs.get('mouseUpFunc', None)

        bounds = kwargs.get('bounds', None)
        if type(bounds) is tuple:
            min_x = bounds[0]
            min_y = bounds[1]
            max_x = bounds[2]
            max_y = bounds[3]

            if max_x <= min_x:
                raise ValueError('Max X cannot be less than or equal to min X')

            if max_y <= min_y:
                raise ValueError('Max Y cannot be less than or equal to min Y')
                 
            self.useBounds = True
            self.bounds = (min_x, min_y, max_x, max_y)
            self.scale_x = self.width // abs(max_x - min_x)
            self.scale_y = self.width // abs(max_y - min_y)
            bx = 0
            if min_x >= 0:
                bx = -(min_x * self.scale_x)
            else:
                bx = self.width - (max_x * self.scale_x)
            by = 0
            if min_y >= 0:
                by = -(min_x * self.scale_y)
            else:
                by = (max_y * self.scale_y)
            
            self.bound_center = (bx, by)

        master.after(100, self.__setup())
        master.after(100, self.__animate())
        master.mainloop()


    def clearBounds(self):
        self.useBounds = False

    '''mouse related methods ---------------------------------------'''
    def __get_mouse_positions(self, e):
        if self.useBounds:
            transformed = self.canvas.transform_coords([[e.x, e.y]])
            self.mouse_x = transformed[0][0]
            self.mouse_y = transformed[0][1]
            self.mouse_x = self.tools.map(self.mouse_x,
                                          0,
                                          self.width,
                                          self.bounds[0],
                                          self.bounds[2])
            self.mouse_y = self.tools.map(self.mouse_y,
                                          0,
                                          self.width,
                                          self.bounds[3],
                                          self.bounds[1])
        else:
            self.mouse_x = e.x - self.canvas.get_center_pos()[0]
            self.mouse_y = e.y - self.canvas.get_center_pos()[1]

        self.mouse_left = e.x
        self.mouse_top = e.y

    def __motion_event(self, event):
        self.__get_mouse_positions(event)
        if self.mouseMoveFunction:
            self.mouseMoveFunction(self)

    def __mouse_left_btn_click(self, event):
        if self.clickFunction:
            self.clickFunction(self, 'left')

    def __mouse_middle_btn_click(self, event):
        if self.clickFunction:
            self.clickFunction(self, 'middle')

    def __mouse_right_btn_click(self, event):
        if self.clickFunction:
            self.clickFunction(self, 'right')

    def __left_mouse_btn_down(self, event):
        self.__get_mouse_positions(event)
        if self.mouseDownFunction:
            self.mouseDownFunction(self, 'left')

    def __right_mouse_btn_down(self, event):
        self.__get_mouse_positions(event)
        if self.mouseDownFunction:
            self.mouseDownFunction(self, 'right')

    def __left_mouse_btn_up(self, event):
        if self.mouseUpFunction:
            self.mouseUpFunction(self, 'left')

    def __right_mouse_btn_up(self, event):
        if self.mouseUpFunction:
            self.mouseUpFunction(self, 'right')

    '''-------------------------------------------------------------'''
        
    def __setup(self):
        if callable(self.setupFunction):
            self.setupFunction(self)
        else:
            raise TypeError('Setup function is either undefined or not callable!')
        
    def __animate(self):
        if self.autoClear == True:
            self.canvas.clear('all')        
            self.canvas.clear_data()

        if callable(self.drawFunction):
            self.drawFunction(self)
        else:
            raise Exception('Draw function is either undefined or not callable!')

        if self.export_path != '':
            self.canvas.export_frame()
        self.canvas.handle.after(self.interval, self.__animate)

    def __on_closing(self):
        if self.export_path != '':
            print('Saving frames as GIF file... please wait!')
            self.canvas.save_frames(self.export_path, self.interval)
            print('Done!')
        self.master.destroy()