import pygame

from dataclasses import dataclass

from enum import Enum, auto

from typing import Optional

import math

"""
klasa numeruje strony kolizji

Numeracja:
- NONE - 0
- LEFT - 1
- RIGHT - 2
- TOP - 3
- BOTTOM - 4
"""
class CollisioSide(Enum):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()

"""
klasa numeruje rodzaje obiektów w grze

Numeracja:
- DRONE - 0
- WALL - 1
- FLOOR - 2
- OBSTACLE - 3
"""
class ObjectType(Enum):
    DRONE = auto()
    WALL = auto()
    FLOOR = auto()
    OBSTACLE = auto()

"""
klasa Vector2 reprezentuje wektor o dwóch współżędnych

Atrybuty:
- x - położenie w poziomie (float)
- y - położenie w pionie (float)

Metody:
- lenght - zwraca długość wektora (float)
"""
@dataclass
class Vector2:
    x: float
    y: float

    def lenght(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
"""
klasa obiektu grywalnego

Atrubuty:
- x - pozycja (lewy górny róg) w poziomie (float)
- y - pozycja (lewy górny róg) w pionie (float)
- width - szerokość obiektu (float)
- height - wysokość obiektu (float)
- object_type - rodzaj obiektu w grze (Enum)

Metody/gettery:
- right - zwraca współżędną x prawego boku
- left - zwraca współżędną x lewego boku
- top - zwraca współżędną y górnego boku
- bottom - zwraca współżędną y dolnego boku
- center_x - zwraca współżędną x środka obiektu
- center_y zwraca współżędną y środka obiektu
- center - zwraca współżędne środka w postaci wektora (x, y)
"""
@dataclass
class GameObject:
    x: float
    y: float
    width: float
    height: float
    object_type: ObjectType

    @property
    def left(self):
        return self.x
    
    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y
    
    @property
    def bottom(self):
        return self.y + self.height
    
    @property
    def center_x(self):
        return self.x + self.width / 2
    
    @property
    def center_y(self):
        return self.y + self.height / 2

    @property
    def center(self):
        return (self.center_x, self.center_y)

"""
klasa drona którym można sterować

Atrybuty:
- x - pozycja (lewy górny róg) w poziomie (float)
- y - pozycja (lewy górny róg) w pionie (float)
- width - szerokość obiektu (float)
- height - wysokość obiektu (float)
- object_type - rodzaj obiektu w grze (Enum)
- destroyed - zmienna określająca czy obiekt jest zniszczony (bool)
- angle - przechylenie drona (początkowo 0)
- position - przechowuje pozycję obiektu w dwóch wymiarach (Vector2)
- velocity - prędkości w kierynkach poziomym i pionowym wyrażone jako wektor (Vector2)
- gravity - wartość grawitacji drona
- front_rotor_force - siła przedniego rotora (początkowo 0)
- back_rotor_force - siła tylniego rotora (początkowo 0) 
- score - zdobyte punkty (początkowo 0)

"""
class Drone(GameObject):
    STABILIZATION = 0.95

    def __init__(self, x: float, y: float, width: float=60, height: float=40, file_dir: str=None):
        super().__init__(x, y, width, height, ObjectType.DRONE)
        self.destroyed: bool = False
        self.angle: float = 0
        self.position: Vector2 = Vector2(x, y)
        self.velocity: Vector2 = Vector2(0, 0)
        self.gravity: float = 0
        self.front_rotor_force: float = 0
        self.back_rotor_force: float = 0
        self.score: int = 0
        try:
            self.image: pygame.image = pygame.image.load(file_dir)
        except:
            self.image: pygame.image = None

    def update(self, dt: float):
        if self.destroyed: 
            return
        
        self.angle += (self.front_rotor_force - self.back_rotor_force) * (1 - self.STABILIZATION)
        self.angle *= self.STABILIZATION

        total_lift = self.front_rotor_force + self.back_rotor_force

        rad = math.radians(self.angle)
        accel_x = total_lift * math.sin(rad) * 2.0
        accel_y = self.gravity - (total_lift * math.cos(rad))

        self.velocity.x += accel_x * dt
        self.velocity.y += accel_y * dt
        
        self.velocity.x *= 0.99
        self.velocity.y *= 0.99

        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt


"""
klasa przechowuje dane kolizji

Atrybuty:
- collision - czy wystąpiła kolizja (bool)
- obj - obiekt z jakim wystąpiła kolizja (pygame.Rect)
- side - strona którą obiekt główny, np. dron uderzył w przeszkodę (str:("right", "left", "top", "bottom"))
- vx - prędkość pozioma uderzenia
- vy - prędkość pionowa uderzenia

danych obiektu klasy CollisionInfo nie można zmienić (konwencja)
"""
class CollisionInfo:
    def __init__(self, collision: bool=False, obj: pygame.Rect=None, side=None, vx=0, vy=0):
        self._collision = collision
        self._obj = obj
        self._side = side
        self._vx = vx
        self._vy = vy

    @property
    def collision(self):
        return self._collision
    
    @property
    def obj(self):
        return self._obj
    
    @property
    def side(self):
        return self._side
    
    @property
    def vx(self):
        return self._vx
    
    @property
    def vy(self):
        return self._vy
    
def check_collision(main_obj: pygame.Rect, obstacle: pygame.Rect) -> CollisionInfo:

    if not main_obj.colliderect(obstacle):
        return CollisionInfo(obj=obstacle)
    


