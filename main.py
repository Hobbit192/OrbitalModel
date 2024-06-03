import pygame
import pygame_gui
import os

# Colours
WHITE = (255, 255, 255)
BACKGROUND = (10, 5, 38)
ORANGE = (255, 85, 0)
YELLOW = (255, 255, 0)

# Classes
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

class Body():
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

# Constants and initialise
G = 6.67430e-11
restitution_coefficient = 0.5
distance_scale_factor = 2e4
velocity_scale_factor = 100
radius_scale_factor = 2e4
pygame.init()
all_sprites_list = pygame.sprite.Group()

# Setup window and surfaces
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,30'
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h - 80

window_size = (screen_width, screen_height)
centrex = screen_width / 2
centrey = screen_height / 2
screen = pygame.display.set_mode(window_size)

trail_surface = pygame.Surface(window_size, pygame.SRCALPHA)
trail_surface.fill((255, 255, 255, 0))
body_surface = pygame.Surface(window_size)
screen.blit(body_surface, (0, 0))
body_surface.blit(trail_surface, (0, 0))

ui_surface = pygame.Surface(window_size)
ui_surface.fill(WHITE)
ui_surface.set_colorkey(WHITE)
manager = pygame_gui.UIManager((1536, 802))
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='Say Hello', manager=manager)

icon = pygame.image.load("black-hole-256x256.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Orbital Simulator", "OrbitSim")

# Define Bodies

Earth = Body(5.972168e24, 8371.0e3, Vector(0, 0), Vector(0, 0), (18, 53, 36), "Earth")
Space_Station = Body(450000, 100e3, Vector(0, (G * Earth.mass / (Earth.radius + 1000e3)) ** 0.5), Vector(8371.0e3 + 1000e3, 0), (255, 254, 255), "ISS")
Moon = Body(7.342e22, 1737.4e3, Vector(0, (G * Earth.mass / (Earth.radius + 384400e3)) ** 0.5), Vector(8371.0e3 + 384400e3, 0), (128, 128, 128), "Moon")
Rocket = Body(10000, 100e3, Vector(2000, 9000), Vector(Earth.radius, 0), (176, 36, 204), "Rocket")

bodies = [Earth, Space_Station, Moon, Rocket]
all_sprites_list.update()
body_surface.fill(BACKGROUND)
all_sprites_list.draw(body_surface)
pygame.display.flip()

# ---------------------------------------- Main Program Loop -----------------------------------------------------------
running = True
dragging = False
selected = False
clock = pygame.time.Clock()
clock.tick()
simulation_elapsed = 0
drawing_elapsed = 0
print(Vector(7,8))

while running:
    delta = clock.tick(1000)
    simulation_elapsed += delta
    drawing_elapsed += delta
    #time_delta = clock.tick(6000)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_EQUALS:
                distance_scale_factor /= 1.1
                radius_scale_factor /= 1.1

                for body in bodies:
                    body.sprite.set_radius(body.radius / radius_scale_factor, body.position)

            if event.key == pygame.K_MINUS:
                distance_scale_factor *= 1.1
                radius_scale_factor *= 1.1

                for body in bodies:
                    body.sprite.set_radius(body.radius / radius_scale_factor, body.position)

            if event.key == pygame.K_UP:
                centrey += 20

            if event.key == pygame.K_DOWN:
                centrey -= 20

            if event.key == pygame.K_LEFT:
                centrex += 20

            if event.key == pygame.K_RIGHT:
                centrex -= 20

        #manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for body in bodies:
                if body.sprite.rect.collidepoint(event.pos):
                    dragging = True
                    selected_body = body
                    selected = True

                    # Create GUI window elements
                    details_window = pygame_gui.elements.UIWindow(
                        rect=pygame.Rect((50,50),(100,100)),
                        manager= manager,
                        window_display_title="Test window"
                    )

                    break

                selected = False

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                selected_body.position = Vector(event.pos[0], event.pos[1]).convert_back()
                selected_body.velocity = Vector(0, 0)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # Accelerate bodies
    for body in bodies:
        acceleration_total = Vector(0, 0)

        for other in bodies:
            # Find forces from other bodies and acceleration of this body
            if body != other:
                body_to_other = other.position - body.position

                acceleration_magnitude = G * other.mass / body_to_other.magnitude() ** 2
                acceleration = body_to_other * (acceleration_magnitude / body_to_other.magnitude())

                acceleration_total += acceleration

                if body_to_other.magnitude() <= body.radius + other.radius:
                    print("COLLISTION!")
                    c = (2 * (body.mass * other.mass) / (body.mass + other.mass) * body_to_other.dot(body.velocity - other.velocity)
                         / body_to_other.dot(body_to_other))

                    print("Body velocity before = ",body.velocity)

                    body.velocity = body.velocity - (body_to_other * (c / body.mass))
                    other.velocity = other.velocity + (body_to_other * (c / other.mass))

                    print("Body velocity after = ",body.velocity)


        body.move(acceleration_total)

    if drawing_elapsed >= 16:
        for body in bodies:
            # Draw tracers
            #pygame.draw.circle(trail_surface, body.colour, (body.last_displayed.convert().x,
            #                                                body.last_displayed.convert().y), 1)

            # Draw body sprites
            body.sprite.set_pos(body.position.convert())
            body.last_displayed = body.position
            body_surface.fill(BACKGROUND)
            all_sprites_list.draw(body_surface)

            #body_surface.blit(trail_surface, (0, 0))

        # Information to display if the body is selected
        if selected:
            font = pygame.font.Font('GillSans.ttf', 32)
            name_text = font.render(selected_body.name, True, WHITE, selected_body.colour)
            name_rect = name_text.get_rect()
            name_rect.center = (75, 75)
            body_surface.blit(name_text, name_rect)

            velocity_text = font.render("Speed: " + str(selected_body.velocity.magnitude() // 1) + " m/s", True,
                                        WHITE, selected_body.colour)
            velocity_rect = velocity_text.get_rect()
            velocity_rect.center = (145, 110)
            body_surface.blit(velocity_text, velocity_rect)

            pygame.draw.line(body_surface, ORANGE,
                             (selected_body.position.convert().x, selected_body.position.convert().y),
                             (selected_body.position.convert().x + selected_body.velocity.x / velocity_scale_factor,
                              selected_body.position.convert().y + selected_body.velocity.y / velocity_scale_factor),
                             5)

        drawing_elapsed = 0
        screen.blit(body_surface, (0, 0))
        #manager.update(time_delta)
        #manager.draw_ui(ui_surface)
        pygame.display.flip()

