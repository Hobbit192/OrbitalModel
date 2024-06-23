from vectors import Vector

class ScaleFactor:
    def __init__(self, distance_scale_factor, radius_scale_factor, velocity_scale_factor):
        self.distance_scale_factor = distance_scale_factor
        self.radius_scale_factor = radius_scale_factor
        self.velocity_scale_factor = velocity_scale_factor


WHITE = (255, 255, 255)
BACKGROUND = (10, 5, 38)
ORANGE = (255, 85, 0)
G = 6.67430e-11
restitution_coefficient = 0.5

scale_factors = ScaleFactor(distance_scale_factor=2e4, radius_scale_factor=2e4, velocity_scale_factor=100)
