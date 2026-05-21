import pygame

from src.window import Window
from src.shared import Color
from src.drone import Drone
"""
Wyświetla ekran końca gry z wycentrowanym napisem i interaktywnym przyciskiem
Zmienia stan player_drone.destroyed na False po kliknięciu 'Play again?'
Po wybraniu opcji ponownej gry parametry określające pozycję drona to:
start_x (domyślnie 0)
start_y (domyślnie 0)
"""
def show_game_over_screen(screen: Window, player_drone: Drone, start_x: float=0, start_y: float=0) -> None:
    #czcionki napisów
    font_title = pygame.font.SysFont("Arial", 64, bold=True)
    font_button = pygame.font.SysFont("Arial", 32)

    #napis Game Over
    title_surface = font_title.render("Game Over", True, Color.WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (screen.screen_size[0] // 2, (screen.screen_size[1] // 2) - 50)

    #przycisk
    button_text_surface = font_button.render("Play again?", True, Color.WHITE)
    button_text_rect = button_text_surface.get_rect()
    button_text_rect.center = (screen.screen_size[0] // 2, (screen.screen_size[1] // 2) + 50)
    button_rect = pygame.Rect(
        button_text_rect.left - 20,
        button_text_rect.top - 10,
        button_text_rect.width + 40,
        button_text_rect.height + 20
    )

    #myszka
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    #przycisk kolor początkowy
    button_color = Color.RED

    #kolizja z myszką
    if button_rect.collidepoint(mouse_pos):
        button_color = Color.GREEN  #zmiana na zielony

        #kliknięcie przycisku
        if mouse_pressed[0]:
            player_drone.destroyed = False
            player_drone.reset(start_x, start_y)

    #rysowanie
    #lekkie przyciemnienie tła
    overlay = pygame.Surface((screen.screen_size[0], screen.screen_size[1]), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.screen.blit(overlay, (0, 0))

    screen.screen.blit(title_surface, title_rect)

    pygame.draw.rect(screen.screen, button_color, button_rect, border_radius=5)

    screen.screen.blit(button_text_surface, button_text_rect)