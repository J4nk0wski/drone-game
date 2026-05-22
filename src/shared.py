import pygame

from dataclasses import dataclass

from enum import Enum, auto

from typing import Optional

"""
klasa numeruje strony kolizji

Numeracja:
- NONE - 1
- LEFT - 2
- RIGHT - 3
- TOP - 4
- BOTTOM - 5
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
- DRONE - 1
- WALL - 2
- FLOOR - 3
- OBSTACLE - 4
"""
class ObjectType(Enum):
    DRONE = auto()
    WALL = auto()
    FLOOR = auto()
    OBSTACLE = auto()
    ENEMY = auto()
    BULLET = auto()

    def __eq__(self, other) -> bool:
        return self.value == other.value

"""
klasa Vector2 reprezentuje wektor o dwóch współżędnych

Atrybuty:
- x - położenie w poziomie (float)
- y - położenie w pionie (float)

Metody:
- length - zwraca długość wektora (float)

Przeciążone operatory:
- dodawanie
- negacja
- odejmowanie
"""
@dataclass
class Vector2:
    x: float
    y: float
    
    def __add__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __sub__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return self + (-other)

    def length(self) -> float:
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
class GameObject:
    def __init__(self, x: float, y: float, width: float, height: float, object_type: ObjectType):
        self.pos: Vector2 = Vector2(x, y)
        self.width: float = width
        self.height: float = height
        self.object_type: ObjectType = object_type
        self.velocity: Vector2 = Vector2(0, 0)
        self.gravity: float = 0
        self.angular_velocity: float = 0
        self.inertia: float = 0
        self.mass: float = 0
        self.angle: float= 0
        self.max_angle: float| None = None
        self.img: pygame.Surface | None = None

    @property
    def rect(self): return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    @property
    def left(self):
        return self.pos.x
    
    @property
    def right(self):
        return self.pos.x + self.width

    @property
    def top(self):
        return self.pos.y
    
    @property
    def bottom(self):
        return self.pos.y + self.height
    
    @property
    def center_x(self):
        return self.pos.x + self.width / 2
    
    @property
    def center_y(self):
        return self.pos.y + self.height / 2

    @property
    def center(self):
        return Vector2(self.center_x, self.center_y)

    def create_image(self, file_dir: str) -> None:
        original_img = pygame.image.load(file_dir).convert_alpha()
        self.img = pygame.transform.scale(original_img, (int(self.width), int(self.height)))

    def create_image_original(self, file_dir: str) -> None:
        img = pygame.image.load(file_dir).convert_alpha()
        self.img = img
        self.width, self.height = img.get_size()

    def copy_image(self, image: pygame.Surface) -> None:
        self.img = pygame.transform.scale(image, (int(self.width), int(self.height)))


    def copy_image_original(self, image: pygame.Surface) -> None:
        self.img = image
        self.width, self.height = image.get_size()

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
klasa upraszczająca dostęp do kolorów zamiast każdorazowo testować 
wartości barw ta klasa ma nazwane kolory

jeśli kolor którego potrzebujesz nie znajduje się w klasie śmiało go dodaj
postaraj się zachować podział na kategorie
"""
class Color:
    # --- PODSTAWOWE ---
    WHITE       = pygame.Color(255, 255, 255)
    BLACK       = pygame.Color(0, 0, 0)
    GRAY        = pygame.Color(128, 128, 128)
    LIGHT_GRAY  = pygame.Color(200, 200, 200)
    DARK_GRAY   = pygame.Color(50, 50, 50)

    # --- PALETA BARW (Czyste kolory) ---
    RED         = pygame.Color(255, 0, 0)
    GREEN       = pygame.Color(0, 255, 0)
    BLUE        = pygame.Color(0, 0, 255)
    YELLOW      = pygame.Color(255, 255, 0)
    CYAN        = pygame.Color(0, 255, 255)
    MAGENTA     = pygame.Color(255, 0, 255)
    ORANGE      = pygame.Color(255, 165, 0)
    PURPLE      = pygame.Color(128, 0, 128)

    # --- ATMOSFERYCZNE I NATURA ---
    SKY_BLUE    = pygame.Color(135, 206, 235)
    DEEP_SEA    = pygame.Color(0, 105, 148)
    FOREST_GREEN = pygame.Color(34, 139, 34)
    SAND        = pygame.Color(194, 178, 128)
    BROWN       = pygame.Color(139, 69, 19)

    # --- KOLORY GAME-DESIGN (UI i Efekty) ---
    GOLD        = pygame.Color(255, 215, 0)
    SILVER      = pygame.Color(192, 192, 192)
    BRONZE      = pygame.Color(205, 127, 50)
    CRIMSON     = pygame.Color(220, 20, 60)
    LIME        = pygame.Color(50, 205, 50)
    
    # --- KOLORY RETRO / CYBERPUNK (Neonowe) ---
    NEON_PINK   = pygame.Color(255, 20, 147)
    NEON_GREEN  = pygame.Color(57, 255, 20)
    NEON_BLUE   = pygame.Color(0, 255, 239)
    ELECTRIC_VIOLET = pygame.Color(143, 0, 255)

    # --- PRZEZROCZYSTE (Overlay) ---
    # Ostatnia liczba to kanał Alpha: 0 (niewidoczne) do 255 (pełne)
    SHADOW      = pygame.Color(0, 0, 0, 150)
    HIGHLIGHT   = pygame.Color(255, 255, 255, 100)
    DANGER_ZONE = pygame.Color(255, 0, 0, 80)

    # --- TŁA ---
    BG_DARK     = pygame.Color(20, 20, 25)
    BG_NIGHT    = pygame.Color(10, 10, 40)

"""
funkcja reguluje jasność koloru
Parametry:
- color (pygame.Color) - zmieniany kolor
- amount (float) - wartość jasności (0.8 = 80%)
"""
def adjust_brightness(color: pygame.Color, amount: float) -> pygame.Color:
    new_color = pygame.Color(color.r, color.g, color.b, color.a)
    h, s, l, a = new_color.hsla
    new_color.hsla = (h, s, max(0, min(100, l * amount)), a)
    return new_color

"""
funkcja reguluje przezroczystość koloru
Parametry:
- color (pygame.Color) - zmieniany kolor
- amount (float) - wartość przezroczystości (0.8 = 80%)
"""
def adjust_transparency(color: pygame.Color, amount: float) -> pygame.Color:
    new_color = pygame.Color(color.r, color.g, color.b, color.a)
    h, s, l, a = new_color.hsla
    new_color.hsla = (h, s, l, max(0, min(100, a * amount))) 
    return new_color

"""
funkcja reguluje saturacę koloru
Parametry:
- color (pygame.Color) - zmieniany kolor
- amount (float) - wartość saturację (0.8 = 80%)
"""
def adjust_saturation(color: pygame.Color, amount: float) -> pygame.Color:
    new_color = pygame.Color(color.r, color.g, color.b, color.a)
    h, s, l, a = new_color.hsla
    new_color.hsla = (h, max(0, min(100, s * amount)), l, a) 
    return new_color

