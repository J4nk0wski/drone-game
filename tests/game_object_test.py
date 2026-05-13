import unittest
import pygame
import os
from src.drone import Drone, Floor, Obstacle
from src.shared import Vector2, ObjectType


class TestDroneLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        # Tworzymy mały ekran w trybie bez okna (dummy video driver),
        # aby testy mogły działać na serwerach bez monitora
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.display.set_mode((1, 1))

    def setUp(self):
        """Przygotowanie świeżego obiektu drona przed każdym testem."""
        self.drone = Drone(x=100, y=100, width=50, height=30)

    def test_initialization(self):
        """Sprawdza czy dron inicjalizuje się z poprawnymi wartościami."""
        self.assertEqual(self.drone.x, 100)
        self.assertEqual(self.drone.y, 100)
        self.assertEqual(self.drone.health, Drone.HEALTH)
        self.assertEqual(self.drone.lives, Drone.LIVES)
        self.assertFalse(self.drone.destroyed)
        self.assertEqual(self.drone.object_type, ObjectType.DRONE)

    def test_health_check_regeneration(self):
        """Testuje system utraty życia i regeneracji zdrowia."""
        self.drone.health = 0
        self.drone.health_check()

        self.assertEqual(self.drone.lives, Drone.LIVES - 1)
        self.assertEqual(self.drone.health, Drone.HEALTH)
        self.assertFalse(self.drone.destroyed)

    def test_drone_destruction(self):
        """Sprawdza czy dron zostaje zniszczony po utracie wszystkich żyć."""
        self.drone.lives = 1
        self.drone.health = 0
        self.drone.health_check()

        self.assertTrue(self.drone.destroyed)
        self.assertEqual(self.drone.lives, 0)

    def test_copy_image_scaling(self):
        """Testuje czy metoda copy_image poprawnie przypisuje Surface."""
        test_surface = pygame.Surface((100, 100))
        self.drone.copy_image(test_surface)

        self.assertIsNotNone(self.drone.img)
        # Sprawdzenie czy przeskalowano do wymiarów drona (50x30)
        self.assertEqual(self.drone.img.get_width(), 50)
        self.assertEqual(self.drone.img.get_height(), 30)

    def test_copy_image_original(self):
        """Testuje czy metoda copy_image_original zmienia wymiary obiektu."""
        original_width, original_height = 120, 80
        test_surface = pygame.Surface((original_width, original_height))

        self.drone.copy_image_original(test_surface)

        self.assertEqual(self.drone.width, original_width)
        self.assertEqual(self.drone.height, original_height)
        self.assertEqual(self.drone.img.get_width(), original_width)


class TestEnvironmentObjects(unittest.TestCase):
    def test_floor_initialization(self):
        floor = Floor(x=0, y=500, width=800, height=50)
        self.assertEqual(floor.object_type, ObjectType.FLOOR)
        self.assertEqual(floor.rect.top, 500)

    def test_obstacle_angle(self):
        obs = Obstacle(x=200, y=200)
        self.assertEqual(obs.angle, 0)
        obs.angle = 45.5
        self.assertEqual(obs.angle, 45.5)


if __name__ == '__main__':
    unittest.main()