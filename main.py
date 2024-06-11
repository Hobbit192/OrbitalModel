import pygame
from setup import body_surface, ui_surface, screen_info, screen
from constants import WHITE, BACKGROUND, ORANGE, G, scale_factors
from vectors import Vector
from bodies import all_sprites_list, bodies
from gui import (ui_manager, info_title_label, name_label, planet_label, mass_label, mass_entry_text, e_label_1,
                 power_entry_text_1, mass_unit_label, mass_slider, radius_label, radius_entry_text, e_label_2,
                 power_entry_text_2, radius_unit_label, radius_slider, red_label, red_slider, red_entry_text,
                 green_label, green_slider, green_entry_text, blue_label, blue_slider, blue_entry_text,
                 velocity_x_label, velocity_y_label, speed_label, emphasis_rect_1, emphasis_rect_2, emphasis_rect_3,
                 emphasis_rect_4, emphasis_rect_5, emphasis_rect_6, trajectories_label, window_visible)

# Initialise
pygame.init()


def convert_to_screen(vector):
    return Vector(vector.x / scale_factors.distance_scale_factor + screen_info.centre_x,
                  vector.y / scale_factors.distance_scale_factor + screen_info.centre_y)


def convert_from_screen(vector):
    return Vector((vector.x - screen_info.centre_x) * scale_factors.distance_scale_factor,
                  (vector.y - screen_info.centre_y) * scale_factors.distance_scale_factor)


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

while running:
    time_delta = clock.tick(1000)
    drawing_elapsed += time_delta
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_EQUALS:
                scale_factors.distance_scale_factor /= 1.1
                scale_factors.radius_scale_factor /= 1.1

                for body in bodies:
                    body.sprite.set_radius(body.radius / scale_factors.radius_scale_factor, body.position)

            if event.key == pygame.K_MINUS:
                scale_factors.distance_scale_factor *= 1.1
                scale_factors.radius_scale_factor *= 1.1

                for body in bodies:
                    body.sprite.set_radius(body.radius / scale_factors.radius_scale_factor, body.position)

            if event.key == pygame.K_UP:
                screen_info.centre_y += 20

            if event.key == pygame.K_DOWN:
                screen_info.centre_y -= 20

            if event.key == pygame.K_LEFT:
                screen_info.centre_x += 20

            if event.key == pygame.K_RIGHT:
                screen_info.centre_x -= 20

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for body in bodies:
                click_pos = convert_from_screen(Vector(event.pos[0], event.pos[1]))
                if (click_pos - body.position).magnitude() <= body.radius:
                    dragging = True
                    selected_body = body
                    selected = True
                    break

                selected = False

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                selected_body.position = convert_from_screen(Vector(event.pos[0], event.pos[1]))
                selected_body.velocity = Vector(0, 0)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # Move bodies
    deltav_list = []

    for body in bodies:
        net_acceleration = Vector(0, 0)

        for other in bodies:
            if other != body:
                separation = body.separation(other)
                body_to_other = other.position - body.position

                # Check for collisions

                if separation <= body.radius + other.radius:
                    c = (2 * (body.mass * other.mass) / (body.mass + other.mass) * body_to_other.dot(
                         body.velocity - other.velocity) / body_to_other.dot(body_to_other))

                    # Move until separated

                    body.move(body_to_other * (-c / body.mass))
                    other.move(body_to_other * (c / other.mass))

                    while body.separation(other) <= body.radius + other.radius:
                        body.move(Vector(0, 0))
                        other.move(Vector(0, 0))

            # Find forces from other bodies and acceleration of this body

                net_acceleration += body_to_other * (G * other.mass / separation ** 3)

        deltav_list.append(net_acceleration)

    # Move
    for z in zip(bodies, deltav_list):
        z[0].move(z[1])

    if drawing_elapsed >= 16:
        for body in bodies:

            # Draw body sprites
            body.sprite.set_pos(convert_to_screen(body.position))

        body_surface.fill(BACKGROUND)
        all_sprites_list.draw(body_surface)

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
                             (convert_to_screen(selected_body.position).x, convert_to_screen(selected_body.position).y),
                             (convert_to_screen(selected_body.position).x + selected_body.velocity.x / scale_factors.velocity_scale_factor,
                              convert_to_screen(selected_body.position).y + selected_body.velocity.y / scale_factors.velocity_scale_factor),
                             5)

        drawing_elapsed = 0
        #ui_manager.update(time_delta)
        #ui_manager.draw_ui(ui_surface)

        screen.blit(body_surface, (0, 0))
        body_surface.blit(ui_surface, (0, 0))

        pygame.display.flip()
