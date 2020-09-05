import math

class Vector(object):
    '''Class to define 2D vectors'''
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, v2):
        if not isinstance(v2, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')
        return Vector(self.a + v2.a, self.b + v2.b)

    def __sub__(self, v2):
        if not isinstance(v2, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')
        return Vector(self.a - v2.a, self.b - v2.b)

    def __mul__(self, v2):
        if not isinstance(v2, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')
        return Vector(self.a * v2.a, self.b * v2.b)
    
    def __neg__(self):
        return Vector(-self.a, -self.b)

    def __and__(self, v2):
        if not isinstance(v2, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')
        return (self.a * v2.b) + (self.b * v2.a)


    def length(self):
        return math.sqrt(self.a ** 2 + self.b ** 2)

    def angle_between(self, v2):
        if not isinstance(v2, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')
        return math.degrees(math.atan2(self.a * v2.b - self.b * v2.a, self.a * v2.a + self.b * v2.b))