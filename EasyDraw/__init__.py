import tkinter as tk
from EasyDraw import Color
from EasyDraw import Canvas
from EasyDraw import Tools

class EasyDraw(object):
    '''EasyDraw main class'''
    def __init__(self, **kwargs):
        self.width       = kwargs.get('width', 400)
        self.height      = kwargs.get('height', 400)
        self.autoClear   = kwargs.get('autoClear', True)  
        self.interval    = kwargs.get('fps', 30)
        self.export_path = kwargs.get('exportPath', '')
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_left = 0
        self.mouse_top = 0
        if self.interval not in range(0, 1001):
            raise ValueError("invalid fps value should be between 1 and 1000 but '%d' was entered." % self.interval)
        self.interval  = 1000 // self.interval
        
        master         = tk.Tk()
        self.master    = master
        master.bind('<Motion>', self.__motion_event)
        master.title(kwargs.get('title', 'EasyDraw App'))
        master.protocol("WM_DELETE_WINDOW", self.__on_closing)

        self.bg_color = kwargs.get('background', 'silver')
        self.canvas = Canvas.Canvas(master,
                            width = self.width,
                            height = self.height,
                            background = self.bg_color)

        self.tools = Tools.Tools()
        self.color = Color.Color()

        self.setupFunction  = kwargs.get('setupFunc', None)
        self.drawFunction   = kwargs.get('drawFunc', None)
        self.motionFunction = kwargs.get('motionFunc', None)
        

        master.after(100, self.__setup())
        master.after(100, self.__animate())
        master.mainloop()
        

    def __motion_event(self, event):
        self.mouse_x = event.x - self.canvas.get_center_pos()[0]
        self.mouse_y = event.y - self.canvas.get_center_pos()[1]
        self.mouse_left = event.x
        self.mouse_top = event.y
        if self.motionFunction:
            self.motionFunction(self)
        
    def __setup(self):
        if callable(self.setupFunction):
            self.setupFunction(self)
        else:
            raise TypeError('Setup function is either undefined or not callable!')
        
    def __animate(self):
        if self.autoClear == True:
            self.canvas.clear('all')
            self.canvas.handle.create_rectangle(0, 0, self.width, self.height, fill = self.bg_color, outline = self.bg_color)
        
            self.canvas.clear_data()

        if callable(self.drawFunction):
            self.drawFunction(self)
        else:
            raise Exception('Draw function is either undefined or not callable!')

        if self.export_path != '': self.canvas.export_frame()
        self.canvas.handle.after(self.interval, self.__animate)

    def __on_closing(self):
        if self.export_path != '':
            print('Saving frames as GIF file... please wait!')
            self.canvas.save_frames(self.export_path, self.interval)
            print('Done!')
        self.master.destroy()
