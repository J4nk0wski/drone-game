import pygame
import os
from src.drone import Drone
from src.shared import GameObject, ObjectType, Color
from src.game_logic import check_collision
# Importuje klasę Camera z window.py
from src.window import Window, Camera


def main():
    pygame.init()

    game_window = Window(size=(800, 600), game_name="Drone Game")
    game_window.change_background_color(Color.BG_NIGHT)

    # Tworze kamerę
    camera = Camera(screen_width=800, screen_height=600)

    clock = pygame.time.Clock()
    running = True

    player_drone = Drone(x=370, y=50, width=60, height=40)
    folder_skryptu = os.path.dirname(__file__)  # to da nam ścieżkę do folderu 'src'
    sciezka_drona = os.path.join(folder_skryptu, "dron.png")

    player_drone.create_image(sciezka_drona)
    player_drone.gravity = 0.5

    # Poszerzam podłogę (od -2000 do szerokości 4000), bo teraz dron może daleko odlecieć
    floor = GameObject(x=-2000, y=550, width=4000, height=50, object_type=ObjectType.FLOOR)

    # Tworzymy listę przeszkód z użyciem ObjectType z shared.py
    obstacles = [
        GameObject(x=100, y=400, width=50, height=150, object_type=ObjectType.OBSTACLE),
        GameObject(x=600, y=300, width=100, height=50, object_type=ObjectType.OBSTACLE),
        GameObject(x=-300, y=200, width=200, height=40, object_type=ObjectType.OBSTACLE)
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # sterowanie
        # szybki reset
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_drone.x = 370
            player_drone.y = 50
            player_drone.velocity.x = 0
            player_drone.velocity.y = 0

        # Domyślna moc silników (gdy puszczasz klawisze)
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

        # fizyka gry
        player_drone.velocity.y += player_drone.gravity

        player_drone.y += player_drone.velocity.y
        player_drone.rect.y = player_drone.y

        player_drone.x += player_drone.velocity.x
        player_drone.rect.x = player_drone.x

        # Kolizje
        collision_info = check_collision(player_drone, floor)
        if collision_info.collision:
            player_drone.velocity.y = 0
            player_drone.y = floor.top - player_drone.height
            player_drone.rect.y = player_drone.y

        # Kolizje z przeszkodami (efekt odbicia)
        for obs in obstacles:
            if check_collision(player_drone, obs).collision:
                # Odwracamy wektor prędkości (dron się odbija i traci trochę pędu)
                player_drone.velocity.x *= -0.8
                player_drone.velocity.y *= -0.8
                # Lekko wypychamy drona, żeby nie zablokował się w teksturze
                player_drone.y -= 2
                player_drone.rect.y = player_drone.y

        # Kamera
        camera.update(player_drone)

        # rysowanie na ekranie
        if game_window.background_image:
            game_window.screen.blit(game_window.background_image, (0, 0))
        else:
            game_window.screen.fill(game_window.color)

        # Przepuszczam obiekty przez kamerę (apply), żeby narysować je z przesunięciem
        floor_rect_cam = camera.apply(floor)
        pygame.draw.rect(game_window.screen, Color.FOREST_GREEN, floor_rect_cam)

        #Rysowanie przeszkód z użyciem neonowych kolorów
        for i, obs in enumerate(obstacles):
            obs_rect_cam = camera.apply(obs)
            # Używamy różnych kolorów na przemian dla lepszego efektu wizualnego
            color = Color.NEON_PINK if i % 2 == 0 else Color.NEON_BLUE
            pygame.draw.rect(game_window.screen, color, obs_rect_cam)
            # Dodajemy białą ramkę, żeby wyglądało jak prawdziwa przeszkoda w grze
            pygame.draw.rect(game_window.screen, Color.WHITE, obs_rect_cam, width=2)

        drone_rect_cam = camera.apply(player_drone)
        if player_drone.img:
            # Skaluje grafikę na wypadek użycia w przyszłości opcji 'zoom' z kamery
            scaled_img = pygame.transform.scale(player_drone.img,
                                                (int(drone_rect_cam.width), int(drone_rect_cam.height)))
            game_window.screen.blit(scaled_img, drone_rect_cam)
        else:
            pygame.draw.rect(game_window.screen, Color.RED, drone_rect_cam)

        # Rysuje paski mocy silników (interfejs zostaje w miejscu, nie podlega kamerze)
        game_window.draw_engine_power(left_power, right_power)

        game_window.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()