import unittest
import pygame
import os
from src.window import Camera
from src.shared import GameObject, ObjectType, Vector2


class TestCamera(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.camera = Camera(screen_width=1280, screen_height=720, look_ahead=15.0)

    def test_camera_initialization(self):
        """Sprawdza stan początkowy kamery."""
        self.assertEqual(self.camera.offset.x, 0)
        self.assertEqual(self.camera.offset.y, 0)
        self.assertEqual(self.camera.zoom_level, 1.0)
        self.assertEqual(self.camera.width, 1280)

    def test_camera_apply(self):
        """Sprawdza, czy kamera poprawnie aplikuje przesunięcie na obiekt."""
        self.camera.offset = Vector2(100, 100)

        # Obiekt testowy używający zaktualizowanej klasy GameObject (z pos.x, pos.y)
        obj = GameObject(x=150, y=150, width=50, height=50, object_type=ObjectType.DRONE)

        rect = self.camera.apply(obj)

        self.assertIsInstance(rect, pygame.Rect)
        self.assertEqual(rect.width, 50)
        self.assertEqual(rect.height, 50)