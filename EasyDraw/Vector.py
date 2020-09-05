import math

class Vector(object):
    '''Class to define 2D vectors'''
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __check_type(self, v):
        if not isinstance(v, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')

    def __add__(self, v2):
        self.__check_type(v2)
        return Vector(self.a + v2.a, self.b + v2.b)

    def __sub__(self, v2):
        self.__check_type(v2)
        return Vector(self.a - v2.a, self.b - v2.b)

    def __mul__(self, v2):
        # scalar mul
        if isinstance(v2, Vector):
            return Vector(self.a * v2.a, self.b * v2.b)
        # dot product
        elif isinstance(v2, (int, float)):
            return Vector(self.a * v2, self.b * v2)

    def __rmul__(self, v2):
        return self * v2
    
    def __neg__(self):
        return Vector(-self.a, -self.b)

    def length(self):
        return math.sqrt(self.a ** 2 + self.b ** 2)

    def angle_between(self, v2):
        self.__check_type(v2)
        return math.degrees(math.atan2(self.a * v2.b - self.b * v2.a, self.a * v2.a + self.b * v2.b))
