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

    camera = Camera(screen_width=1280, screen_height=720, look_ahead=0.0, damping=0.08)
    running = True

    # inicjalizacja swiata
    game_world = World(tile_size=60)
    game_world.load_level(1)

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
            # Opcjonalnie: można tu wywołać game_world.load_level(1) żeby zresetować monety i wieżyczki
            for enemy in game_world.enemies:
                enemy.bullets.clear()

        # Wyliczenie przyrostu siły silników
        left_force_change = (player_drone.left_rotor.max_force / 1.5) * dt
        right_force_change = (player_drone.right_rotor.max_force / 1.5) * dt

        left_force_change_fast = (player_drone.left_rotor.max_force / 0.5) * dt
        right_force_change_fast = (player_drone.right_rotor.max_force / 0.5) * dt

        if not is_game_over and not is_game_won:
            # Strzelanie
            if keys[pygame.K_SPACE]:
                player_drone.shoot()

            if keys[pygame.K_w]:
                player_drone.right_rotor.set_force(
                    min(player_drone.right_rotor.force + right_force_change, player_drone.right_rotor.max_force))
            if keys[pygame.K_s]:
                player_drone.right_rotor.set_force(max(player_drone.right_rotor.force - right_force_change, 0))
            if keys[pygame.K_d]:
                player_drone.right_rotor.set_force(
                    min(player_drone.right_rotor.force + right_force_change_fast, player_drone.right_rotor.max_force))
            if keys[pygame.K_a]:
                player_drone.right_rotor.set_force(max(player_drone.right_rotor.force - right_force_change_fast, 0))

            if keys[pygame.K_UP]:
                player_drone.left_rotor.set_force(
                    min(player_drone.left_rotor.force + left_force_change, player_drone.left_rotor.max_force))
            if keys[pygame.K_DOWN]:
                player_drone.left_rotor.set_force(max(player_drone.left_rotor.force - left_force_change, 0))
            if keys[pygame.K_RIGHT]:
                player_drone.left_rotor.set_force(
                    min(player_drone.left_rotor.force + left_force_change_fast, player_drone.left_rotor.max_force))
            if keys[pygame.K_LEFT]:
                player_drone.left_rotor.set_force(max(player_drone.left_rotor.force - left_force_change_fast, 0))
        else:
            player_drone.left_rotor.set_force(0)
            player_drone.right_rotor.set_force(0)

        old_pos_x, old_pos_y = player_drone.pos.x, player_drone.pos.y

        if not is_game_over and not is_game_won:
            player_drone.update_physics(dt)

            player_drone.update_bullets(game_world.enemies, game_world.obstacles)

            for enemy in game_world.enemies:
                enemy.shoot(player_drone, game_world.obstacles)
                enemy.update_bullets(player_drone, game_world.obstacles, 8000, 8000)

        player_drone.rect.x = int(player_drone.pos.x)
        player_drone.rect.y = int(player_drone.pos.y)

        # --- KOLIZJE ---
        # 1. Lądowisko
        if game_world.landing_pad and check_collision(player_drone, game_world.landing_pad).collision:
            if abs(player_drone.velocity.y) < 150 and abs(player_drone.angle) < 0.3:
                is_game_won = True
                player_drone.velocity.x = player_drone.velocity.y = 0
            else:
                player_drone.health -= 100
                player_drone.health_check()
                if player_drone.destroyed:
                    is_game_over = True

        # 2. Przeszkody (ściany)
        for obs in game_world.obstacles:
            if check_collision(player_drone, obs).collision:
                player_drone.pos.x, player_drone.pos.y = old_pos_x, old_pos_y
                player_drone.rect.x, player_drone.rect.y = int(old_pos_x), int(old_pos_y)
                player_drone.velocity.x *= -0.3
                player_drone.velocity.y *= -0.3
                if abs(player_drone.velocity.x) < 15:
                    player_drone.velocity.x = 0
                if abs(player_drone.velocity.y) < 15:
                    player_drone.velocity.y = 0

        # 3. Wieżyczki
        for enemy in game_world.enemies:
            if check_collision(player_drone, enemy).collision:
                player_drone.pos.x, player_drone.pos.y = old_pos_x, old_pos_y
                player_drone.rect.x, player_drone.rect.y = int(old_pos_x), int(old_pos_y)
                player_drone.velocity.x *= -0.3
                player_drone.velocity.y *= -0.3
                if abs(player_drone.velocity.x) < 15:
                    player_drone.velocity.x = 0
                if abs(player_drone.velocity.y) < 15:
                    player_drone.velocity.y = 0
                player_drone.health -= 15
                player_drone.health_check()
                if player_drone.destroyed:
                    is_game_over = True

        # 4. Monety (ZBIERANIE!)
        # Sprawdzamy kopie listy, bo bedziemy usuwac z niej elementy
        for coin in getattr(game_world, 'coins', []):  # Zabezpieczenie jesli w world.py nie ma atrybutu coins
            if check_collision(player_drone, coin).collision:
                player_drone.score += coin.value
                game_world.coins.remove(coin)

        if check_collision(player_drone, floor).collision:
            is_game_over = True

        camera.update(player_drone)

        # --- RENDEROWANIE ---
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
            game_window.draw_text("H", (pad_cam_rect.centerx, pad_cam_rect.centery), font_size=24, color=Color.WHITE,
                                  centered=True)

        # Rysowanie przeciwników i ich pocisków (żółte)
        for enemy in game_world.enemies:
            if enemy_img_raw:
                scaled_enemy = pygame.transform.scale(enemy_img_raw, (game_world.tile_size, game_world.tile_size))
                enemy_cam = camera.apply(enemy)
                rotated_enemy = pygame.transform.rotate(scaled_enemy, enemy.angle)
                game_window.screen.blit(rotated_enemy, rotated_enemy.get_rect(center=enemy_cam.center))
            else:
                pygame.draw.rect(game_window.screen, Color.RED, camera.apply(enemy))

            for bullet in enemy.bullets:
                bullet_cam = camera.apply(bullet)
                pygame.draw.circle(game_window.screen, Color.YELLOW, bullet_cam.center, int(bullet.width / 2))

        # Rysowanie monet (tymczasowo na pomaranczowo)
        for coin in getattr(game_world, 'coins', []):
            coin_cam = camera.apply(coin)
            # Jesli dodasz teksture, mozesz ja tutaj wstawic. Na razie rysujemy kolko
            pygame.draw.circle(game_window.screen, Color.ORANGE, coin_cam.center, int(coin.width / 2))

        # Rysowanie pocisków gracza (cyjanowe)
        for bullet in player_drone.bullets:
            bullet_cam = camera.apply(bullet)
            pygame.draw.circle(game_window.screen, Color.CYAN, bullet_cam.center, int(bullet.width / 2))

        drone_cam = camera.apply(player_drone)
        if player_drone.img:
            scaled_img = pygame.transform.scale(player_drone.img, (int(drone_cam.width), int(drone_cam.height)))
            rotated_img = pygame.transform.rotate(scaled_img, -math.degrees(player_drone.angle))
            game_window.screen.blit(rotated_img, rotated_img.get_rect(center=drone_cam.center))
        else:
            pygame.draw.rect(game_window.screen, Color.RED, drone_cam)

        # --- UI ---
        health_pct = max(0.0, player_drone.health / player_drone.max_health)
        pygame.draw.rect(game_window.screen, Color.RED, (20, 20, 200, 20))
        pygame.draw.rect(game_window.screen, Color.GREEN, (20, 20, int(200 * health_pct), 20))
        game_window.draw_text(f"HP: {int(player_drone.health)}", (225, 20), font_size=18, color=Color.WHITE)
        game_window.draw_text(f"SCORE: {player_drone.score}", (10, 80), font_size=24, color=Color.WHITE)
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