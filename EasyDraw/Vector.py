import math
import random

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Addition
    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    # Subtraction
    def __sub__(self, v2):
        return Vector(self.x - v2.x, self.y - v2.y)

    # Element-wise multiplication or scalar multiplication
    def __mul__(self, v2):
        if isinstance(v2, Vector):
            return Vector(self.x * v2.x, self.y * v2.y)
        elif isinstance(v2, (int, float)):
            return Vector(self.x * v2, self.y * v2)

    # Right-side scalar multiplication
    def __rmul__(self, v2):
        return self * v2

    # Division by scalar
    def __truediv__(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError('The right-hand side must be int or float!')
        return Vector(self.x / val, self.y / val)

    # Dot product
    def dot(self, v2):
        return self.x * v2.x + self.y * v2.y

    # Cross product
    def cross(self, v2):
        return self.x * v2.y - self.y * v2.x

    # Negation
    def __neg__(self):
        return Vector(-self.x, -self.y)

    # Euclidean length of the vector
    def length(self):
        return math.hypot(self.x, self.y)

    # Angle between two vectors
    def angle_between(self, v2):
        return -math.degrees(math.atan2(self.x * v2.y - self.y * v2.x, self.x * v2.x + self.y * v2.y))

    # Euclidean distance between two vectors
    def distance_from(self, v2):
        return math.hypot(self.x - v2.x, self.y - v2.y)

    # Heading angle of the vector
    def heading(self):
        return self.angle_between(Vector(1, 0))

    # Set the magnitude of the vector
    def set_mag(self, mag):
        self.x *= mag
        self.y *= mag

    # Magnitude of the vector
    def mag(self):
        return self.length()

    # Square of the magnitude
    def mag_square(self):
        return self.length() ** 2

    # Limit the length of the vector
    def limit(self, max_value):
        mSq = self.mag_square()
        if mSq > max_value ** 2:
            vec = (self / math.sqrt(mSq)) * max_value
            self.x, self.y = vec.x, vec.y

    # Normalize the vector
    def normalize(self):
        l = self.mag()
        if l != 0:
            vec = self * (1 / l)
            self.x, self.y = vec.x, vec.y

    # Create a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Linear interpolation between two vectors
    def lerp(self, v2, amount):
        x = self.x + (v2.x - self.x) * amount
        y = self.y + (v2.y - self.y) * amount
        return Vector(x, y)

    # Projection of this vector onto another vector
    def project(self, v2):
        scalar = self.dot(v2) / v2.mag_square()
        return v2 * scalar

    # Reflection of this vector across a surface with a given normal vector
    def reflect(self, normal):
        reflected = self - normal * (2 * self.dot(normal) / normal.mag_square())
        return reflected

# Create a random unit vector
class RandomVector:
    def __new__(self):
        x = random.uniform(-1, 1)
        sign = random.choice([-1, 1])
        return Vector(x, math.sqrt(1 - x ** 2) * sign)

# Create a vector from an angle
class VectorFromAngle:
    def __new__(self, cls, angle, length=1):
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
        return Vector(x, y)
