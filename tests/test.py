import pygame
from src.window import Window, Camera
from src.drone import Drone
from src.shared import Color, Vector2, GameObject, ObjectType

def main():
    pygame.init()
    win_size = (1280, 720)
    window = Window(win_size, "Test Kamery i Zoomu")
    camera = Camera(win_size[0], win_size[1])
    clock = pygame.time.Clock()

    player = Drone(x=640, y=360, width=60, height=40)

    obstacles = [
        GameObject(200, 200, 100, 100, ObjectType.OBSTACLE),
        GameObject(1500, 400, 400, 50, ObjectType.WALL),
        GameObject(-500, 1000, 2500, 60, ObjectType.FLOOR)
    ]

    speed_multiplier = 5.0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Kółko myszy - prędkość drona
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: speed_multiplier += 1.0
                if event.button == 5: speed_multiplier = max(1.0, speed_multiplier - 1.0)

        keys = pygame.key.get_pressed()

        # Zmiana Zoomu
        if keys[pygame.K_z]:  # Przybliżenie
            camera.zoom_level = min(3.0, camera.zoom_level + 0.02)
        if keys[pygame.K_x]:  # Oddalenie
            camera.zoom_level = max(0.3, camera.zoom_level - 0.02)

        # Logika ruchu
        move_dir = pygame.Vector2(0, 0)
        if keys[pygame.K_a]: move_dir.x -= 1
        if keys[pygame.K_d]: move_dir.x += 1
        if keys[pygame.K_w]: move_dir.y -= 1
        if keys[pygame.K_s]: move_dir.y += 1

        if pygame.mouse.get_pressed()[0]:
            m_pos = pygame.mouse.get_pos()
            # Przy obliczaniu pozycji w świecie musimy teraz uwzględnić ZOOM
            center_x, center_y = camera.width / 2, camera.height / 2
            world_x = (m_pos[0] - center_x) / camera.zoom_level + center_x + camera.offset.x
            world_y = (m_pos[1] - center_y) / camera.zoom_level + center_y + camera.offset.y

            dir_vec = pygame.Vector2(world_x - player.center_x, world_y - player.center_y)
            if dir_vec.length() > 0:
                move_dir += dir_vec.normalize()

        if move_dir.length() > 0:
            move_dir = move_dir.normalize() * speed_multiplier

        player.velocity = Vector2(move_dir.x, move_dir.y)

        # POPRAWKA: Użycie wektora pos zamiast x/y
        player.pos.x += player.velocity.x
        player.pos.y += player.velocity.y
        player.rect.x = int(player.pos.x)
        player.rect.y = int(player.pos.y)

        camera.update(player)

        camera.set_limits(
            min_x=-1000.0,
            max_x=2000.0,
            min_y=-2000.0,
            max_y=1000.0
        )

        # Renderowanie
        window.screen.fill(Color.BG_DARK)

        # Rysowanie przeszkód
        for obs in obstacles:
            pygame.draw.rect(window.screen, Color.GRAY, camera.apply(obs))

        # Rysowanie drona
        pygame.draw.rect(window.screen, Color.CYAN, camera.apply(player))

        # Info UI
        font = pygame.font.SysFont(None, 24)
        zoom_txt = font.render(
            f"Zoom: {camera.zoom_level:.2f} (Zmiana Z/X) / Prędkość: {speed_multiplier:.1f} (Zmiana scroll) / Ruch Strzałki i LPM",
            True, Color.WHITE)
        window.screen.blit(zoom_txt, (20, 20))

        window.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()