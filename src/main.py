import pygame
from src.drone import Drone
from src.shared import GameObject, ObjectType
from src.game_logic import check_collision
#Importujemy klasę Window
from src.window import Window


def main():
    pygame.init()

    #Używamy klasy window do tworzenia okna
    # Podajemy nasz rozmiar i tytuł gry
    game_window = Window(size=(800, 600), game_name="Drone Game")
    # Zmieniamy domyślne białe tło na czarne
    game_window.change_background_color((0, 0, 0))

    clock = pygame.time.Clock()
    running = True

    # 1. Tworzymy drona
    player_drone = Drone(x=370, y=50, width=60, height=40)
    player_drone.create_image(None)
    player_drone.gravity = 0.5

    # 2. Tworzymy podłogę
    floor = GameObject(x=0, y=550, width=800, height=50, object_type=ObjectType.FLOOR)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #sterowanie
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player_drone.velocity.y -= 1.0

        if keys[pygame.K_LEFT]:
            player_drone.velocity.x = -5
        elif keys[pygame.K_RIGHT]:
            player_drone.velocity.x = 5
        else:
            player_drone.velocity.x = 0

        # fizyka
        player_drone.velocity.y += player_drone.gravity
        player_drone.y += player_drone.velocity.y
        player_drone.rect.y = player_drone.y

        player_drone.x += player_drone.velocity.x
        player_drone.rect.x = player_drone.x

        # kolizje
        collision_info = check_collision(player_drone, floor)
        if collision_info.collision:
            player_drone.velocity.y = 0
            player_drone.y = floor.top - player_drone.height
            player_drone.rect.y = player_drone.y

        # Ekran

        # Czyścimy tło używając klasy Window
        if game_window.background_image:
            game_window.screen.blit(game_window.background_image, (0, 0))
        else:
            game_window.screen.fill(game_window.color)

        # Rysujemy podłogę i drona na ekranie
        pygame.draw.rect(game_window.screen, (100, 100, 100), floor.rect)

        if player_drone.img:
            game_window.screen.blit(player_drone.img, player_drone.rect)
        else:
            pygame.draw.rect(game_window.screen, (255, 0, 0), player_drone.rect)

        # Używamy klasy window do odświeżania ekranu
        game_window.update()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()