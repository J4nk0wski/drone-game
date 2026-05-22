import pygame
import os
from drone import Drone
from shared import GameObject, ObjectType, Color
from game_logic import check_collision
from window import Window, Camera
import renderer
import math

def main():
    pygame.init()

    game_window = Window(size=(1280, 720), game_name="Drone Game")
    game_window.change_background_color(Color.BG_NIGHT)

    # Tworze kamerę
    camera = Camera(screen_width=800, screen_height=600)

    clock = pygame.time.Clock()
    running = True

    player_drone = Drone(x=370, y=50, width=30, height=20)
    folder_skryptu = os.path.dirname(__file__)
    sciezka_drona = os.path.join(folder_skryptu, "dron.png")

    player_drone.create_image(sciezka_drona)


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
            player_drone.velocity_x = 0
            player_drone.velocity_y = 0
            is_game_over = False  # Resetujemy stan gry, wyłączamy napis


        # Wyłączamy sterowanie silnikami, gdy gra jest przegrana
        if not is_game_over:
            if keys[pygame.K_w]:
                player_drone.left_rotor.set_force(min(player_drone.left_rotor.force + 1, player_drone.left_rotor.max_force))
            if keys[pygame.K_s]:
                player_drone.left_rotor.set_force(max(player_drone.left_rotor.force - 1, 0))
            if keys[pygame.K_UP]:
                player_drone.right_rotor.set_force(min(player_drone.right_rotor.force + 1, player_drone.right_rotor.max_force))
            if keys[pygame.K_DOWN]:
                player_drone.right_rotor.set_force(max(player_drone.right_rotor.force - 1, 0))

        # Zapis pozycji
        old_x = player_drone.x
        old_y = player_drone.y

        dt = clock.tick(60) / 1000.0
        if not is_game_over:
            player_drone.update_physics(dt)
            
            #player_drone.velocity.x = max(-8.0, min(8.0, player_drone.velocity.x))
            #player_drone.velocity.y = max(-10.0, player_drone.velocity.y)
        player_drone.rect.x = player_drone.x
        player_drone.rect.y = player_drone.y

        
        

        # Fizyka gry
        # Grawitacja działa tylko, gdy gra trwa
        """
        if not is_game_over:
            player_drone.velocity.y += player_drone.gravity

        player_drone.y += player_drone.velocity.y
        player_drone.rect.y = player_drone.y

        player_drone.x += player_drone.velocity.x
        player_drone.rect.x = player_drone.x
        """
        # --- KOLIZJE Z PODŁOGĄ ---
        collision_info = check_collision(player_drone, floor)
        if collision_info.collision:
            player_drone.velocity_y = 0
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
                player_drone.velocity_x = 0
                player_drone.velocity_y = 0

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
            scaled_img = pygame.transform.scale(player_drone.img, (int(drone_rect_cam.width), int(drone_rect_cam.height)))
            
            angle_deg = math.degrees(player_drone.angle)
            rotated_img = pygame.transform.rotate(scaled_img, -angle_deg)
            rotated_rect = rotated_img.get_rect(center=drone_rect_cam.center)

            game_window.screen.blit(rotated_img, rotated_rect)
        else:
            pygame.draw.rect(game_window.screen, Color.RED, drone_rect_cam)

        game_window.draw_engine_power(player_drone.left_rotor.force/ player_drone.left_rotor.max_force, player_drone.right_rotor.force/ player_drone.right_rotor.max_force)

        # Pokazanie tekstu koncowego
        if is_game_over:
            renderer.show_game_over_screen(game_window, player_drone,)


        """
        Funkcje pomocnicze do wyswietlania aktualnego polozenia i kata nachylenia
        ang_text = "Angle: " + str(round((player_drone.angle * 360) / (2 *math.pi), 1))
        game_window.draw_text(ang_text, (100, 100), 24, (255, 255, 255))
        x_pos_text = "x pos: " + str(round(player_drone.x, 2))
        y_pos_text = "y pos: " + str(round(player_drone.y, 2))
        game_window.draw_text(x_pos_text, (100, 120), 24, (255, 255, 255))
        game_window.draw_text(y_pos_text, (100, 140), 24, (255, 255, 255))
        """


        game_window.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":#
    main()