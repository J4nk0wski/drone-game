import unittest
import pygame
import os
from src.window import Window


class TestWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicjalizacja środowiska graficznego w trybie wirtualnym."""
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_window_initialization(self):
        """Sprawdza domyślne parametry okna po inicjalizacji."""
        win = Window(size=(1280, 720), game_name="Test Window")

        self.assertEqual(win.screen_size, (1280, 720))
        self.assertEqual(win.fps, 60)
        self.assertIsNotNone(win.screen)

    def test_set_fps(self):
        """Sprawdza funkcję modyfikacji limitu klatek."""
        win = Window(size=(800, 600))
        win.set_fps(120)
        self.assertEqual(win.fps, 120)