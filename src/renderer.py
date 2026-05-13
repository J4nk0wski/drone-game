import pygame

from src.window import Window

"""
wypisuje na środku ekranu napis "Game Over"
"""
def end_screen_text(screen: Window) -> None:
    font = pygame.font.SysFont("monospace", 50)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = screen.screen_size[0] / 2, screen.screen_size[1] / 2
    screen.screen.blit(text, text_rect)