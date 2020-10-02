'''
    EasyDraw
    -------------------------------
    A graphical library built for visual arts.
    EasyDraw is built on top of tkinter and has more functionalities.

    Author: Vafa Karamzadegan
    https://github.com/vafakaramzadegan/EasyDraw
'''

import tkinter as tk
import time

from EasyDraw import Color
from EasyDraw import Canvas
from EasyDraw.Tools import *
from EasyDraw import Vector

class EasyDraw(object):
    '''EasyDraw main class'''
    def __init__(self, **kwargs):
        print('Hello from EasyDraw!')
        # app clock
        self.tick         = 1
        self.__start_time = time.time()

        self.width        = kwargs.get('width', 400)
        self.height       = kwargs.get('height', 400)
        self.fullscreen   = kwargs.get('fullscreen', False)
        self.autoClear    = kwargs.get('autoClear', True)

        self.showStats    = kwargs.get('showStats', False)

        self.interval     = kwargs.get('fps', 30)
        if self.interval not in range(0, 1001):
            raise ValueError("invalid fps value should be between 1 and 1000 but '%d' was entered." % self.interval)
        self.interval  = 1000 // self.interval

        self.export_path  = kwargs.get('exportPath', '')
        if self.export_path != '':
            print('Recording frames...')
        # mouse position relative to origin
        self.mouse_x      = 0
        self.mouse_y      = 0
        # mouse distance to top left corner
        self.mouse_left   = 0
        self.mouse_top    = 0
        # indicates whether to use XY coordination system
        self.useBounds    = False
        self.bounds       = kwargs.get('bounds', None)
        self.scale_x      = 0
        self.scale_y      = 0
        self.bound_center = (0, 0)
        
        master         = tk.Tk()
        self.master    = master

        if self.fullscreen:
            master.attributes("-fullscreen", True)
            master.update()
            self.width = master.winfo_width()
            self.height = master.winfo_height()

        # bind mouse event handlers
        master.bind('<Motion>'         , self.__motion_event)
        master.bind('<Button-1>'       , self.__mouse_left_btn_click)
        master.bind('<Button-2>'       , self.__mouse_middle_btn_click)
        master.bind('<Button-3>'       , self.__mouse_right_btn_click)
        master.bind('<B1-Motion>'      , self.__left_mouse_btn_down)
        master.bind('<B3-Motion>'      , self.__right_mouse_btn_down)
        master.bind('<ButtonRelease-1>', self.__left_mouse_btn_up)
        master.bind('<ButtonRelease-3>', self.__right_mouse_btn_up)
        
        master.bind('<Escape>', self.__on_escape_key)
        master.bind('<Key>', self.__on_key_press)
        master.bind('<KeyRelease>', self.__on_key_release)

        # set window title
        master.title(kwargs.get('title', 'EasyDraw App'))
        # bind onWindowClose event
        master.protocol("WM_DELETE_WINDOW", self.__on_closing)

        self.bg_color = kwargs.get('background', 'silver')
        self.showGrid = kwargs.get('showGrid', False)

        self.canvas = Canvas.Canvas(master,
                            app = self,
                            width = self.width,
                            height = self.height,
                            background = self.bg_color,
                            showGrid = self.showGrid)

        # deprecated -------------------------
        self.tools = Tools()
        self.color = Color.Color()
        # ------------------------------------

        self.setupFunction     = kwargs.get('setupFunc', None)
        self.drawFunction      = kwargs.get('drawFunc', None)

        self.keyPressFunc      = kwargs.get('keyPressFunc', None)
        self.keyReleaseFunc    = kwargs.get('keyReleaseFunc', None)
        
        # mouse event callbacks
        self.mouseMoveFunction = kwargs.get('mouseMoveFunc', None)
        self.clickFunction     = kwargs.get('clickFunc', None)
        self.mouseDownFunction = kwargs.get('mouseDownFunc', None)
        self.mouseUpFunction   = kwargs.get('mouseUpFunc', None)

        if type(self.bounds) is tuple:
            min_x = self.bounds[0]
            min_y = self.bounds[1]
            max_x = self.bounds[2]
            max_y = self.bounds[3]
            if max_x <= min_x:
                raise ValueError('Max X cannot be less than or equal to min X')

            if max_y <= min_y:
                raise ValueError('Max Y cannot be less than or equal to min Y')
            self.useBounds = True
            self.scale_x = self.width // abs(max_x - min_x)
            self.scale_y = self.width // abs(max_y - min_y)
            bx = 0
            if min_x >= 0:
                bx = -(min_x * self.scale_x)
            else:
                bx = self.width - (max_x * self.scale_x)
            by = 0
            if min_y >= 0:
                by = -(min_y * self.scale_y)
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
            self.mouse_x = e.x
            self.mouse_y = e.y
            self.mouse_x = map(self.mouse_x,
                                          0,
                                          self.width,
                                          self.bounds[0],
                                          self.bounds[2])
            self.mouse_y = map(self.mouse_y,
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
        #self.__get_mouse_positions(event)
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
        if self.mouseDownFunction:
            self.mouseDownFunction(self, 'left')

    def __right_mouse_btn_down(self, event):
        if self.mouseDownFunction:
            self.mouseDownFunction(self, 'right')

    def __left_mouse_btn_up(self, event):
        if self.mouseUpFunction:
            self.mouseUpFunction(self, 'left')

    def __right_mouse_btn_up(self, event):
        if self.mouseUpFunction:
            self.mouseUpFunction(self, 'right')
    '''-------------------------------------------------------------'''
    def __show_stats(self):
        c = self.canvas
        c.push()
        c.translate(0, 0)
        c.font_color('white')
        c.text_anchor('nw')
        c.font_family('12')

        str = (
            f'fps:        {(self.tick / (time.time() - self.__start_time)):.2f}\n'\
            f'tick:       {self.tick}\n\n'\

            f'win width:  {self.width}\n'\
            f'win height: {self.height}\n\n'\

            f'mouse left: {self.mouse_left}\n'\
            f'mouse top:  {self.mouse_top}\n'\
            f'mouse x:    {self.mouse_x:.2f}\n'\
            f'mouse y:    {self.mouse_y:.2f}'
        )
        obj = c.text(24, 24, str)
        bounds = c.handle.bbox(obj)
        c.fill('black')
        c.stroke('black')
        c.rect(bounds[0] - 16, bounds[1] - 16, bounds[2] + 16, bounds[3] + 16, alpha = .7)
        c.bring_to_front(obj)
        c.pop()

    def __setup(self):
        if callable(self.setupFunction):
            self.setupFunction(self)
            if self.showStats:
                self.__show_stats()
        else:
            raise TypeError('Setup function is either undefined or not callable!')
        
    def __animate(self):
        if self.autoClear == True:
            self.canvas.clear('all')        
            self.canvas.clear_data()
        else:
            if self.showGrid:
                self.canvas.showGrid()
        if callable(self.drawFunction):
            self.tick += 1
            mx = self.master.winfo_pointerx() - self.master.winfo_rootx()
            my = self.master.winfo_pointery() - self.master.winfo_rooty()
            if mx > 0 and mx <= self.width and my > 0 and my <= self.height:
                self.__get_mouse_positions(Vector.Vector(mx, my))
            self.drawFunction(self)
        else:
            raise Exception('Draw function is either undefined or not callable!')

        if self.export_path != '':
            self.canvas.export_frame()

        if self.showStats:
                self.__show_stats()

        self.canvas.handle.after(self.interval, self.__animate)

    def __on_closing(self):
        if self.export_path != '':
            print('Saving frames as GIF file... please wait!')
            self.canvas.save_frames(self.export_path, self.interval)
            print('Done!')
        self.master.destroy()

    def __on_escape_key(self, e):
        self.master.destroy()

    def __on_key_press(self, e):
        if self.keyPressFunc:
            self.keyPressFunc(self, e)

    def __on_key_release(self, e):
        if self.keyReleaseFunc:
            self.keyReleaseFunc(self, e)