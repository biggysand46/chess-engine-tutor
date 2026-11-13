import pygame, sqlite3, json, random
pygame.init()

# Defining the resolution of the window
resolution = window_width, window_height = 800, 600
window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

pygame.display.set_caption("Chess Tutor")