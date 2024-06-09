import pygame
from setup import body_surface, screen, screen_info
from constants import WHITE, BACKGROUND, ORANGE, G, scale_factors
from vectors import Vector
from bodies import all_sprites_list, bodies

# Initialise
pygame.init()

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

        #manager.process_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for body in bodies:
                click_pos = Vector(event.pos[0], event.pos[1]).convert_back()
                if (click_pos - body.position).magnitude() <= body.radius:
                    dragging = True
                    selected_body = body
                    selected = True

                    # Create GUI window elements
                    #details_window = pygame_gui.elements.UIWindow(
                        #rect=pygame.Rect((50,50),(100,100)),
                        #manager= manager,
                        #window_display_title="Test window"
                    #)

                    break

                selected = False

        if event.type == pygame.MOUSEMOTION:
            if dragging:
                selected_body.position = Vector(event.pos[0], event.pos[1]).convert_back()
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
                #check for collisions

                if separation <= body.radius + other.radius:
                    c = (2 * (body.mass * other.mass) / (body.mass + other.mass) * body_to_other.dot(
                    body.velocity - other.velocity)
                     / body_to_other.dot(body_to_other))

                    impulse = body_to_other * (-c / body.mass)

                    #body.velocity = body.velocity - (body_to_other * (c / body.mass))

                    #other.velocity = other.velocity + (body_to_other * (c / other.mass))
                    #move until separated
                    body.move(body_to_other * (-c / body.mass))
                    other.move(body_to_other * (c / other.mass))
                    while body.separation(other) <= body.radius + other.radius:
                        body.move(Vector(0, 0))
                        other.move(Vector(0, 0))

            # Find forces from other bodies and acceleration of this body

                net_acceleration += body_to_other * (G * other.mass / separation ** 3)

        deltav_list.append(net_acceleration)

    #move
    for z in zip(bodies, deltav_list):
        z[0].move(z[1])

    if drawing_elapsed >= 16:
        for body in bodies:
            # Draw tracers
            #pygame.draw.circle(trail_surface, body.colour, (body.last_displayed.convert().x,
            #                                                body.last_displayed.convert().y), 1)

            # Draw body sprites
            body.sprite.set_pos(body.position.convert())
            #body.last_displayed = body.position
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
                             (selected_body.position.convert().x + selected_body.velocity.x / scale_factors.velocity_scale_factor,
                              selected_body.position.convert().y + selected_body.velocity.y / scale_factors.velocity_scale_factor),
                             5)

        drawing_elapsed = 0
        screen.blit(body_surface, (0, 0))
        #manager.update(time_delta)
        #manager.draw_ui(ui_surface)
        pygame.display.flip()

