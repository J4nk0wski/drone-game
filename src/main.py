import pygame
import os
from src.drone import Drone
from src.shared import GameObject, ObjectType, Color
from src.game_logic import check_collision
from src.window import Window, Camera
from src.renderer import end_screen_text


def main():
    pygame.init()

    game_window = Window(size=(800, 600), game_name="Drone Game")
    game_window.change_background_color(Color.BG_NIGHT)

    # Tworze kamerę
    camera = Camera(screen_width=800, screen_height=600)

    clock = pygame.time.Clock()
    running = True

    player_drone = Drone(x=370, y=50, width=60, height=40)
    folder_skryptu = os.path.dirname(__file__)
    sciezka_drona = os.path.join(folder_skryptu, "dron.png")

    player_drone.create_image(sciezka_drona)
    player_drone.gravity = 0.5

    # Poszerzam podłogę
    floor = GameObject(x=-2000, y=550, width=4000, height=50, object_type=ObjectType.FLOOR)

    # Tworze listę przeszkód
    obstacles = [
        GameObject(x=100, y=400, width=50, height=150, object_type=ObjectType.OBSTACLE),
        GameObject(x=600, y=300, width=100, height=50, object_type=ObjectType.OBSTACLE),
        GameObject(x=-300, y=200, width=200, height=40, object_type=ObjectType.OBSTACLE)
    ]

    # --- FLAGA STANU GRY ---
    is_game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Sterowanie
        keys = pygame.key.get_pressed()

        # Szybki reset
        if keys[pygame.K_r]:
            player_drone.x = 370
            player_drone.y = 50
            player_drone.velocity.x = 0
            player_drone.velocity.y = 0
            is_game_over = False  # Resetujemy stan gry, wyłączamy napis

        left_power, right_power = 0.0, 0.0

        # Wyłączamy sterowanie silnikami, gdy gra jest przegrana
        if not is_game_over:
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

        # Zapis pozycji
        old_x = player_drone.x
        old_y = player_drone.y

        # Fizyka gry
        # Grawitacja działa tylko, gdy gra trwa
        if not is_game_over:
            player_drone.velocity.y += player_drone.gravity

        player_drone.y += player_drone.velocity.y
        player_drone.rect.y = player_drone.y

        player_drone.x += player_drone.velocity.x
        player_drone.rect.x = player_drone.x

        # --- KOLIZJE Z PODŁOGĄ ---
        collision_info = check_collision(player_drone, floor)
        if collision_info.collision:
            player_drone.velocity.y = 0
            player_drone.y = floor.top - player_drone.height
            player_drone.rect.y = player_drone.y

        # Kolizje z przeszkodami
        for obs in obstacles:
            if check_collision(player_drone, obs).collision:
                #Przegrana
                is_game_over = True

                #Cofam drona do bezpiecznej pozycji sprzed klatki
                player_drone.x = old_x
                player_drone.y = old_y
                player_drone.rect.x = old_x
                player_drone.rect.y = old_y

                #Zatrzymujemy go w miejscu
                player_drone.velocity.x = 0
                player_drone.velocity.y = 0

        # Kamera
        camera.update(player_drone)

        #Ekran
        if game_window.background_image:
            game_window.screen.blit(game_window.background_image, (0, 0))
        else:
            game_window.screen.fill(game_window.color)

        floor_rect_cam = camera.apply(floor)
        pygame.draw.rect(game_window.screen, Color.FOREST_GREEN, floor_rect_cam)

        for i, obs in enumerate(obstacles):
            obs_rect_cam = camera.apply(obs)
            color = Color.NEON_PINK if i % 2 == 0 else Color.NEON_BLUE
            pygame.draw.rect(game_window.screen, color, obs_rect_cam)
            pygame.draw.rect(game_window.screen, Color.WHITE, obs_rect_cam, width=2)

        drone_rect_cam = camera.apply(player_drone)
        if player_drone.img:
            scaled_img = pygame.transform.scale(player_drone.img,
                                                (int(drone_rect_cam.width), int(drone_rect_cam.height)))
            game_window.screen.blit(scaled_img, drone_rect_cam)
        else:
            pygame.draw.rect(game_window.screen, Color.RED, drone_rect_cam)

        game_window.draw_engine_power(left_power, right_power)

        # Pokazanie tekstu koncowego
        if is_game_over:
            end_screen_text(game_window)

        game_window.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()