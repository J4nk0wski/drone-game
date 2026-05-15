import pygame

from src.window import Window
from src.shared import Color

"""
wypisuje na środku ekranu napis "Game Over"
"""
def end_screen_text(screen: Window) -> None:
    font = pygame.font.SysFont("monospace", 50)
    text = font.render("Game Over", True, Color.WHITE)
    text_rect = text.get_rect()
    text_rect.center = screen.screen_size[0] / 2, (screen.screen_size[1] / 2) - 50

    font_button = pygame.font.SysFont("monospace", 30)
    #named_button_rect = font_button.render().get_rect()
    named_button = font_button.render("Play again?", True, Color.WHITE, Color.GREEN)

    named_button_rect = named_button.get_rect()
    named_button_rect.center = screen.screen_size[0] / 2, (screen.screen_size[1] / 2) + 20

    m_pos = pygame.mouse.get_pos()
    if named_button_rect.collidepoint(m_pos):
        named_button.set_colorkey(color=Color.GREEN)
    else:
        named_button.set_colorkey(Color.WHITE)


    screen.screen.blit(text, text_rect)
    screen.screen.blit(named_button, named_button_rect)


def show_game_over_screen(screen: pygame.Surface, player_drone) -> None:
    """
    Wyświetla ekran końca gry z wycentrowanym napisem i interaktywnym przyciskiem.
    Zmienia stan player_drone.destroyed na False po kliknięciu 'Play again?'.
    """
    # 1. Przygotowanie czcionek
    # Jeśli nie masz własnych czcionek .ttf, SysFont użyje systemowych
    font_title = pygame.font.SysFont("Arial", 64, bold=True)
    font_button = pygame.font.SysFont("Arial", 32)

    # 2. Tworzenie napisu "Game Over" i centrowanie go
    title_surface = font_title.render("Game Over", True, Color.WHITE)
    title_rect = title_surface.get_rect()
    # Ustawiamy środek napisu dokładnie na środku ekranu, ale lekko przesunięty w górę (-50)
    title_rect.center = (screen.get_width() // 2, (screen.get_height() // 2) - 50)

    # 3. Przygotowanie przycisku "Play again?"
    button_text_surface = font_button.render("Play again?", True, Color.WHITE)
    button_text_rect = button_text_surface.get_rect()

    # Ustawiamy środek tekstu przycisku poniżej napisu "Game Over" (+50)
    button_text_rect.center = (screen.get_width() // 2, (screen.get_height() // 2) + 50)

    # Tworzymy fizyczny prostokąt (tło przycisku) z lekkim marginesem (paddingiem) wokół tekstu
    button_rect = pygame.Rect(
        button_text_rect.left - 20,
        button_text_rect.top - 10,
        button_text_rect.width + 40,
        button_text_rect.height + 20
    )

    # 4. Obsługa interakcji myszy (Hover effect)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    # Domyślny kolor przycisku to czerwony
    button_color = Color.RED

    # Sprawdzamy, czy kursor myszy znajduje się wewnątrz prostokąta przycisku
    if button_rect.collidepoint(mouse_pos):
        button_color = Color.GREEN  # Zmiana koloru na zielony po najechaniu

        # Jeśli kursor najechał I gracz kliknął lewy przycisk myszy (indeks 0)
        if mouse_pressed[0]:
            player_drone.destroyed = False
            # Tutaj możesz też zresetować inne parametry drona, np.:
            # player_drone.health = player_drone.HEALTH
            # player_drone.lives = player_drone.LIVES
            # player_drone.x, player_drone.y = 370, 50
            # player_drone.velocity.y = 0

    # 5. Rysowanie elementów na ekranie
    # Przyciemniamy lekko tło gry pod spodem (opcjonalne, ale daje ładny efekt)
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Czarny z przezroczystością Alpha
    screen.blit(overlay, (0, 0))

    # Rysujemy napis główny
    screen.blit(title_surface, title_rect)

    # Rysujemy tło przycisku (zaokrąglone rogi = border_radius=5)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=5)

    # Rysujemy tekst na przycisku
    screen.blit(button_text_surface, button_text_rect)