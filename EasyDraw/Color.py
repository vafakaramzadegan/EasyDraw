import random
from warnings import warn

class Color:
    def __init__(self):
        pass

    def hsv_to_rgb(self, HSV):
        '''convert an integer HSV tuple (value range from 0 to 255) to a RGB tuple'''
        # Unpack the HSV tuple for readability
        H, S, V = HSV
        # Check if the color is Grayscale
        if S == 0:
            R = V
            G = V
            B = V
            return (R, G, B)
        # Make hue 0-5
        region = H // 43
        # Find remainder part, make it from 0-255
        remainder = (H - (region * 43)) * 6; 
        # Calculate temp vars, doing integer multiplication
        P = (V * (255 - S)) >> 8
        Q = (V * (255 - ((S * remainder) >> 8))) >> 8
        T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8
        # Assign temp vars based on color cone region
        if region == 0:
            R = V
            G = T
            B = P
        elif region == 1:
            R = Q
            G = V
            B = P
        elif region == 2:
            R = P 
            G = V
            B = T
        elif region == 3:
            R = P
            G = Q
            B = V
        elif region == 4:
            R = T
            G = P
            B = V
        else: 
            R = V
            G = P
            B = Q
        return (R, G, B)

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb 

    def rgb(self, r, g, b):
        warn("Please use RGB class to build color: RGB(r, g, b)", DeprecationWarning, stacklevel = 2)
        return RGB(r, g, b)

    def hsv(self, h, s, v):
        warn("Please use HSV class to build color: HSV(h, s, v)", DeprecationWarning, stacklevel = 2)
        return HSV(h, s, v)
    
    def random(self):
        warn("Please use RandomColor class to build color: myColor = RandomColor()", DeprecationWarning, stacklevel = 2)
        return RandomColor()


# convert rgb value to hex
class RGB(object):
    def __new__(self, r, g, b):
        c = Color()
        return c.rgb_to_hex((r, g, b))

# convert hsv value to hex
class HSV(object):
    def __new__(self, h, s, v):
        c = Color()
        return c.rgb_to_hex(
            c.hsv_to_rgb((h, s, v))
        )

# blend two rgba colors
class BlendColors:
    def __new__(self, rgba1, rgba2):
        red   = (rgba1[0] * rgba1[3]) + (rgba2[0] * (1.0 - rgba2[3]))
        green = (rgba1[1] * rgba1[3]) + (rgba2[1] * (1.0 - rgba2[3]))
        blue  = (rgba1[2] * rgba1[3]) + (rgba2[2] * (1.0 - rgba2[3]))
        return (int(red), int(green), int(blue))

# generate random HEX color
class RandomColor:
    def __new__(self):
        color = tuple(random.sample(range(0, 255), 3))
        c = Color()
        return c.rgb_to_hex(color)