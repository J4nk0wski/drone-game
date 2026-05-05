import pygame
#nalezy dodac komentarze
class Window:

#ustawia domyslny rozmiar okna na 1280x720 i nazwe gry na GAME 
    def __init__(self, size=(1280,720), game_name="Game"):
        self.screen = pygame.display.set_mode(size)
        self.color = (255, 255, 255)
        self.rectangles = []
#inicjalizyje okno przy tworzeniu obiektu Window
        pygame.display.set_caption(game_name)
    
    def change_background_color(self, new_color=(255, 255, 255)):
        self.color = new_color
    
    def update(self):
        pygame.display.update()

    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)
    
    def draw_rect(self, rectangle):
        pygame.draw.rect(self.screen, (255, 0, 0), rectangle)

    def render(self):
        self.screen.fill(self.color)
        for rectangle in self.rectangles:
            self.draw_rect(rectangle)

        self.update()

        
    