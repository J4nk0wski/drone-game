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
class CollisionSide(Enum):
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
    def rect(self): return pygame.Rect(self.x, self.y, self.width, self.height)

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
- velocity - prędkości w kierynkach poziomym i pionowym wyrażone jako wektor (Vector2)
- gravity - wartość grawitacji drona
- front_rotor_force - siła przedniego rotora (początkowo 0)
- back_rotor_force - siła tylniego rotora (początkowo 0) 
- score - zdobyte punkty (początkowo 0)
- rect - Rect drona
- img - grafika drona
"""
class Drone(GameObject):

    def __init__(self, x: float=0, y: float=0, width: float=60, height: float=40):
        super().__init__(x, y, width, height, ObjectType.DRONE)
        self.destroyed: bool = False
        self.angle: float = 0
        self.velocity: Vector2 = Vector2(0, 0)
        self.gravity: float = 0
        self.front_rotor_force: float = 0
        self.back_rotor_force: float = 0
        self.score: int = 0
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.img: pygame.image = None

    def create_image(self, file_dir: str=None, width: float=None, height: float=None):
        if width == None:
            width = self.width
        else:
            self.width = width

        if height == None:
            height = self.height
        else:
            self.height = height

        if file_dir == None:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            return

        original_img = pygame.image.load(file_dir)
        scaled_img = pygame.transform.scale(original_img,(width, height))
        self.img = scaled_img
        self.rect = scaled_img.get_rect()

"""
klasa przechowuje dane kolizji obiektu dynamicznego ze statycznym
dla klasy drona lub jego pochodnej zwraca dodatkowo prędkość jako pole klasy CollisionInfo

Atrybuty:
- collision - czy nastąpiła kolizja (bool)
- side - strona kolizji (CollisionSide)
- object_hit - przeszkoda z którą zderzył się główny obiekt (GameObject)
- velocity - prędkości głównego obiektu podczas zderzenia (Vector2)
"""
@dataclass
class CollisionInfo:
    collision: bool
    side: CollisionSide
    object_hit: Optional[GameObject]
    velocity: Optional[Vector2]

"""

"""
def check_collision(dynamic: GameObject, static: GameObject) -> CollisionInfo:
    if not dynamic.rect.colliderect(static.rect):
        return CollisionInfo(False, CollisionSide.NONE, None, None)

    d_rect = dynamic.rect
    s_rect = static.rect
    
    overlaps = {
        CollisionSide.TOP: d_rect.bottom - s_rect.top,
        CollisionSide.BOTTOM: s_rect.bottom - d_rect.top,
        CollisionSide.LEFT: d_rect.right - s_rect.left,
        CollisionSide.RIGHT: s_rect.right - d_rect.left,
    }
    side = min(overlaps, key=overlaps.get)
    if isinstance(dynamic, Drone):
        return CollisionInfo(True, side, static, dynamic.velocity)
    return CollisionInfo(True, side, static)


