import os
import pygame

from constants import BACKGROUND

pygame.init()


class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.centre_x = self.width / 2
        self.centre_y = self.height / 2


os.environ["SDL_VIDEO_WINDOW_POS"] = "0,30"
info = pygame.display.Info()

screen_info = Screen(width=info.current_w, height=info.current_h - 80)

window_size = (screen_info.width, screen_info.height)
screen = pygame.display.set_mode(window_size)

velocity_surface = pygame.Surface(window_size, pygame.SRCALPHA)
velocity_surface.fill((255, 255, 255, 0))
thrust_surface = pygame.Surface(window_size, pygame.SRCALPHA)
thrust_surface.fill((255, 255, 255, 0))

body_surface = pygame.Surface(window_size)
ui_surface = pygame.Surface(window_size)
ui_surface.set_colorkey(BACKGROUND)
menu_surface = pygame.Surface(window_size)
menu_surface.fill(BACKGROUND)
controls_surface = pygame.Surface(window_size)
controls_surface.fill(BACKGROUND)

icon = pygame.image.load("black-hole-256x256.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Orbital Simulator", "OrbitSim")

