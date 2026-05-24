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

--------/health_check/--------
jeśli zdrowie <= 0 zabiera życie i regeneruje zdrowie 
jeśli brak żyć dron.destroyed = True
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

"""
Klasa podłogi. Teraz bardzo uboga, ale z czasem można dodać mechaniki specjalne dla podłogi.

Klasa dziedziczy po GameObject 
"""
class Floor(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
        super().__init__(x, y, width, height, ObjectType.FLOOR)

"""
Klasa ściany. Teraz bardzo uboga, ale z czasem można dodać mechaniki specjalne dla ściany.

Klasa dziedziczy po GameObject 
"""
class Wall(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
        super().__init__(x, y, width, height, ObjectType.WALL)

"""
Klasa przeszkody.

Klasa dziedziczy po GameObject 
"""
class Obstacle(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
        super().__init__(x, y, width, height, ObjectType.OBSTACLE)

"""
Klasa statycznego przeciwnika, który strzela.

Klasa dziedziczy po GameObject 
"""
class Enemy(GameObject):
    def __init__(self, x: float = 0, y: float = 0, reload_time: int=3000, bullet_speed: float=7) -> None:
        super().__init__(x, y, 50, 50, ObjectType.ENEMY)
        #czas w milisekundach
        self.reload_time: int = reload_time
        self.reload_timer: float = 0

        self.reloading: bool = False
        self.bullets: list[Bullet] = []
        self.bullet_speed: float = bullet_speed

    """
    Metoda pozwala na sprawdzenie czy przeciwnik 'widzi' podany jako argument obiekt 
    Parametry jakie trzeba podać to:
    - szukany obiekt (instancja klasy GameObject)
    - lista wszystkich obiektów które 'są materialne' (zasłaniają widoczność), 
      podane jako lista obiektów dziedziczących po GameObject
    """
    def search(self, dron: GameObject, objects: list[GameObject]) -> bool:
        start_pos = self.rect.center
        end_pos = dron.rect.center

        for obj in objects:
            if obj == self or obj == dron:
                continue

            if obj.rect.clipline(start_pos, end_pos):
                return False

        return True

    """
    Jeśli działo jest przeładowanie i cel wykryty to strzela.
    """
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

    """
    Przeładowuje broń przeciwnika co określony czas (reload time).
    """
    def reload(self) -> None:
        if self.reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.reload_timer >= self.reload_time:
                self.reloading = False

    """
    Oblicza nachylenie.
    """
    @staticmethod
    def tilt(dist: Vector2) -> float:
        angle_rad = atan2(dist.y, dist.x)
        angle_deg = degrees(angle_rad)

        return  -angle_deg

    """
    Aktualizuje pozycję pocisków i obsługuje kolizje.
    Usuwa pociski, które trafiły w przeszkodę, drona lub wyleciały poza ekran.
    """
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

Klasa dziedziczy po GameObject
"""
class Bullet(GameObject):
    def __init__(self, x: float, y: float, angle: float, speed: float) -> None:
        super().__init__(x, y, 10, 10, ObjectType.BULLET)
        self.speed = speed
        self.angle = angle
        self.velocity: Vector2 = self.calculate_velocity_from_angle()

    """
    Oblicza składowe wektora prędkości X i Y na podstawie kąta dopasowanego do Pygame
    oraz zadanej prędkości (speed).
    """
    def calculate_velocity_from_angle(self) -> Vector2:
        standard_angle_deg = -self.angle
        angle_rad = radians(standard_angle_deg)
        vel_x = cos(angle_rad) * self.speed
        vel_y = sin(angle_rad) * self.speed
        return Vector2(vel_x, vel_y)

    """
    Aktualizuje pozycję obiektu na podstawie jego prędkości.
    """
    def update_pos(self) -> None:
        self.pos += self.velocity

"""
Klasa Rotora przeznaczona do użytku w klasie Drone.
"""
class Rotor:
    def __init__(self, offset_x: float, x_pos ,y_pos, size: int = 6):
        self.offset: float = offset_x   # odległość od środka drona (dodatnia w prawo, ujemna w lewo)
        self.force: float = 0.0            # siła ciągu (zawsze >= 0)
        self.size: int = size
        self.x = x_pos                #pozycja silnika
        self.y = y_pos
        self.max_force = 10

    """
    Ustawianie wartości w podanych przedziałach.
    """
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