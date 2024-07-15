import pygame
from constants import WHITE, G, radius_scale_factor
from vectors import Vector, null_vector


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

    def update_sprite_info(self, colour, pixel_radius):
        self.colour = colour
        self.pixel_radius = pixel_radius
        self.image = pygame.Surface([pixel_radius * 2, pixel_radius * 2])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.circle(self.image, colour, (pixel_radius, pixel_radius), pixel_radius)
        self.rect = self.image.get_rect()


class Body:
    def __init__(self, mass, radius, velocity, position, colour, name):
        self.mass = mass
        self.radius = radius
        self.velocity = velocity
        self.position = position
        self.colour = colour
        self.name = name
        self.thrust_magnitude = 0
        self.thrust_angle = 0

        self.sprite = Sprite(colour, radius / radius_scale_factor)
        all_sprites_list.add(self.sprite)

    def update_sprite(self, colour, radius):
        self.sprite.update_sprite_info(colour, radius / radius_scale_factor)

    def separation(self, other):
        return (self.position - other.position).magnitude()

    def move(self, acceleration):
        new_velocity = self.velocity + acceleration
        new_position = self.position + (self.velocity + new_velocity) * 0.5
        self.velocity = new_velocity
        self.position = new_position


all_sprites_list = pygame.sprite.Group()

Earth = Body(9.972168e26, 8371.0e3, Vector(0, -10), Vector(0, 0), (18, 53, 36), "Earth")
Moon = Body(7.342e23, 1737.4e3, Vector(0, -7022), Vector(405400e3, 0), (128, 128, 128), "Moon")
Other = Body(4.5e22, 1000e3, Vector(-500, 6000), Vector(565400e3, 0), (255, 0, 0), "Other")
Minmus = Body(3.342e24, 4737.4e3, Vector(0, 11022), Vector(-405400e3, 0), (128, 128, 255), "Minmus")
Other2 = Body(9.5e25, 5898e3, Vector(0, -6000), Vector(-565400e3, 0), (76, 155, 120), "Other2")
Other3 = Body(9.5e25, 6438e3, Vector(8000, 0), Vector(0, 500000e3), (30, 20, 10), "Other3")
Other4 = Body(9.5e25, 6200e3, Vector(-8000, 0), Vector(0, -500000e3), (100, 97, 125), "Other4")
Other5 = Body(9.5e25, 5706e3, Vector(0, 8000), Vector(-965400e3, 0), (230, 222, 201), "Other5")
Other6 = Body(3e26, 4123e3, Vector(0, -6000), Vector(640000e3, 0), (176, 36, 204), "Other6")

bodies = [Earth, Moon, Other, Minmus, Other2, Other3, Other4, Other5, Other6]
