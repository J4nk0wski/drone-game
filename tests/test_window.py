import sys
import os
import unittest
 
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
 
import pygame
pygame.init()
 
from window import Window
 
class TestWindowInitialization(unittest.TestCase):
 
    def setUp(self):
        self.window = Window(size=(800, 600), game_name="TestGame")
 
    def test_default_screen_size(self):
        self.assertEqual(self.window.screen_size, (800, 600))
 
    def test_default_background_color_is_white(self):
        self.assertEqual(self.window.color, (255, 255, 255))
 
    def test_default_fps_is_60(self):
        self.assertEqual(self.window.fps, 60)
 
    def test_no_background_image_by_default(self):
        self.assertIsNone(self.window.background_image)
 
    def test_rectangles_list_starts_empty(self):
        self.assertEqual(self.window.rectangles, [])
 
    def test_image_rects_list_starts_empty(self):
        self.assertEqual(self.window.image_rects, [])
 
 
class TestWindowBackgroundColor(unittest.TestCase):
 
    def setUp(self):
        self.window = Window()
 
    def test_change_background_color(self):
        self.window.change_background_color((100, 150, 200))
        self.assertEqual(self.window.color, (100, 150, 200))
 
    def test_render_fills_background_color(self):
        self.window.change_background_color((255, 0, 0))
        self.window.render()
        #sprawdza pixel w srodku ekranu
        color = self.window.screen.get_at((640, 360))
        self.assertEqual(color[:3], (255, 0, 0))
 
    def test_render_default_white_background(self):
        self.window.render()
        color = self.window.screen.get_at((640, 360))
        self.assertEqual(color[:3], (255, 255, 255))
 
 
class TestWindowRectangles(unittest.TestCase):
 
    def setUp(self):
        self.window = Window()
 
    def test_add_rectangle(self):
        rect = pygame.Rect(10, 10, 100, 50)
        self.window.add_rectangle(rect)
        self.assertIn(rect, self.window.rectangles)
 
    def test_add_multiple_rectangles(self):
        rects = [pygame.Rect(i * 10, 0, 50, 50) for i in range(3)]
        for r in rects:
            self.window.add_rectangle(r)
        self.assertEqual(len(self.window.rectangles), 3)
 
    def test_render_draws_rectangle_on_screen(self):
        rect = pygame.Rect(200, 200, 100, 100)
        self.window.add_rectangle(rect)
        self.window.render()
        color = self.window.screen.get_at((250, 250))
        self.assertEqual(color[:3], (105, 194, 245))
 
class TestWindowFPS(unittest.TestCase):
 
    def setUp(self):
        self.window = Window()
 
    def test_set_fps(self):
        self.window.set_fps(30)
        self.assertEqual(self.window.fps, 30)
 
    def test_set_fps_high(self):
        self.window.set_fps(144)
        self.assertEqual(self.window.fps, 144)
 
 
class TestWindowEngineBarClamping(unittest.TestCase):
    def setUp(self):
        self.window = Window()
 
    def test_draw_engine_power_normal(self):
        self.window.render()
        self.window.draw_engine_power(0.5, 0.8)
 
    def test_draw_engine_power_above_max(self):
        self.window.render()
        self.window.draw_engine_power(999, 999)
 
    def test_draw_engine_power_below_min(self):
        self.window.render()
        self.window.draw_engine_power(-1, -5)
 
    def test_draw_engine_power_zero(self):
        self.window.render()
        self.window.draw_engine_power(0, 0)
 
if __name__ == '__main__':
    unittest.main()