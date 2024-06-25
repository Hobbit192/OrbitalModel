import pygame
import pygame_gui
from pygame_gui.core import ObjectID, UIElement
from pygame_gui.core.interfaces import IUIManagerInterface
from setup import screen_info


class UIShape(UIElement):
    def __init__(self, relative_rect: pygame.Rect, shape: str, colour: tuple, manager: IUIManagerInterface,
                 container=None, starting_height=1, layer_thickness=1):
        super().__init__(relative_rect, manager, container, starting_height=starting_height, layer_thickness=layer_thickness)
        self.shape = shape
        self.colour = colour
        self.image = pygame.Surface(relative_rect.size, pygame.SRCALPHA)
        self.draw()
        self.element_ids = ["shape_element"]

    def draw(self):
        if self.shape == "circle":
            pygame.draw.circle(self.image, self.colour, (self.rect.width // 2, self.rect.height // 2),
                               (min(self.rect.width, self.rect.height) // 2))

        elif self.shape == "rectangle":
            pygame.draw.rect(self.image, self.colour, self.image.get_rect())

        elif self.shape == "triangle":
            points = [
                (self.rect.width // 2, 0),
                (self.rect.width, self.rect.height),
                (0, self.rect.height)
            ]
            pygame.draw.polygon(self.image, self.colour, points)

    def update(self, time_delta):
        pass

    def update_colour(self, colour: tuple):
        self.colour = colour
        self.redraw()

    def redraw(self):
        self.image.fill((0, 0, 0, 0))  # Clear the surface
        self.draw()


# Initialize Pygame
pygame.init()

# Create a UI manager
ui_manager = pygame_gui.UIManager((screen_info.width, screen_info.height), "THEME.JSON")

# ---------------------------------------- INFO PANEL ------------------------------------------------------------------
info_panel_width = 365
info_panel_height = 700
info_panel_x = screen_info.width - info_panel_width
info_panel_y = (screen_info.height - info_panel_height) // 2
info_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(info_panel_x, info_panel_y, info_panel_width, info_panel_height),
                                         manager=ui_manager,
                                         starting_height=1,
                                         object_id=ObjectID(class_id="@panels"),
                                         visible=0
                                         )

# Elements on the Info Panel
info_title_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((12, 10), (140, 16)),
                                               text="// INFORMATION PANEL",
                                               manager=ui_manager,
                                               container=info_panel,
                                               object_id=ObjectID(class_id="@title_labels")
                                               )
info_toggle_button_x = screen_info.width - 29
info_toggle_button_y = (screen_info.height - 100) // 2
info_toggle_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((info_toggle_button_x, info_toggle_button_y),
                                                                            (29, 100)),
                                                  text="",
                                                  manager=ui_manager,
                                                  object_id=ObjectID(class_id="@left_toggle_button")
                                                  )

info_toggle_button.disable()

name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((47, 47), (266, 79)),
                                         text="JUPITER",
                                         manager=ui_manager,
                                         container=info_panel,
                                         object_id=ObjectID(object_id="#name_label")
                                         )

planet_label = UIShape(relative_rect=pygame.Rect((11, 119), (173, 173)),
                       shape="circle",
                       colour=(81, 136, 130),
                       manager=ui_manager,
                       container=info_panel
                       )

mass_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((185, 149), (45, 18)),
                                         text="Mass:",
                                         manager=ui_manager,
                                         container=info_panel,
                                         object_id=ObjectID(class_id="@info_labels")
                                         )

mass_entry_text = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((252, 149), (42, 18)),
                                                      manager=ui_manager,
                                                      container=info_panel,
                                                      object_id=ObjectID(class_id="@info_text_entry"),
                                                      initial_text="0.01"
                                                      )

mass_entry_text.set_text_length_limit(4)
mass_entry_text.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])

e_label_1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((298, 149), (9, 18)),
                                        text="E",
                                        manager=ui_manager,
                                        container=info_panel,
                                        object_id=ObjectID(class_id="@info_labels")
                                        )

power_entry_text_1 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((313, 149), (24, 18)),
                                                         manager=ui_manager,
                                                         container=info_panel,
                                                         object_id=ObjectID(class_id="@info_text_entry"),
                                                         initial_text="1"
                                                         )
power_entry_text_1.set_text_length_limit(2)
power_entry_text_1.set_allowed_characters("numbers")

mass_unit_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((335, 149), (24, 18)),
                                              text="kg",
                                              manager=ui_manager,
                                              container=info_panel,
                                              object_id=ObjectID(class_id="@info_labels")
                                              )

mass_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((195, 171), (140, 20)),
                                                     start_value=0.01,
                                                     value_range=(0.01, 9.99),
                                                     manager=ui_manager,
                                                     container=info_panel,
                                                     object_id=ObjectID(class_id="@info_sliders"),
                                                     click_increment=0.01
                                                     )

radius_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((185, 222), (63, 18)),
                                           text="Radius:",
                                           manager=ui_manager,
                                           container=info_panel,
                                           object_id=ObjectID(class_id="@info_labels")
                                           )

radius_entry_text = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((252, 222), (42, 18)),
                                                        manager=ui_manager,
                                                        container=info_panel,
                                                        object_id=ObjectID(class_id="@info_text_entry"),
                                                        initial_text="0.01"
                                                        )

radius_entry_text.set_text_length_limit(4)
radius_entry_text.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])

e_label_2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((298, 222), (9, 18)),
                                        text="E",
                                        manager=ui_manager,
                                        container=info_panel,
                                        object_id=ObjectID(class_id="@info_labels")
                                        )

power_entry_text_2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((311, 222), (24, 18)),
                                                         manager=ui_manager,
                                                         container=info_panel,
                                                         object_id=ObjectID(class_id="@info_text_entry"),
                                                         initial_text="1"
                                                         )
power_entry_text_2.set_text_length_limit(2)
power_entry_text_2.set_allowed_characters("numbers")

radius_unit_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((335, 222), (15, 18)),
                                                text="m",
                                                manager=ui_manager,
                                                container=info_panel,
                                                object_id=ObjectID(class_id="@info_labels")
                                                )

radius_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((195, 244), (140, 20)),
                                                       start_value=0.01,
                                                       value_range=(0.01, 9.99),
                                                       manager=ui_manager,
                                                       container=info_panel,
                                                       object_id=ObjectID(class_id="@info_sliders"),
                                                       click_increment=0.01
                                                       )

red_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((12, 319), (36, 18)),
                                        text="Red:",
                                        manager=ui_manager,
                                        container=info_panel,
                                        object_id=ObjectID(class_id="@info_labels")
                                        )

red_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((78, 316), (140, 20)),
                                                    start_value=0,
                                                    value_range=(0, 255),
                                                    manager=ui_manager,
                                                    container=info_panel,
                                                    object_id=ObjectID(class_id="@info_sliders"),
                                                    click_increment=1
                                                    )

red_entry_text = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((246, 317), (33, 18)),
                                                     manager=ui_manager,
                                                     container=info_panel,
                                                     object_id=ObjectID(class_id="@info_text_entry"),
                                                     initial_text="0"
                                                     )

red_entry_text.set_text_length_limit(3)
red_entry_text.set_allowed_characters("numbers")

green_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((12, 347), (54, 18)),
                                          text="Green:",
                                          manager=ui_manager,
                                          container=info_panel,
                                          object_id=ObjectID(class_id="@info_labels")
                                          )

green_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((78, 344), (140, 20)),
                                                      start_value=0,
                                                      value_range=(0, 255),
                                                      manager=ui_manager,
                                                      container=info_panel,
                                                      object_id=ObjectID(class_id="@info_sliders"),
                                                      click_increment=1
                                                      )

green_entry_text = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((246, 345), (33, 18)),
                                                       manager=ui_manager,
                                                       container=info_panel,
                                                       object_id=ObjectID(class_id="@info_text_entry"),
                                                       initial_text="0"
                                                       )

green_entry_text.set_text_length_limit(3)
green_entry_text.set_allowed_characters("numbers")

blue_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((12, 375), (45, 18)),
                                         text="Blue:",
                                         manager=ui_manager,
                                         container=info_panel,
                                         object_id=ObjectID(class_id="@info_labels")
                                         )

blue_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((78, 373), (140, 20)),
                                                     start_value=0,
                                                     value_range=(0, 255),
                                                     manager=ui_manager,
                                                     container=info_panel,
                                                     object_id=ObjectID(class_id="@info_sliders"),
                                                     click_increment=1
                                                     )

blue_entry_text = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((246, 374), (33, 18)),
                                                      manager=ui_manager,
                                                      container=info_panel,
                                                      object_id=ObjectID(class_id="@info_text_entry"),
                                                      initial_text="0"
                                                      )

blue_entry_text.set_text_length_limit(3)
blue_entry_text.set_allowed_characters("numbers")

velocity_x_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((37, 414), (216, 18)),
                                               text="Horizontal velocity (x):",
                                               manager=ui_manager,
                                               container=info_panel,
                                               object_id=ObjectID(class_id="@info_labels")
                                               )

velocity_y_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((55, 440), (198, 18)),
                                               text="Vertical velocity (y):",
                                               manager=ui_manager,
                                               container=info_panel,
                                               object_id=ObjectID(class_id="@info_labels")
                                               )

speed_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150, 466), (54, 18)),
                                          text="Speed:",
                                          manager=ui_manager,
                                          container=info_panel,
                                          object_id=ObjectID(class_id="@info_labels")
                                          )

speed_value_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((200, 466), (120, 18)),
                                                text=" m/s",
                                                manager=ui_manager,
                                                container=info_panel,
                                                object_id=ObjectID(class_id="@info_labels")
                                                )

emphasis_rect_1 = UIShape(relative_rect=pygame.Rect((6, 408), (5, 80)),
                          shape="rectangle",
                          colour=(77, 81, 81),
                          manager=ui_manager,
                          container=info_panel
                          )

emphasis_rect_2 = UIShape(relative_rect=pygame.Rect((16, 408), (5, 80)),
                          shape="rectangle",
                          colour=(77, 81, 81),
                          manager=ui_manager,
                          container=info_panel
                          )

emphasis_rect_3 = UIShape(relative_rect=pygame.Rect((26, 408), (5, 80)),
                          shape="rectangle",
                          colour=(77, 81, 81),
                          manager=ui_manager,
                          container=info_panel
                          )

emphasis_rect_4 = UIShape(relative_rect=pygame.Rect((31, 408), (301, 4)),
                          shape="rectangle",
                          colour=(77, 81, 81),
                          manager=ui_manager,
                          container=info_panel
                          )

emphasis_rect_5 = UIShape(relative_rect=pygame.Rect((31, 484), (301, 4)),
                          shape="rectangle",
                          colour=(77, 81, 81),
                          manager=ui_manager,
                          container=info_panel
                          )

emphasis_rect_6 = UIShape(relative_rect=pygame.Rect((328, 412), (4, 72)),
                          shape="rectangle",
                          colour=(77, 81, 81),
                          manager=ui_manager,
                          container=info_panel
                          )

trajectories_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((12, 514), (162, 18)),
                                                 text="Show trajectories:",
                                                 manager=ui_manager,
                                                 container=info_panel,
                                                 object_id=ObjectID(class_id="@info_labels")
                                                 )

# ----------------------------------------- NEW BODY PANEL -------------------------------------------------------------

new_body_panel_width = 110
new_body_panel_height = 110
new_body_panel_x = 0
new_body_panel_y = screen_info.height - new_body_panel_height
new_body_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((new_body_panel_x, new_body_panel_y),
                                                                       (new_body_panel_width, new_body_panel_height)),
                                             manager=ui_manager,
                                             starting_height=1,
                                             object_id=ObjectID(class_id="@panels"),
                                             visible=1
                                             )

# Elements on the New Body Panel

new_body_title_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((6, 4), (80, 16)),
                                                   text="// NEW BODY",
                                                   manager=ui_manager,
                                                   container=new_body_panel,
                                                   object_id=ObjectID(class_id="@title_labels")
                                                   )

new_body_label = UIShape(relative_rect=pygame.Rect((16, 24), (74, 74)),
                         shape="circle",
                         colour=(81, 136, 130),
                         manager=ui_manager,
                         container=new_body_panel
                         )

# Main event loop
"""
        # Toggle the window visibility on button click
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == toggle_button:
                window_visible = not window_visible

    # Update the toggle button position
    if window_visible:
        toggle_button_y = info_panel_y - toggle_button_height  # Position above the window
    else:
        toggle_button_y = screen_info.height - toggle_button_height  # Position at the bottom of the screen
    toggle_button.set_relative_position((toggle_button_x, toggle_button_y))


    # Draw the custom window if it's visible
    if window_visible:
        info_panel.show()
    else:
        info_panel.hide()
"""
