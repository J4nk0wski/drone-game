import pygame

from src.shared import GameObject, ObjectType, Color
from src.drone import Drone
from src.game_logic import check_collision
# POPRAWKA: Importujemy show_game_over_screen prosto z window
from src.window import Window, show_game_over_screen


def main():
    pygame.init()

    #Używamy konstrukcji Window z game_name
    screen = Window(size=(800, 600), game_name="Drone Game")
    clock = pygame.time.Clock()
    running = True

    #Tworzymy drona (wyżej, żeby miał z czego spadać)
    player_drone = Drone(x=370, y=50, width=60, height=40)
    # Włączamy grawitację
    player_drone.gravity = 0.5

    #Tworzymy podłogę bazując na klasie z shared.py
    floor = GameObject(x=0, y=550, width=800, height=50, object_type=ObjectType.FLOOR)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Logika i fizyka gry
        # Dron przyspiesza w dół przez grawitację
        player_drone.velocity.y += player_drone.gravity

        # Używamy pos.y, bo przeszliśmy na wektory (Vector2)
        player_drone.pos.y += player_drone.velocity.y
        # Aktualizujemy pozycję hitboxa drona
        player_drone.rect.y = int(player_drone.pos.y)

        # Kolizje
        collision_info = check_collision(player_drone, floor)
        if collision_info.collision:
            # Jeśli uderzy w podłogę, zatrzymujemy prędkość spadania
            if player_drone.velocity.y < 2:
                player_drone.velocity.y = 0
            player_drone.velocity.y = -player_drone.velocity.y * 0.6
            # Ustawiamy go idealnie na powierzchni podłogi
            player_drone.pos.y = floor.rect.top - player_drone.height
            player_drone.rect.y = int(player_drone.pos.y)

        # Rysowanie na ekranie
        screen.screen.fill(Color.BLACK)

        # Rysujemy podłogę na szaro
        pygame.draw.rect(screen.screen, Color.GRAY, floor.rect)

        # Rysujemy drona
        if player_drone.img:
            screen.screen.blit(player_drone.img, player_drone.rect)
        else:
            pygame.draw.rect(screen.screen, Color.RED, player_drone.rect)

        show_game_over_screen(screen, player_drone)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()