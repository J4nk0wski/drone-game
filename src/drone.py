import pygame

from shared import GameObject, ObjectType, Vector2

from math import atan2, degrees, radians, sin, cos
"""
klasa drona którym można sterować

Stałe klasowe:
- HEALTH - zdrowie = 100
- LIVES - życia = 3

Atrybuty:
- x - pozycja (lewy górny róg) w poziomie (float)
- y - pozycja (lewy górny róg) w pionie (float)
- width - szerokość obiektu (float)
- height - wysokość obiektu (float)
- rect - Rect drona
- object_type - rodzaj obiektu w grze (Enum)
- destroyed - zmienna określająca czy obiekt jest zniszczony (bool)
- angle - przechylenie drona (początkowo 0)
- velocity - prędkości w kierynkach poziomym i pionowym wyrażone jako wektor (Vector2)
- gravity - wartość grawitacji drona
- front_rotor_force - siła przedniego rotora (początkowo 0)
- back_rotor_force - siła tylniego rotora (początkowo 0) 
- score - zdobyte punkty (początkowo 0)
- img - grafika drona
- health - zdrowie
- lives - życia

--------/create_image/--------
pobiera z pliku grafikę drona i dostosowywuje do wymiarów drona

--------/create_image_original/--------
pobiera z pliku grafikę drona i zachowuje oryginalny rozmiar grafiki, nadpisuje rozmiary drona
pobiera z pliku grafikę i dostosowywuje do wymiarów klasowych

--------/create_image_original/--------
pobiera z pliku grafikę i zachowuje oryginalny rozmiar grafiki, nadpisuje wyzmiary klasowe

--------/copy_image/--------
dostosowywuje do wymiarów grafikę i zapisuje ją jako swój atrybut

--------/copy_image_original/--------
zapisuje jako swój atrybut oryginalną grafikę i zmienia swoje wymiary na wymiary grafiki

--------/health_check/--------
jeśli zdrowie <= 0 zabiera życie i regeneruje zdrowie 
jeśli brak żyć dron.destroyed = True
"""
class Drone(GameObject):
    HEALTH = 100
    LIVES = 3
    
    def __init__(self, x: float=0, y: float=0, width: float=60, height: float=40) -> None:
        super().__init__(x, y, width, height, ObjectType.DRONE)
        self.destroyed: bool = False
        self.angle: float = 0
        self.velocity: Vector2 = Vector2(0, 0)
        self.gravity: float = 0
        self.front_rotor_force: float = 0
        self.back_rotor_force: float = 0
        self.score: int = 0
        self.health = self.HEALTH
        self.lives = self.LIVES

    def health_check(self) -> None:
        if self.health <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.destroyed = True
            self.health = self.HEALTH
    """
    Przywraca parametry drona do stanu początkowego
    Metoda przyjmuje pozycję początkową (inaczej x=0, y=0)
    """
    def reset(self, start_x: float=0, start_y: float=0) -> None:
        self.x = start_x
        self.y = start_y
        self.velocity = Vector2(0, 0)
        self.gravity = 0
        self.front_rotor_force = 0
        self.back_rotor_force = 0
        self.score = 0
        self.health = self.HEALTH
        self.lives = self.LIVES
        
"""
Klasa podłogi. Teraz bardzo uboga, ale z czasem można dodać mechaniki specjalne dla podłogi.
Atrybuty/gettery:
- x - pozycja (lewy górny róg) w poziomie (float)
- y - pozycja (lewy górny róg) w pionie (float)
- width - szerokość obiektu (float)
- height - wysokość obiektu (float)
- rect - Rect podłogi (pygame.Rect)
- left - pozycja lewego boku (float)
- right - pozycja prawego boku (float)
- top - pozycja górnej krawędzi (float)
- bottom - pozycja dolnej krawędzi (float)
- center_x - środek w poziomie (float)
- center_y - środek w pionie (float)
- center - środek (Vector2)
- img - grafika podłogi (pygame.Surface)

--------/create_image/--------
pobiera z pliku grafikę i dostosowywuje do wymiarów klasowych

--------/create_image_original/--------
pobiera z pliku grafikę i zachowuje oryginalny rozmiar grafiki, nadpisuje wyzmiary klasowe

--------/copy_image/--------
dostosowywuje do wymiarów grafikę i zapisuje ją jako swój atrybut

--------/copy_image_original/--------
zapisuje jako swój atrybut oryginalną grafikę i zmienia swoje wymiary na wymiary grafiki
"""
class Floor(GameObject):
    def __init__(self, x: float=0, y: float=0, width: float=60, height: float=40) -> None:
        super().__init__(x, y, width, height, ObjectType.FLOOR)

"""
Klasa ściany. Teraz bardzo uboga, ale z czasem można dodać mechaniki specjalne dla ściany.
Atrybuty/gettery:
- x - pozycja (lewy górny róg) w poziomie (float)
- y - pozycja (lewy górny róg) w pionie (float)
- width - szerokość obiektu (float)
- height - wysokość obiektu (float)
- rect - Rect podłogi (pygame.Rect)
- left - pozycja lewego boku (float)
- right - pozycja prawego boku (float)
- top - pozycja górnej krawędzi (float)
- bottom - pozycja dolnej krawędzi (float)
- center_x - środek w poziomie (float)
- center_y - środek w pionie (float)
- center - środek (Vector2)
- img - grafika ściany (pygame.Surface)

--------/create_image/--------
pobiera z pliku grafikę i dostosowywuje do wymiarów klasowych

--------/create_image_original/--------
pobiera z pliku grafikę i zachowuje oryginalny rozmiar grafiki, nadpisuje wyzmiary klasowe

--------/copy_image/--------
dostosowywuje do wymiarów grafikę i zapisuje ją jako swój atrybut

--------/copy_image_original/--------
zapisuje jako swój atrybut oryginalną grafikę i zmienia swoje wymiary na wymiary grafiki
"""
class Wall(GameObject):
    def __init__(self, x: float=0, y: float=0, width: float=60, height: float=40) -> None:
        super().__init__(x, y, width, height, ObjectType.WALL)

"""
Klasa przeszkody.
Atrybuty/gettery:
- x - pozycja (lewy górny róg) w poziomie (float)
- y - pozycja (lewy górny róg) w pionie (float)
- width - szerokość obiektu (float)
- height - wysokość obiektu (float)
- rect - Rect podłogi (pygame.Rect)
- left - pozycja lewego boku (float)
- right - pozycja prawego boku (float)
- top - pozycja górnej krawędzi (float)
- bottom - pozycja dolnej krawędzi (float)
- center_x - środek w poziomie (float)
- center_y - środek w pionie (float)
- center - środek (Vector2)
- img - grafika przeszkody (pygame.Surface)
- angle - kąt nachylenia (float)

--------/create_image/--------
pobiera z pliku grafikę i dostosowywuje do wymiarów klasowych

--------/create_image_original/--------
pobiera z pliku grafikę i zachowuje oryginalny rozmiar grafiki, nadpisuje wyzmiary klasowe

--------/copy_image/--------
dostosowywuje do wymiarów grafikę i zapisuje ją jako swój atrybut

--------/copy_image_original/--------
zapisuje jako swój atrybut oryginalną grafikę i zmienia swoje wymiary na wymiary grafiki
"""
class Obstacle(GameObject):
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
        super().__init__(x, y, width, height, ObjectType.OBSTACLE)
        self.angle: float = 0

"""
Klasa przeciwnika, który strzela do gracza i przy trafieniu pociskiem zabiera punkty HP

--------/create_image/--------
pobiera z pliku grafikę drona i dostosowywuje do wymiarów drona

--------/create_image_original/--------
pobiera z pliku grafikę drona i zachowuje oryginalny rozmiar grafiki, nadpisuje rozmiary drona
pobiera z pliku grafikę i dostosowywuje do wymiarów klasowych

--------/create_image_original/--------
pobiera z pliku grafikę i zachowuje oryginalny rozmiar grafiki, nadpisuje wyzmiary klasowe

--------/copy_image/--------
dostosowywuje do wymiarów grafikę i zapisuje ją jako swój atrybut

--------/copy_image_original/--------
zapisuje jako swój atrybut oryginalną grafikę i zmienia swoje wymiary na wymiary grafiki
"""
class Enemy(GameObject):
    def __init__(self, x: float = 0, y: float = 0, reload_time: int=3000, bullet_speed: float=7) -> None:
        super().__init__(x, y, 50, 50, ObjectType.ENEMY)
        self.angle: float = 0
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


    def shoot(self, dron: GameObject, objects: list[GameObject]):
        if not self.reloading and self.search(dron, objects):
            self.reload_timer = pygame.time.get_ticks()
            self.reloading = True
            #TO DO strzelanie pociskiem
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

    def update_bullets(self, dron: Drone, objects: list[GameObject], screen_width: int = 800, screen_height: int = 600) -> None:
        """
        Aktualizuje pozycję pocisków i obsługuje kolizje.
        Usuwa pociski, które trafiły w przeszkodę, drona lub wyleciały poza ekran.
        """
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

            if (bullet.x < 0 or bullet.x > screen_width or
                    bullet.y < 0 or bullet.y > screen_height):
                hit_something = True

            if hit_something:
                self.bullets.remove(bullet)

"""
Klasa pocisku, króry znika po trafieniu w przeszkodę.

--------/create_image/--------
pobiera z pliku grafikę drona i dostosowywuje do wymiarów drona

--------/create_image_original/--------
pobiera z pliku grafikę drona i zachowuje oryginalny rozmiar grafiki, nadpisuje rozmiary drona
pobiera z pliku grafikę i dostosowywuje do wymiarów klasowych

--------/create_image_original/--------
pobiera z pliku grafikę i zachowuje oryginalny rozmiar grafiki, nadpisuje wyzmiary klasowe

--------/copy_image/--------
dostosowywuje do wymiarów grafikę i zapisuje ją jako swój atrybut

--------/copy_image_original/--------
zapisuje jako swój atrybut oryginalną grafikę i zmienia swoje wymiary na wymiary grafiki

--------/tilt/--------
Oblicza nachylenie z prędkości pocisku.
"""
class Bullet(GameObject):
    def __init__(self, x: float, y: float, angle: float, speed: float) -> None:
        super().__init__(x, y, 10, 10, ObjectType.BULLET)
        self.speed = speed
        self.angle: float = angle
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
        self.x += self.velocity.x
        self.y += self.velocity.y

