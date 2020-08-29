import tkinter as tk
from EasyDraw import color
from EasyDraw import canvas
from EasyDraw import tools

class EasyDraw(object):
    '''EasyDraw main class'''
    def __init__(self, **kwargs):
        self.width     = kwargs.get('width', 400)
        self.height    = kwargs.get('height', 400)
        self.autoClear = kwargs.get('autoClear', True)  
        self.interval  = kwargs.get('fps', 30)
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
        
        self.canvas = canvas.Canvas(master,
                            width = self.width,
                            height = self.height,
                            background = kwargs.get('background', 'silver'))

        self.tools = tools.Tools()
        self.color = color.Color()

        self.setupFunction  = kwargs.get('setupFunc', None)
        self.drawFunction   = kwargs.get('drawFunc', None)
        self.motionFunction = kwargs.get('motionFunc', None)
        
        self.setup()
        self.animate()
        master.mainloop()

    def __motion_event(self, event):
        self.mouse_x = event.x - self.canvas.center_x
        self.mouse_y = event.y - self.canvas.center_y
        self.mouse_left = event.x
        self.mouse_top = event.y
        if self.motionFunction:
            self.motionFunction(self)
        
    def setup(self):
        self.setupFunction(self)
        
    def animate(self):
        if self.autoClear: self.canvas.clear('all')
        self.drawFunction(self)
        self.canvas.handle.after(self.interval, self.animate)