import pygame
import os
from src.drone import Drone
from src.shared import GameObject, ObjectType, Color
from src.game_logic import check_collision
# ZMIANA 1: Importujemy klasę Camera z window.py
from src.window import Window, Camera


def main():
    pygame.init()

    game_window = Window(size=(800, 600), game_name="Drone Game")
    game_window.change_background_color(Color.BG_NIGHT)

    # ZMIANA 2: Tworzymy kamerę
    camera = Camera(screen_width=800, screen_height=600)

    clock = pygame.time.Clock()
    running = True

    player_drone = Drone(x=370, y=50, width=60, height=40)
    folder_skryptu = os.path.dirname(__file__)  # to da nam ścieżkę do folderu 'src'
    sciezka_drona = os.path.join(folder_skryptu, "dron.png")

    player_drone.create_image(sciezka_drona)
    player_drone.gravity = 0.5

    # ZMIANA 3: Poszerzamy podłogę (od -2000 do szerokości 4000), bo teraz dron może daleko odlecieć!
    floor = GameObject(x=-2000, y=550, width=4000, height=50, object_type=ObjectType.FLOOR)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- STEROWANIE ---
        keys = pygame.key.get_pressed()

        # ZMIANA 4: Domyślna moc silników (gdy puszczasz klawisze)
        left_power, right_power = 0.0, 0.0

        if keys[pygame.K_UP]:
            player_drone.velocity.y -= 1.0
            left_power, right_power = 0.8, 0.8

        if keys[pygame.K_LEFT]:
            player_drone.velocity.x -= 0.5
            left_power, right_power = 0.2, 1.0
        elif keys[pygame.K_RIGHT]:
            player_drone.velocity.x += 0.5
            left_power, right_power = 1.0, 0.2
        else:
            player_drone.velocity.x *= 0.95

        player_drone.velocity.x = max(-8.0, min(8.0, player_drone.velocity.x))
        player_drone.velocity.y = max(-10.0, player_drone.velocity.y)

        # --- FIZYKA GRY ---
        player_drone.velocity.y += player_drone.gravity

        # ZMIANA 5: Tutaj MUSZĄ być plusy, żeby sterowanie zgadzało się z kierunkiem
        player_drone.y += player_drone.velocity.y
        player_drone.rect.y = player_drone.y

        player_drone.x += player_drone.velocity.x
        player_drone.rect.x = player_drone.x

        # --- KOLIZJE ---
        collision_info = check_collision(player_drone, floor)
        if collision_info.collision:
            player_drone.velocity.y = 0
            player_drone.y = floor.top - player_drone.height
            player_drone.rect.y = player_drone.y

        # --- AKTUALIZACJA KAMERY ---
        # ZMIANA 6: Kamera śledzi pozycję drona
        camera.update(player_drone)

        # --- RYSOWANIE NA EKRANIE ---
        if game_window.background_image:
            game_window.screen.blit(game_window.background_image, (0, 0))
        else:
            game_window.screen.fill(game_window.color)

        # ZMIANA 7: Przepuszczamy obiekty przez kamerę (apply), żeby narysować je z przesunięciem
        floor_rect_cam = camera.apply(floor)
        pygame.draw.rect(game_window.screen, Color.FOREST_GREEN, floor_rect_cam)

        drone_rect_cam = camera.apply(player_drone)
        if player_drone.img:
            # Skalujemy grafikę na wypadek użycia w przyszłości opcji 'zoom' z kamery
            scaled_img = pygame.transform.scale(player_drone.img,
                                                (int(drone_rect_cam.width), int(drone_rect_cam.height)))
            game_window.screen.blit(scaled_img, drone_rect_cam)
        else:
            pygame.draw.rect(game_window.screen, Color.RED, drone_rect_cam)

        # ZMIANA 8: Rysujemy paski mocy silników (interfejs zostaje w miejscu, nie podlega kamerze)
        game_window.draw_engine_power(left_power, right_power)

        game_window.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()