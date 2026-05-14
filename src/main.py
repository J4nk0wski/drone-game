import pygame
from drone import Drone
from shared import GameObject, ObjectType, CollisionSide
from game_logic import check_collision
from window import Window, Camera


def main():
    pygame.init()

    # Tworzenie okna
    game_window = Window(size=(800, 600), game_name="Drone Game")
    game_window.change_background_color((0, 0, 0))

    # Używamy argumentów pozycyjnych dla kamery (rozwiązuje błąd TypeError)
    camera = Camera(800, 600, 15.0, 0.08)

    clock = pygame.time.Clock()
    running = True

    # Inicjalizacja drona
    player_drone = Drone(x=370, y=50, width=60, height=40)
    player_drone.gravity = 0.5

    # Inicjalizacja podłogi
    floor = GameObject(x=0, y=550, width=800, height=50, object_type=ObjectType.FLOOR)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        left_power = 0.0
        right_power = 0.0

        # --- Sterowanie ---
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player_drone.velocity.y -= 1.0
            left_power, right_power = 0.8, 0.8

        if keys[pygame.K_LEFT]:
            player_drone.velocity.x = -5
            left_power, right_power = 0.2, 1.0
        elif keys[pygame.K_RIGHT]:
            player_drone.velocity.x = 5
            left_power, right_power = 1.0, 0.2
        else:
            player_drone.velocity.x = 0

        # --- Fizyka ---
        player_drone.velocity.y += player_drone.gravity
        player_drone.y += player_drone.velocity.y
        player_drone.x += player_drone.velocity.x

        # Synchronizacja rectów przed kolizją
        player_drone.rect.y = player_drone.y
        player_drone.rect.x = player_drone.x

        # Aktualizacja kamery
        camera.update(player_drone)

        # --- Kolizje ---
        collision_info = check_collision(player_drone, floor)
        if collision_info and collision_info.collision:
            side = collision_info.side

            if side == CollisionSide.TOP:
                player_drone.velocity.y = 0
                player_drone.y = floor.rect.top - player_drone.height
            elif side == CollisionSide.BOTTOM:
                player_drone.velocity.y = 0
                player_drone.y = floor.rect.bottom
            elif side == CollisionSide.LEFT:
                player_drone.velocity.x = 0
                player_drone.x = floor.rect.left - player_drone.width
            elif side == CollisionSide.RIGHT:
                player_drone.velocity.x = 0
                player_drone.x = floor.rect.right

            # Aktualizacja pozycji po poprawce kolizji
            player_drone.rect.y = player_drone.y
            player_drone.rect.x = player_drone.x

        # --- Renderowanie ---
        if game_window.background_image:
            game_window.screen.blit(game_window.background_image, (0, 0))
        else:
            game_window.screen.fill(game_window.color)

        # Rysowanie z uwzględnieniem kamery
        floor_rect_cam = camera.apply(floor)
        drone_rect_cam = camera.apply(player_drone)

        pygame.draw.rect(game_window.screen, (100, 100, 100), floor_rect_cam)

        if player_drone.img:
            game_window.screen.blit(player_drone.img, drone_rect_cam)
        else:
            pygame.draw.rect(game_window.screen, (255, 0, 0), drone_rect_cam)

        # Rysujemy tylko paski mocy (usuwamy niedziałającą telemetrię)
        game_window.draw_engine_power(left_power, right_power)

        game_window.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()