import pygame
import pygame_gui

# Initialize Pygame
pygame.init()

# Set up the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Centered Window Example")

# Create a UI manager
ui_manager = pygame_gui.UIManager((screen_width, screen_height), "THEME.JSON")

# Create a custom window
window_width = 300
window_height = 200
window_x = (screen_width - window_width) // 2  # Center horizontally
window_y = screen_height - window_height  # Position at the bottom border
custom_window = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(window_x, window_y, window_width, window_height),
                                            manager=ui_manager,
                                            starting_height=1)

# Add some UI elements to the custom window
label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 10, 280, 30),
                                    text="This is a centered window",
                                    manager=ui_manager,
                                    container=custom_window)

# Create a toggle button
toggle_button_width = 100
toggle_button_height = 50
toggle_button_x = (screen_width - toggle_button_width) // 2  # Center horizontally
toggle_button_y = window_y - toggle_button_height  # Position above the window
toggle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(toggle_button_x, toggle_button_y, toggle_button_width, toggle_button_height),
                                             text="Toggle",
                                             manager=ui_manager)

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
        toggle_button_y = window_y - toggle_button_height  # Position above the window
    else:
        toggle_button_y = screen_height - toggle_button_height  # Position at the bottom of the screen
    toggle_button.set_relative_position((toggle_button_x, toggle_button_y))

    # Update the UI
    ui_manager.update(time_delta)

    # Clear the window
    screen.fill((255, 255, 255))

    # Draw the custom window if it's visible
    if window_visible:
        custom_window.show()
    else:
        custom_window.hide()

    ui_manager.draw_ui(screen)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()