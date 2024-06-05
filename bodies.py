import pygame
from constants import WHITE, radius_scale_factor, G
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
        self.last_displayed = position

        self.sprite = Sprite(colour, radius / radius_scale_factor)
        all_sprites_list.add(self.sprite)

    def move(self, acceleration):
        new_velocity = self.velocity + acceleration * 0.1
        new_position = self.position + (self.velocity + new_velocity) * 0.5 * 0.1
        self.velocity = new_velocity
        self.position = new_position


all_sprites_list = pygame.sprite.Group()

Earth = Body(5.972168e24, 8371.0e3, Vector(0, 0), Vector(0, 0), (18, 53, 36), "Earth")
Space_Station = Body(450000, 100e3, Vector(0, (G * Earth.mass / (Earth.radius + 1000e3)) ** 0.5), Vector(8371.0e3 + 1000e3, 0), (255, 254, 255), "ISS")
Moon = Body(7.342e22, 1737.4e3, Vector(0, (G * Earth.mass / (Earth.radius + 384400e3)) ** 0.5), Vector(8371.0e3 + 384400e3, 0), (128, 128, 128), "Moon")
Rocket = Body(10000, 100e3, Vector(2000, 9000), Vector(Earth.radius, 0), (176, 36, 204), "Rocket")

bodies = [Earth, Space_Station, Moon, Rocket]