import pygame
import math
from shared import GameObject, ObjectType, Vector2

from math import atan2, degrees
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
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity: float = 500
        self.score: int = 0
        self.health = self.HEALTH
        self.lives = self.LIVES
        #self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.img: pygame.image = None
        #silnik lewy i prawy
        self.right_rotor = Rotor(width/2, x + width/2, y)
        self.left_rotor = Rotor(-width/2, x - width/2, y)
        #obsluga silnika i obrotu drona
        self.angular_velocity: float = 0.0          #w rad/s
        self.inertia: float = 10   #moment bezwladnosci (mozna zmienic w zaleznosci od potrzeb)
        self.mass = 0.1 #nalezy zmenic
        #możliwosc ustawienia maksymalnego kata wychylenia w radianach (None jesli moze byc dowolny)
        self.max_angle = None

    def update_physics(self, dt: float):
        torque = self.right_rotor.force * self.right_rotor.offset + self.left_rotor.force * self.left_rotor.offset
        total_lift = self.right_rotor.force + self.left_rotor.force

        k = 10
        ax = k *(math.sin(self.angle) * total_lift) / self.mass
        ay = k * (-math.cos(self.angle) * total_lift) / self.mass + self.gravity

        #opor powietrza
        self.velocity_x *= 0.99
        self.angular_velocity *= 0.90

        self.velocity_x += ax * dt
        self.velocity_y += ay * dt

        angular_acc = torque / self.inertia
        self.angular_velocity += angular_acc * dt
        self.angle += self.angular_velocity * dt

        if self.max_angle != None:
            self.angle = max(-self.max_angle, min(self.max_angle, self.angle))
            self.angle += self.angular_velocity * dt

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt



    def create_image(self, file_dir: str) -> None:
        self.img = create_image_function(file_dir, self.width, self.height)

    def create_image_original(self, file_dir: str) -> None:
        self.img, self.width, self.height = create_image_original_function(file_dir)

    def copy_image(self, image: pygame.Surface) -> None:
        self.img = copy_image_function(image, self.width, self.height)

    def copy_image_original(self, image: pygame.Surface) -> None:
        self.img, self.width, self.height = copy_image_original_function(image)

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
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
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
    def __init__(self, x: float = 0, y: float = 0, width: float = 60, height: float = 40) -> None:
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
    def __init__(self, x: float = 0, y: float = 0, reload_time: int=3000) -> None:
        super().__init__(x, y, 50, 50, ObjectType.ENEMY)
        self.angle: float = 0
        #czas w milisekundach
        self.reload_time: int = reload_time
        self.reload_timer: float = 0

        self.reloading: bool = False
        self.bullets: list[Bullet] = []

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
"""

def create_image_function(file_dir: str, width: float, height: float) -> pygame.Surface:
    original_img = pygame.image.load(file_dir).convert_alpha()
    img = pygame.transform.scale(original_img, (width, height))
    return img


def create_image_original_function(file_dir: str) -> tuple[pygame.Surface, float, float]:
    img = pygame.image.load(file_dir).convert_alpha()
    return img, img.get_width(), img.get_height()


def copy_image_function(image: pygame.Surface, width: float, height: float) -> pygame.Surface:
    img = pygame.transform.scale(image, (width, height))
    return img


def copy_image_original_function(image: pygame.Surface) -> tuple[pygame.Surface, float, float]:
    return image, image.get_width(), image.get_height()
"""
--------/tilt/--------
Oblicza nachylenie z prędkości pocisku.
"""
class Bullet(GameObject):
    def __init__(self, x: float = 0, y: float = 0, vel_x: float=0, vel_y: float=0) -> None:
        super().__init__(x, y, 10, 10, ObjectType.BULLET)
        self.velocity: Vector2 = Vector2(vel_x, vel_y)
        self.angle: float = 0
        self.tilt()

    """
    Oblicza nachylenie z prędkości pocisku.
    """
    def tilt(self):
        if self.velocity.x == 0 and self.velocity.y == 0:
            return

        original_img = pygame.image.load(file_dir)
        scaled_img = pygame.transform.scale(original_img,(width, height))
        self.img = scaled_img
        self.rect = scaled_img.get_rect()

class Rotor:
    def __init__(self, offset_x: float, x_pos ,y_pos, size: int = 6):
        self.offset: float = offset_x   # odległość od środka drona (dodatnia w prawo, ujemna w lewo)
        self.force: float = 0.0            # siła ciągu (zawsze >= 0)
        self.size: int = size
        self.x = x_pos                #pozycja silnika
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