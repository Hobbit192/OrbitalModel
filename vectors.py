from setup import centrex, centrey
from constants import distance_scale_factor


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

    def convert(self):
        return Vector(self.x / distance_scale_factor + centrex, self.y / distance_scale_factor + centrey)

    def convert_back(self):
        return Vector((self.x - centrex) * distance_scale_factor, (self.y - centrey) * distance_scale_factor)

    def dot(self, other):
        return self.x * other.x + self.y * other.y