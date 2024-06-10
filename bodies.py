import pygame
from constants import WHITE, scale_factors, G
from vectors import Vector


class Sprite(pygame.sprite.Sprite):
    def __init__(self, colour, pixel_radius):
        super().__init__()

        self.colour = colour
        self.pixel_radius = pixel_radius
        self.image = pygame.Surface([pixel_radius * 2, pixel_radius * 2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.circle(self.image, colour, (pixel_radius, pixel_radius), pixel_radius)
        self.rect = self.image.get_rect()

    def set_pos(self, position):
        self.rect.x = position.x - self.pixel_radius
        self.rect.y = position.y - self.pixel_radius



    def set_radius(self, pixel_radius, position):
        self.pixel_radius = pixel_radius
        self.image = pygame.Surface([pixel_radius * 2, pixel_radius * 2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.circle(self.image, self.colour, (pixel_radius, pixel_radius), pixel_radius)
        self.rect = self.image.get_rect()

        self.rect.x = position.x - self.pixel_radius
        self.rect.y = position.y - self.pixel_radius


class Body:
    def __init__(self, mass, radius, velocity, position, colour, name):
        self.mass = mass
        self.radius = radius
        self.velocity = velocity
        self.position = position
        self.colour = colour
        self.name = name
        #self.last_displayed = position

        self.sprite = Sprite(colour, radius / scale_factors.radius_scale_factor)
        all_sprites_list.add(self.sprite)

    def separation(self, other):
        return (self.position-other.position).magnitude()

    def move(self, acceleration):
        new_velocity = self.velocity + acceleration
        new_position = self.position + (self.velocity + new_velocity) * 0.5
        self.velocity = new_velocity
        self.position = new_position


all_sprites_list = pygame.sprite.Group()

Earth = Body(mass=5.972168e24,
             radius=8371.0e3,
             velocity=Vector(0, 0),
             position=Vector(0, 0),
             colour=(18, 53, 36),
             name="Earth"
             )

Space_Station = Body(mass=450000,
                     radius=100e3,
                     velocity=Vector(0,0), #Vector(0, (G * Earth.mass / (Earth.radius + 1000e3)) ** 0.5),
                     position=Vector(Earth.radius + 1000e3, 0),
                     colour=(255, 254, 255),
                     name="ISS"
                     )

Moon = Body(mass=7.342e22,
            radius=1737.4e3,
            velocity=Vector(0, (G * Earth.mass / (Earth.radius + 384400e3)) ** 0.5),
            position=Vector(8371.0e3 + 384400e3, 0),
            colour=(128, 128, 128),
            name="Moon"
            )

Rocket = Body(mass=10000e15,
              radius=100e3,
              velocity=Vector(4000, 00),
              position=Vector(Earth.radius+100e3, 100e3),
              colour=(176, 36, 204),
              name="Rocket"
              )

bodies = [Earth, Space_Station, Moon, Rocket]
