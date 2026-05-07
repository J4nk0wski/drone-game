import pygame
# Tu importy
from src.window import Window
def main():
    pygame.init()
    game_window = Window(size=(1280, 720), game_name="Drone Game")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game_window.render()
    pygame.quit()

if __name__ == "__main__":
    main()