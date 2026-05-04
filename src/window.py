import pygame
 
COLOR_BACKGROUND = (30, 30, 30)    # ciemnoszare tło
COLOR_DRONE      = (100, 180, 255) # niebieski dron
 
 
class Renderer:
 
    def __init__(self, screen):
        self.screen = screen
 
    def draw(self, drone_x, drone_y, drone_size=40):
        # 1. Tło
        self.screen.fill(COLOR_BACKGROUND)
 
        # 2. Dron jako kwadrat
        pygame.draw.rect(self.screen, COLOR_DRONE, (drone_x, drone_y, drone_size, drone_size))