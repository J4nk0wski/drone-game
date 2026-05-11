import pygame

from src.shared import GameObject, ObjectType, Color
from src.drone import Drone
from src.game_logic import check_collision
from src.renderer import end_screen_text
from src.window import Window

def main():
    pygame.init()
    screen = Window((800, 600))
    pygame.display.set_caption("Drone Game")
    clock = pygame.time.Clock()
    running = True

    # 1. Tworzymy drona (wyżej, żeby miał z czego spadać)
    player_drone = Drone(x=370, y=50, width=60, height=40)
    # Wywołujemy funkcję do inicjalizacji grafiki
    #player_drone.create_image(None)
    # Włączamy grawitację (atrybut z drone.py)
    player_drone.gravity = 0.5

    # 2. Tworzymy podłogę bazując na klasie z shared.py
    floor = GameObject(x=0, y=550, width=800, height=50, object_type=ObjectType.FLOOR)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Logika i fizyka gry
        # Dron przyspiesza w dół przez grawitację
        player_drone.velocity.y += player_drone.gravity
        # Zmieniamy fizyczną pozycję drona
        player_drone.y += player_drone.velocity.y
        # Aktualizujemy pozycję hitboxa drona
        player_drone.rect.y = player_drone.y

        # Kolizje
        collision_info = check_collision(player_drone, floor)
        if collision_info.collision:
            # Jeśli uderzy w podłogę, zatrzymujemy prędkość spadania
            player_drone.velocity.y = 0
            # Ustawiamy go idealnie na powierzchni podłogi
            player_drone.y = floor.top - player_drone.height
            player_drone.rect.y = player_drone.y

        # Rysowanie na ekranie
        screen.screen.fill(Color.BLACK)

        # Rysujemy podłogę na szaro
        pygame.draw.rect(screen.screen, Color.GRAY, floor.rect)

        # Rysujemy drona
        if player_drone.img:
            screen.screen.blit(player_drone.img, player_drone.rect)
        else:
            pygame.draw.rect(screen.screen, Color.RED, player_drone.rect)
        end_screen_text(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()