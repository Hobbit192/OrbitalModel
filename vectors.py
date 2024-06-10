from setup import screen_info
from constants import scale_factors


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, multiplier):
        return Vector(self.x * multiplier, self.y * multiplier)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

    def transform(self, translation, scale):
        return (self+translation)*scale

    def convert(self):
        return Vector(self.x / scale_factors.distance_scale_factor + screen_info.centre_x,
                      self.y / scale_factors.distance_scale_factor + screen_info.centre_y)

    def convert_back(self):
        return Vector((self.x - screen_info.centre_x) * scale_factors.distance_scale_factor,
                      (self.y - screen_info.centre_y) * scale_factors.distance_scale_factor)

    def dot(self, other):
        return self.x * other.x + self.y * other.y