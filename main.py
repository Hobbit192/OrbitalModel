import time

import pygame
import pygame_gui

from bodies import all_sprites_list, bodies
from constants import BACKGROUND, ORANGE, G, scale_factors
from gui import (ui_manager, mass_entry_text, mass_slider, radius_entry_text, radius_slider, red_slider, red_entry_text,
                 green_slider, green_entry_text, blue_slider, blue_entry_text, info_panel, name_label,
                 power_entry_text_1, power_entry_text_2, planet_label, speed_value_label)
from setup import body_surface, ui_surface, screen_info, screen
from vectors import Vector
from maths import standard_form, round_to_sf

# Initialise
pygame.init()
info = pygame.display.Info()

# Vector constants
null_vector = Vector(0,0)
screen_centre = Vector(info.current_w / 2, (info.current_h - 80) / 2)
offset = null_vector
zoom = 1


def convert_to_screen(vector):
    return screen_centre + (vector * (1 / scale_factors.distance_scale_factor) + offset) * zoom


def convert_from_screen(vector):
    return ((vector - screen_centre) * (1 / zoom) - offset) * scale_factors.distance_scale_factor


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
                        body.move(null_vector)
                        other.move(null_vector)

                # Find forces from other bodies and acceleration of this body
                net_acceleration += body_to_other * (G * other.mass / separation ** 3)

        delta_v_list.append(net_acceleration)

    # Move
    for z in zip(bodies, delta_v_list):
        z[0].move(z[1])

    if drawing_elapsed >= 16:

        keys = pygame.key.get_pressed()

        offset += Vector(keys[pygame.K_LEFT] - keys[pygame.K_RIGHT], keys[pygame.K_UP] - keys[pygame.K_DOWN]) * (10 / zoom)

        if keys[pygame.K_MINUS]:
            zoom /= 1.01

            for body in bodies:
                body.sprite.set_radius(body.radius / (scale_factors.radius_scale_factor / zoom), body.position)

        if keys[pygame.K_EQUALS]:
            zoom *= 1.01

            for body in bodies:
                body.sprite.set_radius(body.radius / (scale_factors.radius_scale_factor / zoom), body.position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            ui_manager.process_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if not info_panel.relative_rect.collidepoint(event.pos) or info_panel.visible == 0:
                    for body in bodies:
                        click_pos = convert_from_screen(Vector(event.pos[0], event.pos[1]))
                        if (click_pos - body.position).magnitude() <= body.radius:
                            dragging = True
                            selected_body = body
                            selected = True

                            # First time selected info to be displayed
                            info_panel.show()
                            name_label.set_text(selected_body.name.upper())

                            mass_string = str(round(standard_form(selected_body.mass)[0], 2))
                            mass_entry_text.set_text(mass_string)
                            power_string_1 = str(standard_form(selected_body.mass)[1])
                            power_entry_text_1.set_text(power_string_1)

                            radius_string = str(round(standard_form(selected_body.radius)[0], 2))
                            radius_entry_text.set_text(radius_string)
                            power_string_2 = str(standard_form(selected_body.radius)[1])
                            power_entry_text_2.set_text(power_string_2)

                            planet_label.update_colour(selected_body.colour)

                            red_entry_text.set_text(str(selected_body.colour[0]))
                            green_entry_text.set_text(str(selected_body.colour[1]))
                            blue_entry_text.set_text(str(selected_body.colour[2]))
                            break

                        selected = False
                        info_panel.hide()

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    selected_body.position = convert_from_screen(Vector(event.pos[0], event.pos[1]))
                    selected_body.velocity = Vector(0, 0)

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == power_entry_text_1:
                    selected_body.mass = float(mass_entry_text.get_text()) * 10 ** int(power_entry_text_1.get_text())

                elif event.ui_element == power_entry_text_2:
                    selected_body.radius = float(radius_entry_text.get_text()) * 10 ** int(power_entry_text_2.get_text())
                    selected_body.update_sprite(selected_body.colour, selected_body.radius)

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == mass_slider:
                    mass_entry_text.set_text("{:.2f}".format(mass_slider.get_current_value()))
                    selected_body.mass = float(mass_entry_text.get_text()) * 10 ** int(power_entry_text_1.get_text())

                elif event.ui_element == radius_slider:
                    radius_entry_text.set_text("{:.2f}".format(radius_slider.get_current_value()))
                    selected_body.radius = float(radius_entry_text.get_text()) * 10 ** int(power_entry_text_2.get_text())
                    selected_body.update_sprite(selected_body.colour, selected_body.radius)

                elif event.ui_element == red_slider:
                    rounded_red_slider = round(red_slider.get_current_value())
                    red_entry_text.set_text(str(rounded_red_slider))
                    new_red = [int(red_entry_text.get_text()), selected_body.colour[1], selected_body.colour[2]]
                    selected_body.colour = tuple(new_red)
                    selected_body.update_sprite(selected_body.colour, selected_body.radius)
                    planet_label.update_colour(selected_body.colour)

                elif event.ui_element == green_slider:
                    rounded_green_slider = round(green_slider.get_current_value())
                    green_entry_text.set_text(str(rounded_green_slider))
                    new_green = [selected_body.colour[0], int(green_entry_text.get_text()), selected_body.colour[2]]
                    selected_body.colour = tuple(new_green)
                    selected_body.update_sprite(selected_body.colour, selected_body.radius)
                    planet_label.update_colour(selected_body.colour)

                elif event.ui_element == blue_slider:
                    rounded_blue_slider = round(blue_slider.get_current_value())
                    blue_entry_text.set_text(str(rounded_blue_slider))
                    new_blue = [selected_body.colour[0], selected_body.colour[1], int(blue_entry_text.get_text())]
                    selected_body.colour = tuple(new_blue)
                    selected_body.update_sprite(selected_body.colour, selected_body.radius)
                    planet_label.update_colour(selected_body.colour)

        # Sync up slider and text values for all sliders
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

        for body in bodies:

            # Draw body sprites
            body.sprite.set_pos(convert_to_screen(body.position))

        body_surface.fill(BACKGROUND)
        all_sprites_list.draw(body_surface)

        # Information  that needs to be constantly updated to display if the body is selected
        if selected:
            pygame.draw.line(body_surface, ORANGE,
                             (convert_to_screen(selected_body.position).x, convert_to_screen(selected_body.position).y),
                             (convert_to_screen(selected_body.position).x + selected_body.velocity.x / scale_factors.velocity_scale_factor,
                              convert_to_screen(selected_body.position).y + selected_body.velocity.y / scale_factors.velocity_scale_factor),
                             5)

            speed_value_label.set_text(str(round_to_sf(selected_body.velocity.magnitude(), 4)) + " m/s")

        drawing_elapsed = 0
        ui_manager.update(time_delta)
        ui_surface.fill(BACKGROUND)
        ui_manager.draw_ui(ui_surface)

        body_surface.blit(ui_surface, (0, 0))
        screen.blit(body_surface, (0, 0))

        ui_manager.draw_ui(ui_surface)
        pygame.display.flip()
