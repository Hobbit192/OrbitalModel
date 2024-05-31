import pygame
import pygame_gui


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)
details_window = pygame_gui.elements.UIWindow(
                        rect=pygame.Rect((50,50),(100,100)),
                        manager= manager,
                        window_display_title="Test window"
                    )

window_test = pygame_gui.windows.ui_colour_picker_dialog.UIColourPickerDialog(rect=((100, 100), (400, 400)), manager=manager)
clock = pygame.time.Clock()
is_running = True

while is_running:

    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World!')

        manager.process_events(event)

    window_surface.blit(background, (0, 0))

    manager.update(time_delta)
    manager.draw_ui(window_surface)

    pygame.display.update()
