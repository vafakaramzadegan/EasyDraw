from EasyDraw.Tools import Tools

import math
import random

class Vector(object):
    '''Class to define 2D vectors''' 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __check_type(self, v):
        if not isinstance(v, Vector):
            raise ValueError('The second parameter is not an EasyDraw vector type!')

    # simple math operations -------------------------------------------------------
    def __add__(self, v2):
        self.__check_type(v2)
        return Vector(self.x + v2.x, self.y + v2.y)

    def __sub__(self, v2):
        self.__check_type(v2)
        return Vector(self.x - v2.x, self.y - v2.y)

    def __mul__(self, v2):
        # dot product
        if isinstance(v2, Vector):
            return Vector(self.x * v2.x, self.y * v2.y)
        # scalar mul
        elif isinstance(v2, (int, float)):
            return Vector(self.x * v2, self.y * v2)

    def __rmul__(self, v2):
        return self * v2

    def __truediv__(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError('The right-hand side must be int or float!')
        return Vector(self.x / val, self.y / val)
    # ------------------------------------------------------------------------------
    
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # return angle between this vector and another
    def angle_between(self, v2):
        self.__check_type(v2)
        return -math.degrees(math.atan2(self.x * v2.y - self.y * v2.x, self.x * v2.x + self.y * v2.y))

    # return distance from this vector to another
    def distance_from(self, v2):
        self.__check_type(v2)
        return math.sqrt(((self.x - v2.x) ** 2) + ((self.y - v2.y) ** 2))

    # return heading angle
    def heading(self):
        return self.angle_between(Vector(1, 0))

    # set vector magnitude
    def set_mag(self, mag):
        self.x *= mag
        self.y *= mag

    # return vector magnitude
    def mag(self):
        return self.length()

    def mag_square(self):
        return self.length() ** 2

    # limit vector length to a value
    def limit(self, max):
        mSq = self.mag_square()
        if (mSq > max ** 2):
            vec = (self / math.sqrt(mSq)) * max
            self.x = vec.x
            self.y = vec.y

    # normalize this vector
    def normalize(self):
        len = self.mag()
        if len != 0:
            vec = self * (1 / len)
            self.x = vec.x
            self.y = vec.y

    def copy(self):
        return Vector(self.x, self.y)

    # calculate lerp between this and another vector based on a value
    def lerp(self, v2, amount):
        self.__check_type(v2)
        t = Tools()
        x = t.lerp(self.x, v2.x, amount)
        y = t.lerp(self.y, v2.y, amount)
        return Vector(x, y)

# create a random unit vector
class RandomVector:
    def __new__(self):
        x = random.uniform(-1, 1)
        sign = random.choice([-1, 1])
        return Vector(x, math.sqrt(1 - (x ** 2)) * sign)

# create a vector from angle
class VectorFromAngle:
    def __new__(self, angle, length = 1):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return Vector(x, y)
