import math

class Vector(object):
    '''Class to define 2D vectors'''
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __check_type(self, v):
        if not isinstance(v, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')

    def __add__(self, v2):
        self.__check_type(v2)
        return Vector(self.x + v2.x, self.y + v2.y)

    def __sub__(self, v2):
        self.__check_type(v2)
        return Vector(self.x - v2.x, self.y - v2.y)

    def __mul__(self, v2):
        # scalar mul
        if isinstance(v2, Vector):
            return Vector(self.x * v2.x, self.y * v2.y)
        # dot product
        elif isinstance(v2, (int, float)):
            return Vector(self.x * v2, self.y * v2)

    def __rmul__(self, v2):
        return self * v2
    
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # return angle between this and another vector
    def angle_between(self, v2):
        self.__check_type(v2)
        return math.degrees(math.atan2(self.x * v2.y - self.y * v2.x, self.x * v2.x + self.y * v2.y))

    # return distance from this to another vector
    def distance_from(self, v2):
        self.__check_type(v2)
        return math.sqrt(((self.x - v2.x) ** 2) + ((self.y - v2.y) ** 2))