import pygame
import pygame_gui

from bodies import all_sprites_list, bodies
from constants import BACKGROUND, ORANGE, G, scale_factors
from gui import (ui_manager, mass_entry_text, mass_slider, radius_entry_text, radius_slider, red_slider, red_entry_text,
                 green_slider, green_entry_text, blue_slider, blue_entry_text, info_panel)
from setup import body_surface, ui_surface, screen_info, screen
from vectors import Vector

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

        ui_manager.process_events(event)

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

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == mass_slider:
                rounded_mass_slider = round(mass_slider.get_current_value(), 2)
                mass_entry_text.set_text(str(rounded_mass_slider))

            elif event.ui_element == radius_slider:
                rounded_radius_slider = round(radius_slider.get_current_value(), 2)
                radius_entry_text.set_text(str(rounded_radius_slider))

            elif event.ui_element == red_slider:
                rounded_red_slider = round(red_slider.get_current_value())
                red_entry_text.set_text(str(rounded_red_slider))

            elif event.ui_element == green_slider:
                rounded_green_slider = round(green_slider.get_current_value())
                green_entry_text.set_text(str(rounded_green_slider))

            elif event.ui_element == blue_slider:
                rounded_blue_slider = round(blue_slider.get_current_value())
                blue_entry_text.set_text(str(rounded_blue_slider))

    mass_slider_value = mass_slider.get_current_value()
    mass_text = mass_entry_text.get_text()
    if mass_text and float(mass_text) != mass_slider_value:
        mass_slider.set_current_value(float(mass_text))

    radius_slider_value = radius_slider.get_current_value()
    radius_text = radius_entry_text.get_text()
    if radius_text and float(radius_text) != radius_slider_value:
        radius_slider.set_current_value(float(radius_text))

    red_slider_value = red_slider.get_current_value()
    red_text = red_entry_text.get_text()
    if red_text and int(red_text) != red_slider_value:
        red_slider.set_current_value(int(red_text))

    blue_slider_value = blue_slider.get_current_value()
    blue_text = blue_entry_text.get_text()
    if blue_text and int(blue_text) != blue_slider_value:
        blue_slider.set_current_value(int(blue_text))

    green_slider_value = green_slider.get_current_value()
    green_text = green_entry_text.get_text()
    if green_text and int(green_text) != green_slider_value:
        green_slider.set_current_value(int(green_text))

    # Move bodies
    delta_v_list = []

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

        delta_v_list.append(net_acceleration)

    # Move
    for z in zip(bodies, delta_v_list):
        z[0].move(z[1])

    if drawing_elapsed >= 16:
        for body in bodies:

            # Draw body sprites
            body.sprite.set_pos(convert_to_screen(body.position))

        body_surface.fill(BACKGROUND)
        all_sprites_list.draw(body_surface)

        # Information to display if the body is selected
        if selected:
            #info_panel.show()

            pygame.draw.line(body_surface, ORANGE,
                             (convert_to_screen(selected_body.position).x, convert_to_screen(selected_body.position).y),
                             (convert_to_screen(selected_body.position).x + selected_body.velocity.x / scale_factors.velocity_scale_factor,
                              convert_to_screen(selected_body.position).y + selected_body.velocity.y / scale_factors.velocity_scale_factor),
                             5)

        else:
            #info_panel.hide()
            pass

        drawing_elapsed = 0
        ui_manager.update(time_delta)
        ui_surface.fill(BACKGROUND)

        screen.blit(body_surface, (0, 0))
        body_surface.blit(ui_surface, (0, 0))

        ui_manager.draw_ui(ui_surface)
        pygame.display.flip()
