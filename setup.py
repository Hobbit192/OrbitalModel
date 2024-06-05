import os
import pygame

pygame.init()

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,30"
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

icon = pygame.image.load("black-hole-256x256.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Orbital Simulator", "OrbitSim")
