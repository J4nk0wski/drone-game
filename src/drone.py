import pygame

from shared import GameObject, ObjectType, Vector2, adjust_brightness

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

--------/health_check/--------
jeśli zdrowie <= 0 zabiera życie i regeneruje zdrowie 
jeśli brak żyć dron.destroyed = True
zwraca Surface drona
im mniej zdrowia tym bardziej przezroczysty Surface
"""
class Drone(GameObject):
    HEALTH = 100
    LIVES = 3
    
    def __init__(self, x: float=0, y: float=0, width: float=60, height: float=40):
        super().__init__(x, y, width, height, ObjectType.DRONE)
        self.destroyed: bool = False
        self.angle: float = 0
        self.velocity: Vector2 = Vector2(0, 0)
        self.gravity: float = 0
        self.front_rotor_force: float = 0
        self.back_rotor_force: float = 0
        self.score: int = 0
        self.img: pygame.Surface = None
        self.health = self.HEALTH
        self.lives = self.LIVES

    def create_image(self, file_dir: str):
        original_img = pygame.image.load(file_dir).convert_alpha()
        self.width = original_img.width
        self.height = original_img.height
        self.img = pygame.transform.scale(original_img, (self.width, self.height))

    def create_image_original(self, file_dir: str):
        self.img = pygame.image.load(file_dir).convert_alpha()
        self.width = self.img.width
        self.height = self.img.height

    def health_check(self) -> pygame.Surface:
        if self.health <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.destroyed = True
            self.health = self.HEALTH

        if self.img == None:
            return None
        
        match self.health:
            case x if x >= self.HEALTH * 0.75:
                temp_img = self.img.copy()
                return temp_img.convert_alpha(255)
            
            case x if x >= self.HEALTH * 0.5:
                temp_img = self.img.copy()
                return temp_img.convert_alpha(192)
            
            case x if x >= self.HEALTH * 0.25:
                temp_img = self.img.copy()
                return temp_img.convert_alpha(128)
            
            case x if x >= 0:
                temp_img = self.img.copy()
                return temp_img.convert_alpha(64)

        
