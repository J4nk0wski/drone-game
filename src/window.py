import pygame
from shared import Vector2, GameObject, Color
from drone import Drone

class Window:
#ustawia domyslny rozmiar okna na 1280x720 i nazwe gry na GAME 
    def __init__(self, size=(1280,720), game_name="Game"):
        self.screen_size = size
        self.screen = pygame.display.set_mode(size)
        #ustawia domyślnie 60 fps
        self.clock = pygame.Clock()  
        self.fps = 60
        self.image_rects = []
        self.color = Color.WHITE
        self.rectangles = []
        self.background_image = None  # domyślnie brak tła
        #tworzy okno przy tworzeniu obiektu Window
        pygame.display.set_caption(game_name)
        pygame.font.init()
        self.font = pygame.font.SysFont('Consolas', 24, bold=True)
    def set_background_image(self, image_path):
        #Wczytuje zdjęcie ze ścieżki i skaluje je do rozmiaru okna
        image = pygame.image.load(image_path)
        self.background_image = pygame.transform.scale(image, self.screen_size)

    #zmiana koloru tla (domyslnie ustawiony na bialy)
    def change_background_color(self, new_color=Color.WHITE):
        self.color = new_color
    
    #odswiza ekran- metode nalezy wywolac po kazdym przejsciu w petli
    def update(self):
        pygame.display.update()

    #dodaje obiekt typu rect na ekran
    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)
    
    def add_image_rect(self, image_path: str, rectangle: pygame.Rect):
        """
        Wczytuje zdjęcie ze ścieżki, skaluje je do rozmiaru podanego Rect
        i dodaje do listy renderowanych obiektów.
        Rect nadal może być używany jako hitbox — jest przechowywany razem ze zdjęciem.

        Zwraca indeks dodanego elementu (przydatne do późniejszego usunięcia).
        """
        image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(image, (rectangle.width, rectangle.height))
        self.image_rects.append((scaled_image, rectangle))
        return len(self.image_rects) - 1

    #rysuje obiekty typu rect na ekrannie
    def draw_rect(self, rectangle):
        pygame.draw.rect(self.screen, (105, 194, 245), rectangle)

    """ Rysuje paski mocy silników po obu stronach ekranu"""
    def draw_engine_power(self, left_power: float, right_power: float):
        # Przycinaie wartości do zakresu [0, 1]
        left_power  = max(0.0, min(1.0, left_power))
        right_power = max(0.0, min(1.0, right_power))
        bar_width   = 20          # szerokość paska
        bar_margin  = 10          # odstęp od krawędzi ekranu
        bar_height  = 200         # maksymalna wysokość paska
        bar_bottom  = self.screen_size[1] // 2 + bar_height // 2  # wyśrodkowanie pionowe
        # Kolory
        color_background = (50,  50,  50)   # tło paska (ciemny)
        color_fill       = (0,  220,  80)   # wypełnienie (zielony)
        color_border     = (200, 200, 200)  # obwódka
        for power, side in ((right_power, "left"), (left_power, "right")): #TO NIE JEST POMYŁKA - pozostałość po starej implementacji, gdzie silniki były odwrotnie przypisane
            if side == "left":
                x = bar_margin
            else:
                x = self.screen_size[0] - bar_margin - bar_width
            # Tło paska
            bg_rect = pygame.Rect(x, bar_bottom - bar_height, bar_width, bar_height)
            pygame.draw.rect(self.screen, color_background, bg_rect, border_radius=4)
            # Wypełnienie proporcjonalne do mocy
            fill_h   = int(bar_height * power)
            fill_rect = pygame.Rect(x, bar_bottom - fill_h, bar_width, fill_h)
            pygame.draw.rect(self.screen, color_fill, fill_rect, border_radius=4)
            # Obwódka
            pygame.draw.rect(self.screen, color_border, bg_rect, width=2, border_radius=4)

    def draw_text(self, text: str, pos: tuple, font_size: int = 24, color: tuple = (0, 0, 0), font_path: str = None, centered: bool = False):
        font = pygame.font.Font(font_path, font_size)
        surface = font.render(text, True, color)
        
        if centered:
            rect = surface.get_rect(center=pos)
        else:
            rect = surface.get_rect(topleft=pos)
        
        self.screen.blit(surface, rect)


    def set_fps(self, fps: int):
        #Ustawia limit klatek na sekundę
        self.fps = fps

    def tick(self):
        #Wywołaj raz na końcu każdej iteracji pętli gry.
        self.clock.tick(self.fps)

    def get_fps(self):
        #Zwraca aktualne FPS
        return self.clock.get_fps()

    #zmienia kolor tla oraz dodaje obiekty rect na ekran
    #mozna zmienic w zaleznosci od potrzeb
    def render(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.color)

        for rectangle in self.rectangles:
            self.draw_rect(rectangle)
        for image, rect in self.image_rects:
            self.screen.blit(image, rect)

"""
Jak uzywac window.render() window.update() oraz window.tick() w petli gry:
    while running:
    # logika gry...
    window.render()
    window.update()
    window.tick() ← na samym końcu
"""
    

"""
KAAAMEEEERAAAA
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀   Klasa Camera odpowiada za dynamiczne śledzenie drona, obsługę efektu przybliżenia (zoom)
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⠛⠉⠙⠛⠛⠛⠛⠻⢿⣿⣷⣤⡀⠀⠀⠀⠀⠀  oraz ograniczanie ruchu pola widzenia do zadanego obszaru.
⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠋⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠈⢻⣿⣿⡄⠀⠀⠀⠀  
⠀⠀⠀⠀⠀⠀⠀⣸⣿⡏⠀⠀⠀⣠⣶⣾⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣄⠀⠀⠀  Atrybuty:
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⢰⣿⣿⣯⠁⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣷⡄⠀    - offset (Vector2): Aktualne przesunięcie kamery w świecie gry.
⠀⠀⣀⣤⣴⣶⣶⣿⡟⠀⠀⠀⢸⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⡀   - width (int): Szerokość okna, height (int): Wysokość okna
⠀⢰⣿⡟⠋⠉⣹⣿⡇⠀⠀⠀⠘⣿⣿⣿⣿⣷⣦⣤⣤⣤⣶⣶⣶⣶⣿⣿⣿⠀ - look_ahead (float): Współczynnik wyprzedzania ruchu drona
⠀⢸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀  -damping (float): Współczynnik płynności ruchu (0.1 = wolna, 1.0 = natychmiastowa)
⠀⣸⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠉⠻⠿⣿⣿⣿⣿⡿⠿⠿⠛⢻⣿⡇⠀⠀  - zoom_level (float): Aktualna skala przybliżenia obrazu.
⠀⣿⣿⠁⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⠀⠀    - min_x, max_x, min_y, max_y (float): Granice świata, poza które kamera nie wyjdzie.
⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀    Metody:
⠀⣿⣿⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⠀    - set_limits: Definiuje prostokątny obszar ograniczający ruch kamery.
⠀⢿⣿⡆⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀    -update odświeża kamere i wylicza nowe przesunięcie na podstawie pozycji i prędkości drona
⠀⠸⣿⣧⡀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠃⠀⠀    - apply: Przekształca współrzędne obiektu gry na współrzędne ekranu, uwzględniając przesunięcie i zoom.
⠀⠀⠛⢿⣿⣿⣿⣿⣇⠀⠀ ⠀⣰⣿⣿⣷⣶⣶⣶⣶⠶⠀⢠⣿⣿⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⣽⣿⡏⠁⠀⠀⢸⣿⡇⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⣿⣿⡇⠀⢹⣿⡆⠀⠀⠀⣸⣿⠇⠀⠀⠀ Jeżeli ktoś ma pomysł na jakieś zmiany i poprawki to śmiało
⠀⠀⠀⠀⠀⠀⠀⢿⣿⣦⣄⣀⣠⣴⣿⣿⠁⠀⠈⠻⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠿⠿⠿⠿⠋⠁⠀⠀⠀
 """
class Camera:
    def __init__(self, screen_width: int, screen_height: int, look_ahead: float = 15.0, damping: float = 0.08):
        self.offset = Vector2(0, 0)
        self.width = screen_width
        self.height = screen_height
        self.look_ahead = look_ahead
        self.damping = damping
        self.zoom_level = 1.0  # 1.0 to brak przybliżenia
        #Limity ruchu kamery (None oznacza brak limitu w danym kierunku)
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
    
    def set_limits(self, min_x=None, max_x=None, min_y=None, max_y=None):
        """Ustawia granice, których kamera nie może przekroczyć"""
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def update(self, player: 'Drone'):
        # Obliczanie celu (Target) z wyprzedzeniem
        target_x = player.center.x + (player.velocity.x * self.look_ahead)
        target_y = player.center.y + (player.velocity.y * self.look_ahead)

        # Centrowanie
        target_offset_x = target_x - self.width / 2
        target_offset_y = target_y - self.height / 2

        # Damping
        self.offset.x += (target_offset_x - self.offset.x) * self.damping
        self.offset.y += (target_offset_y - self.offset.y) * self.damping

        # Blokowanie kamery wewnątrz limitów
        if self.min_x is not None: self.offset.x = max(self.min_x, self.offset.x)
        if self.max_x is not None: self.offset.x = min(self.max_x - self.width, self.offset.x)
        if self.min_y is not None: self.offset.y = max(self.min_y, self.offset.y)
        if self.max_y is not None: self.offset.y = min(self.max_y - self.height, self.offset.y)

    def apply(self, game_object: GameObject) -> pygame.Rect:
        # 1. Obliczamy pozycję względem kamery w świecie (offset)
        rel_x = game_object.pos.x - self.offset.x
        rel_y = game_object.pos.y - self.offset.y
        
        # 2. Przesuwamy punkt odniesienia do środka ekranu, skalujemy i wracamy
        # To sprawia, że zoom "celuje" w środek okna
        center_x, center_y = self.width / 2, self.height / 2
        
        final_x = (rel_x - center_x) * self.zoom_level + center_x
        final_y = (rel_y - center_y) * self.zoom_level + center_y
        
        # 3. Skalujemy również wymiary obiektu
        final_w = game_object.width * self.zoom_level
        final_h = game_object.height * self.zoom_level
        
        return pygame.Rect(final_x, final_y, final_w, final_h)

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