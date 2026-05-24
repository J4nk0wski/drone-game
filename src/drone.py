import pygame
import math
from shared import GameObject, ObjectType, Vector2

from math import atan2, degrees, radians, sin, cos
"""
klasa drona którym można sterować

Klasa dziedziczy po GameObject 

Atrybuty:
- destroyed - zmienna określająca czy obiekt jest zniszczony (bool)
- front_rotor_force - siła przedniego rotora (początkowo 0)
- back_rotor_force - siła tylniego rotora (początkowo 0) 
- score - zdobyte punkty (początkowo 0)
- health - zdrowie
- lives - życia
- max_health - zdrowie (domyślnie 100)
- max_lives - życia (domyślnie 3)
"""
class Drone(GameObject):
    def __init__(self, x: float=0, y: float=0, width: float=60, height: float=40) -> None:
        super().__init__(x, y, width, height, ObjectType.DRONE)
        self.destroyed: bool = False
        self.max_lives: int = 3
        self.max_health: int = 100

        self.mass = 0.1
        self.inertia = 10
        self.gravity = 500
        self.angular_velocity = 0
        self.angle = 0
        self.velocity = Vector2(0, 0)

        self.score: int = 0
        self.health = self.max_health
        self.lives = self.max_lives

        self.right_rotor = Rotor(width/2, self.center_x + width/2, y)
        self.left_rotor = Rotor(-width/2, self.center_x - width/2, y)

        # --- ARSENAŁ DRONA ---
        self.bullets: list['Bullet'] = []
        self.last_shot_time: float = 0
        self.cooldown: int = 500

    """
    Funkcja symuluje fizykę obiektu.
    """
    def update_physics(self, dt: float) -> None:
        torque = self.right_rotor.force * self.right_rotor.offset + self.left_rotor.force * self.left_rotor.offset
        total_lift = self.right_rotor.force + self.left_rotor.force

        k = 10
        ax = k *(math.sin(self.angle) * total_lift) / self.mass
        ay = k * (-math.cos(self.angle) * total_lift) / self.mass + self.gravity

        #opor powietrza
        self.velocity.x *= 0.99
        self.velocity.y *= 0.99
        self.angular_velocity *= 0.90

        self.velocity.x += ax * dt
        self.velocity.y += ay * dt

        angular_acc = torque / self.inertia
        self.angular_velocity += angular_acc * dt
        self.angle += self.angular_velocity * dt

        if not self.max_angle is None:
            self.angle = max(-self.max_angle, min(self.max_angle, self.angle))
            self.angle += self.angular_velocity * dt

        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

    """
    zwraca sily jakie musza miec silniki tak aby dron pozostawal w rownowadze
    """
    def balance_state(self) -> tuple[float, float]:
        cos_angle = cos(self.angle)
        if abs(cos_angle) < 1e-6:
            raise ValueError("Kat nachylenia jest zbyt duzy")
        k = 10
        total_lift = (self.gravity * self.mass) / (k * cos_angle)
        force = total_lift / 2
        return force, force

    """
    Aktualizuje informacje na temat zdrowia.
    """
    def health_check(self) -> None:
        if self.health <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.destroyed = True
            self.health = self.max_health

    """
    Przywraca parametry drona do stanu początkowego
    Metoda przyjmuje pozycję początkową (inaczej x=0, y=0)
    """
    def reset(self, start_x: float=0, start_y: float=0) -> None:
        self.pos.x = start_x
        self.pos.y = start_y
        self.velocity = Vector2(0, 0)
        self.angular_velocity = 0
        self.score = 0
        self.health = self.max_health
        self.lives = self.max_lives
        self.bullets.clear()

    """
    Wypuszcza 3 pociski (Shotgun).
    """
    def shoot(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cooldown:
            self.last_shot_time = current_time
            base_angle = degrees(self.angle)
            spread = 12
            speed = 25

            self.bullets.append(Bullet(self.pos.x, self.pos.y, base_angle + spread, speed))
            self.bullets.append(Bullet(self.pos.x, self.pos.y, base_angle, speed))
            self.bullets.append(Bullet(self.pos.x, self.pos.y, base_angle - spread, speed))

    """
    Aktualizuje kule gracza i niszczy wieżyczki.
    """
    def update_bullets(self, enemies: list[GameObject], obstacles: list[GameObject]) -> None:
        for bullet in reversed(self.bullets):
            bullet.update_pos()
            hit_something = False

            for obs in obstacles:
                if bullet.rect.colliderect(obs.rect):
                    hit_something = True
                    break

            if not hit_something:
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        enemies.remove(enemy)
                        self.score += 100
                        hit_something = True
                        break

            if (bullet.pos.x < -2000 or bullet.pos.x > 8000 or
                    bullet.pos.y < -2000 or bullet.pos.y > 8000):
                hit_something = True

            if hit_something and bullet in self.bullets:
                self.bullets.remove(bullet)


"""
Klasa podłogi. Teraz bardzo uboga, ale z czasem można dodać mechaniki specjalne dla podłogi.
"""
class Floor(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
        super().__init__(x, y, width, height, ObjectType.FLOOR)

"""
Klasa ściany. Teraz bardzo uboga, ale z czasem można dodać mechaniki specjalne dla ściany.
"""
class Wall(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
        super().__init__(x, y, width, height, ObjectType.WALL)

"""
Klasa przeszkody.
"""
class Obstacle(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
        super().__init__(x, y, width, height, ObjectType.OBSTACLE)

"""
Klasa statycznego przeciwnika, który strzela.
"""
class Enemy(GameObject):
    def __init__(self, x: float = 0, y: float = 0, reload_time: int=3000, bullet_speed: float=7) -> None:
        super().__init__(x, y, 50, 50, ObjectType.ENEMY)
        self.reload_time: int = reload_time
        self.reload_timer: float = 0

        self.reloading: bool = False
        self.bullets: list[Bullet] = []
        self.bullet_speed: float = bullet_speed

    def search(self, dron: GameObject, objects: list[GameObject]) -> bool:
        start_pos = self.rect.center
        end_pos = dron.rect.center

        for obj in objects:
            if obj == self or obj == dron:
                continue

            if obj.rect.clipline(start_pos, end_pos):
                return False

        return True

    def shoot(self, dron: GameObject, objects: list[GameObject]):
        if not self.reloading and self.search(dron, objects):
            self.reload_timer = pygame.time.get_ticks()
            self.reloading = True

            end_pos = dron.center
            start_pos = self.center
            diff_pos = end_pos - start_pos

            new_bullet = Bullet(self.center_x, self.center_y, self.tilt(diff_pos), self.bullet_speed)
            self.bullets.append(new_bullet)
        else:
            self.reload()

    def reload(self) -> None:
        if self.reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.reload_timer >= self.reload_time:
                self.reloading = False

    @staticmethod
    def tilt(dist: Vector2) -> float:
        angle_rad = atan2(dist.y, dist.x)
        angle_deg = degrees(angle_rad)

        return  -angle_deg

    def update_bullets(self, dron: Drone, objects: list[GameObject], screen_width: int = 800, screen_height: int = 600) -> None:
        for bullet in reversed(self.bullets):
            bullet.update_pos()

            hit_something = False

            for obj in objects:
                if obj == self or obj.object_type == ObjectType.BULLET:
                    continue

                if bullet.rect.colliderect(obj.rect):
                    hit_something = True
                    break

            if bullet.rect.colliderect(dron.rect):
                dron.health -= 30
                dron.health_check()
                hit_something = True

            if (bullet.pos.x < 0 or bullet.pos.x > screen_width or
                    bullet.pos.y < 0 or bullet.pos.y > screen_height):
                hit_something = True

            if hit_something:
                self.bullets.remove(bullet)

"""
Klasa pocisku, króry znika po trafieniu w przeszkodę.
"""
class Bullet(GameObject):
    def __init__(self, x: float, y: float, angle: float, speed: float) -> None:
        super().__init__(x, y, 10, 10, ObjectType.BULLET)
        self.speed = speed
        self.angle = angle
        self.velocity: Vector2 = self.calculate_velocity_from_angle()

    def calculate_velocity_from_angle(self) -> Vector2:
        standard_angle_deg = -self.angle
        angle_rad = radians(standard_angle_deg)
        vel_x = cos(angle_rad) * self.speed
        vel_y = sin(angle_rad) * self.speed
        return Vector2(vel_x, vel_y)

    def update_pos(self) -> None:
        self.pos += self.velocity

"""
Klasa Rotora przeznaczona do użytku w klasie Drone.
"""
class Rotor:
    def __init__(self, offset_x: float, x_pos ,y_pos, size: int = 6):
        self.offset: float = offset_x
        self.force: float = 0.0
        self.size: int = size
        self.x = x_pos
        self.y = y_pos
        self.max_force = 10

    def set_force(self, force: float):
        self.force = max(0.0, min(force, self.max_force))

    """
    def set_force(self, force: float) -> None:
        #Ustawia siłę silnika (nie może być ujemna)
        self.force = max(0.0, force)
        angle_rad = atan2(self.velocity.y, self.velocity.x)
        angle_deg = degrees(angle_rad)

        self.angle = -angle_deg
    """

"""
Monety po których zebraniu dron otrzymuje punkty.
"""
class Coin(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 40, height: float = 40, value: float = 5):
        super().__init__(x, y, width, height, ObjectType.COIN)
        self.value = value