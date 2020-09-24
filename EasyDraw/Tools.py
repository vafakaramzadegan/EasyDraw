class Tools:
    '''Class to define Math functions'''

    # linear interpolation between two points
    def lerp(self, v0, v1, t):
        return (1 - t) * v0 + t * v1

    # map value
    def map(self, x, a, b, c, d):
        y = (x - a) / (b - a) * (d - c) + c
        return y


def constrain(n, minn, maxn):
    return max(min(maxn, n), minn)

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

def map(x, a, b, c, d):
        y = (x - a) / (b - a) * (d - c) + c
        return y