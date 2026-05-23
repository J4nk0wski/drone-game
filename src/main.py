import pygame
import os
import math
from drone import Drone
from shared import GameObject, ObjectType, Color
from game_logic import check_collision
from window import Window, Camera, show_game_over_screen
from world import World


def main():
    pygame.init()

    game_window = Window(size=(1280, 720), game_name="Drone Game - Level 1")
    game_window.set_fps(60)

    # Ustawienia tekstur
    base_dir = os.path.dirname(__file__)
    textures_dir = os.path.join(base_dir, "textures")
    bg_path = os.path.join(textures_dir, "background_0.png")
    drone_path = os.path.join(textures_dir, "Drone.png")

    wall_texture_path = os.path.join(textures_dir, "ground_texture_0.png")
    meta_texture_path = os.path.join(textures_dir, "ground_texture_0.png")
    enemy_texture_path = os.path.join(textures_dir, "UGV_turret.png")

    try:
        game_window.set_background_image(bg_path)
    except pygame.error:
        game_window.change_background_color(Color.BG_NIGHT)

    camera = Camera(screen_width=1280, screen_height=720, look_ahead=20.0, damping=0.08)
    running = True

    # Swiat
    level_map = [
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
        "O                                                                              O",
        "O   S                                                                          O",
        "O                                                                              O",
        "O                                      E                                       O",
        "O                                   OOOOOOO                                    O",
        "O                                                                              O",
        "O             E                                              E                 O",
        "OOOOOOOOOOOOOOOOOOOOO                                  OOOOOOOOOOOOOOOOOOOOOOOOO",
        "O                                                                              O",
        "O                                                                        M     O",
        "O                                                                              O",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    ]

    game_world = World(tile_size=60)
    game_world.load_level(level_map)

    player_drone = Drone(x=game_world.start_x, y=game_world.start_y, width=64, height=32)
    try:
        player_drone.create_image(drone_path)
    except pygame.error:
        print("Nie znaleziono grafiki drona!")

    try:
        wall_img_raw = pygame.image.load(wall_texture_path).convert_alpha()
    except pygame.error:
        wall_img_raw = None

    try:
        meta_img_raw = pygame.image.load(meta_texture_path).convert_alpha()
    except pygame.error:
        meta_img_raw = None

    try:
        enemy_img_raw = pygame.image.load(enemy_texture_path).convert_alpha()
    except pygame.error:
        enemy_img_raw = None

    floor = GameObject(x=-2000, y=2500, width=8000, height=50, object_type=ObjectType.FLOOR)
    is_game_over = False
    is_game_won = False

    while running:
        dt = 1.0 / game_window.fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            player_drone.reset(game_world.start_x, game_world.start_y)
            player_drone.destroyed = False
            is_game_over = False
            is_game_won = False

        if not is_game_over and not is_game_won:
            if keys[pygame.K_w]:
                player_drone.left_rotor.set_force(
                    min(player_drone.left_rotor.force + 2, player_drone.left_rotor.max_force))
            if keys[pygame.K_s]:
                player_drone.left_rotor.set_force(max(player_drone.left_rotor.force - 2, 0))
            if keys[pygame.K_UP]:
                player_drone.right_rotor.set_force(
                    min(player_drone.right_rotor.force + 2, player_drone.right_rotor.max_force))
            if keys[pygame.K_DOWN]:
                player_drone.right_rotor.set_force(max(player_drone.right_rotor.force - 2, 0))
        else:
            player_drone.left_rotor.set_force(0)
            player_drone.right_rotor.set_force(0)

        old_x, old_y = player_drone.x, player_drone.y

        if not is_game_over and not is_game_won:
            player_drone.update_physics(dt)

        player_drone.rect.x = player_drone.x
        player_drone.rect.y = player_drone.y

        # Kolizje
        if game_world.landing_pad and check_collision(player_drone, game_world.landing_pad).collision:
            if abs(player_drone.velocity_y) < 150 and abs(player_drone.angle) < 0.3:
                is_game_won = True
                player_drone.velocity_x = player_drone.velocity_y = 0
            else:
                player_drone.health -= 100
                player_drone.health_check()
                if player_drone.destroyed:
                    is_game_over = True

        for obs in game_world.obstacles:
            if check_collision(player_drone, obs).collision:
                player_drone.x, player_drone.y = old_x, old_y
                player_drone.rect.x, player_drone.rect.y = old_x, old_y
                player_drone.velocity_x *= -0.3
                player_drone.velocity_y *= -0.3

        for enemy in game_world.enemies:
            if check_collision(player_drone, enemy).collision:
                player_drone.x, player_drone.y = old_x, old_y
                player_drone.rect.x, player_drone.rect.y = old_x, old_y
                player_drone.velocity_x *= -0.3
                player_drone.velocity_y *= -0.3
                player_drone.health -= 15
                player_drone.health_check()
                if player_drone.destroyed:
                    is_game_over = True

        if check_collision(player_drone, floor).collision:
            is_game_over = True

        camera.update(player_drone)

        # Renderowanie
        game_window.render()

        if wall_img_raw:
            scaled_wall = pygame.transform.scale(wall_img_raw, (game_world.tile_size, game_world.tile_size))
            for obs in game_world.obstacles:
                game_window.screen.blit(scaled_wall, camera.apply(obs))
        else:
            for obs in game_world.obstacles:
                pygame.draw.rect(game_window.screen, Color.NEON_BLUE, camera.apply(obs))

        if game_world.landing_pad:
            pad_cam_rect = camera.apply(game_world.landing_pad)
            if meta_img_raw:
                scaled_meta = pygame.transform.scale(meta_img_raw, (pad_cam_rect.width, pad_cam_rect.height))
                game_window.screen.blit(scaled_meta, pad_cam_rect)
            else:
                pygame.draw.rect(game_window.screen, Color.GREEN, pad_cam_rect)

            game_window.draw_text("H", (pad_cam_rect.centerx, pad_cam_rect.centery), font_size=24, color=Color.WHITE, centered=True)

        if enemy_img_raw:
            scaled_enemy = pygame.transform.scale(enemy_img_raw, (game_world.tile_size, game_world.tile_size))
            for enemy in game_world.enemies:
                game_window.screen.blit(scaled_enemy, camera.apply(enemy))
        else:
            for enemy in game_world.enemies:
                pygame.draw.rect(game_window.screen, Color.RED, camera.apply(enemy))

        drone_cam = camera.apply(player_drone)
        if player_drone.img:
            scaled_img = pygame.transform.scale(player_drone.img, (int(drone_cam.width), int(drone_cam.height)))
            rotated_img = pygame.transform.rotate(scaled_img, -math.degrees(player_drone.angle))
            game_window.screen.blit(rotated_img, rotated_img.get_rect(center=drone_cam.center))
        else:
            pygame.draw.rect(game_window.screen, Color.RED, drone_cam)

        # UI
        health_pct = max(0.0, player_drone.health / player_drone.max_health)
        pygame.draw.rect(game_window.screen, Color.RED, (20, 20, 200, 20))
        # POPRAWKA: Rzutowanie na int w szerokości paska!
        pygame.draw.rect(game_window.screen, Color.GREEN, (20, 20, int(200 * health_pct), 20))
        game_window.draw_text(f"HP: {int(player_drone.health)}", (225, 20), font_size=18, color=Color.WHITE)
        game_window.draw_text(f"ZYCIA: {player_drone.lives}", (20, 50), font_size=24, color=Color.WHITE)

        game_window.draw_engine_power(
            player_drone.left_rotor.force / player_drone.left_rotor.max_force,
            player_drone.right_rotor.force / player_drone.right_rotor.max_force
        )

        if is_game_over:
            show_game_over_screen(game_window, player_drone, game_world.start_x, game_world.start_y)
            if not player_drone.destroyed:
                is_game_over = False
        elif is_game_won:
            game_window.draw_text("MISSION COMPLETE",
                                  (game_window.screen_size[0] // 2, game_window.screen_size[1] // 2), font_size=72,
                                  color=Color.YELLOW, centered=True)

        game_window.update()
        game_window.tick()

    pygame.quit()


if __name__ == "__main__":
    main()