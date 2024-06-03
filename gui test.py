import pygame
import pygame_gui
import os

from pygame_gui.core import ObjectID

BACKGROUND = (10, 5, 38)

# Initialize Pygame
pygame.init()

# Set up the window
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,30'
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h - 80
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Centered Window Example")

# Create a UI manager
ui_manager = pygame_gui.UIManager((screen_width, screen_height), "THEME.JSON")

# Info panel
info_panel_width = 350
info_panel_height = 700
info_panel_x = screen_width - info_panel_width
info_panel_y = (screen_height - info_panel_height) // 2
info_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(info_panel_x, info_panel_y, info_panel_width, info_panel_height),
                                         manager=ui_manager,
                                         starting_height=1,
                                         object_id=ObjectID(object_id="#info_panel")
                                         )

# Elements on the Info Panel
info_title_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((11, 10), (140, 16)),
                                               text="// INFORMATION PANEL",
                                               manager=ui_manager,
                                               container=info_panel,
                                               object_id=ObjectID(object_id="#info_title_label")
                                               )

name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((44, 47), (266, 79)),
                                         text="JUPITER",
                                         manager=ui_manager,
                                         container=info_panel,
                                         object_id=ObjectID(object_id="#name_label")
                                         )

mass_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((184, 150), (41, 17)),
                                         text="Mass:",
                                         manager=ui_manager,
                                         container=info_panel,
                                         object_id=ObjectID(class_id="@info_labels")
                                         )

radius_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((184, 223), (57, 17)),
                                           text="Radius:",
                                           manager=ui_manager,
                                           container=info_panel,
                                           object_id=ObjectID(class_id="@info_labels")
                                           )

red_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((11, 320), (32, 17)),
                                        text="Red:",
                                        manager=ui_manager,
                                        container=info_panel,
                                        object_id=ObjectID(class_id="@info_labels")
                                        )

green_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((11, 348), (48, 17)),
                                          text="Green:",
                                          manager=ui_manager,
                                          container=info_panel,
                                          object_id=ObjectID(class_id="@info_labels")
                                          )


blue_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((11, 376), (41, 17)),
                                         text="Blue:",
                                         manager=ui_manager,
                                         container=info_panel,
                                         object_id=ObjectID(class_id="@info_labels")
                                         )


# Create a toggle button
toggle_button_width = 100
toggle_button_height = 50
toggle_button_x = (screen_width - toggle_button_width) // 2  # Center horizontally
toggle_button_y = info_panel_y - toggle_button_height  # Position above the window
toggle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(toggle_button_x, toggle_button_y, toggle_button_width, toggle_button_height),
                                             text="Toggle",
                                             manager=ui_manager)

test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 0, 100, 50),
                                             text="Toggle",
                                             manager=ui_manager, object_id="#button_test")

# Window visibility flag
window_visible = True

# Main event loop
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle UI events
        ui_manager.process_events(event)

        # Toggle the window visibility on button click
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == toggle_button:
                window_visible = not window_visible

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_button.disable()

            if event.key == pygame.K_1:
                toggle_button.enable()

    # Update the toggle button position
    if window_visible:
        toggle_button_y = info_panel_y - toggle_button_height  # Position above the window
    else:
        toggle_button_y = screen_height - toggle_button_height  # Position at the bottom of the screen
    toggle_button.set_relative_position((toggle_button_x, toggle_button_y))

    # Update the UI
    ui_manager.update(time_delta)

    # Clear the window
    screen.fill(BACKGROUND)

    # Draw the custom window if it's visible
    if window_visible:
        info_panel.show()
    else:
        info_panel.hide()

    ui_manager.draw_ui(screen)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()