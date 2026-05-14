import pygame

class Window:
#ustawia domyslny rozmiar okna na 1280x720 i nazwe gry na GAME 
    def __init__(self, size=(1280,720), game_name="Game"):
        self.screen_size = size
        self.screen = pygame.display.set_mode(size)
        #ustawia domyślnie 60 fps
        self.clock = pygame.Clock()  
        self.fps = 60
        self.image_rects = []
        self.color = (255, 255, 255)
        self.rectangles = []
        self.background_image = None  # domyślnie brak tła
        #tworzy okno przy tworzeniu obiektu Window
        pygame.display.set_caption(game_name)
    def set_background_image(self, image_path):
        #Wczytuje zdjęcie ze ścieżki i skaluje je do rozmiaru okna
        image = pygame.image.load(image_path)
        self.background_image = pygame.transform.scale(image, self.screen_size)

    #zmiana koloru tla (domyslnie ustawiony na bialy)
    def change_background_color(self, new_color=(255, 255, 255)):
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
        for power, side in ((left_power, "left"), (right_power, "right")):
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
    