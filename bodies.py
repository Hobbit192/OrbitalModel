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

Earth = Body(mass=5.972168e24,
             radius=8371.0e3,
             velocity=Vector(0, 0),
             position=Vector(0, 0),
             colour=(18, 53, 36),
             name="Earth"
             )

Space_Station = Body(mass=450000,
                     radius=100e3,
                     velocity=Vector(0, (G * Earth.mass / (Earth.radius + 1000e3)) ** 0.5),
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

Snooker1 = Body(mass=10000e1,
              radius=100e3,
              velocity=Vector(0, 0),
              position=Vector(0,0),
              colour=(176, 176, 204),
              name="Snooker1"
              )

Snooker2 = Body(mass=10000e1,
              radius=100e3,
              velocity=null_vector,
              position=Vector((((200e3)**2)/2)**0.5, -(((200e3)**2)/2)**0.5),
              colour=(176, 36, 204),
              name="Snooker2"
              )
Snooker3 = Body(mass=10000e1,
              radius=100e3,
              velocity=Vector(0, 0),
              position=Vector((((200e3)**2)/2)**0.5, (((200e3)**2)/2)**0.5),
              colour=(176, 204, 36),
              name="Snooker3"
              )

Snooker4 = Body(mass=10000e1,
              radius=100e3,
              velocity=Vector(50, 0),
              position=Vector(-900e3,0),
              colour=(176, 36, 204),
              name="Snooker4"
              )


Rocket = Body(mass=10000e15,
              radius=100e3,
              velocity=Vector(1000, 00),
              position=Vector(Earth.radius+100e3, 100e3),
              colour=(176, 36, 204),
              name="Rocket"
              )

bodies = [Snooker4, Snooker1, Snooker2, Snooker3]
