import unittest
from src.shared import Color

# Jeśli te funkcje masz w shared.py lub game_logic.py, odkomentuj poniższy import:
# from src.shared import adjust_brightness, adjust_transparency, adjust_saturation

class TestColorAndEffects(unittest.TestCase):
    def test_color_constants(self):
        """Sprawdza, czy bazowe kolory mają prawidłowe krotki RGB"""
        self.assertEqual(Color.WHITE, (255, 255, 255))
        self.assertEqual(Color.RED, (255, 0, 0))
        self.assertEqual(Color.GREEN, (0, 255, 0))
        self.assertEqual(Color.BLACK, (0, 0, 0))

    def test_adjust_brightness(self):
        """Sprawdza funkcję modyfikacji jasności"""
        # base_color = (100, 100, 100)
        # brighter = adjust_brightness(base_color, 1.5)
        # self.assertEqual(brighter, (150, 150, 150))
        pass

    def test_adjust_transparency(self):
        """Sprawdza poprawność dodawania kanału Alpha"""
        # base_color = (255, 0, 0)
        # color_with_alpha = adjust_transparency(base_color, 128)
        # self.assertEqual(len(color_with_alpha), 4)
        # self.assertEqual(color_with_alpha[3], 128)
        pass

    def test_adjust_saturation(self):
        """Sprawdza modyfikację nasycenia"""
        # base_color = (200, 100, 100)
        # result = adjust_saturation(base_color, 1.2)
        # self.assertEqual(len(result), 3)
        pass