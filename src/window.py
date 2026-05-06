import pygame


class Window:
#ustawia domyslny rozmiar okna na 1280x720 i nazwe gry na GAME 
    def __init__(self, size=(1280,720), game_name="Game"):
        self.screen_size = size
        self.screen = pygame.display.set_mode(size)
        self.color = (255, 255, 255)
        self.rectangles = []
        self.background_image = None  # domyślnie brak tła
        #tworzy okno przy tworzeniu obiektu Window
        pygame.display.set_caption(game_name)
    
    def set_background_image(self, image_path):
        #Wczytuje zdjęcie ze ścieżki i skaluje je do rozmiaru okna
        image = pygame.image.load(image_path)
        self.background_image = pygame.transform.scale(image, self.screen_size)

    def change_background_color(self, new_color=(255, 255, 255)):
        self.color = new_color
    
    def update(self):
        pygame.display.update()

    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)
    
    def draw_rect(self, rectangle):
        pygame.draw.rect(self.screen, (105, 194, 245), rectangle)

    def render(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.color)

        for rectangle in self.rectangles:
            self.draw_rect(rectangle)

        self.update()
    
    