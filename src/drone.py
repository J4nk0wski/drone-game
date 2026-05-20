import pygame

from .shared import GameObject, ObjectType, Vector2

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
        self.score: int = 0
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.img: pygame.image = None
        #silnik lewy i prawy
        self.right_rotor = Rotor(width/2, x + width/2, y)
        self.left_rotor = Rotor(width/2, x - width/2, y)
        #obsluga silnika i obrotu drona
        self.angular_velocity: float = 0.0          #w rad/s
        self.inertia: float = (width ** 2) / 12.0   #moment bezwladnosci (mozna zmienic w zaleznosci od potrzeb)
    

    def update_physics(self, dt: float):
        torque = self.right_rotor.force * self.right_rotor.offset + self.left_rotor.force * self.left_rotor.offset
        angular_acceleration = torque / self.inertia
        self.angular_velocity += angular_acceleration * dt
        

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

class Rotor:
    def __init__(self, offset_x: float, x_pos ,y_pos, size: int = 6):
        self.offset_x: float = offset   # odległość od środka drona (dodatnia w prawo, ujemna w lewo)
        self.force: float = 0.0            # siła ciągu (zawsze >= 0)
        self.size: int = size
        self.x = x_pos                #pozycja silnika
        self.y = y_pos
 
    def set_force(self, force: float) -> None:
        """Ustawia siłę silnika (nie może być ujemna)."""
        self.force = max(0.0, force)

