import pygame

from dataclasses import dataclass

from enum import Enum, auto

from typing import Optional

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
