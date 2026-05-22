import unittest
import sys
import os

# Poprawka ścieżki, żeby test widział pliki z folderu src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from world import World


class TestWorldLoading(unittest.TestCase):
    def test_load_simple_map(self):
        #Definiujemy miniaturową makietę mapy do testu
        mock_map = [
            "OS",
            "EM"
        ]
        world = World(tile_size=60)
        world.load_level(mock_map)

        #Sprawdzamy czy punkt startowy drona ('S') ustawił się na x=60, y=0
        self.assertEqual(world.start_x, 60)
        self.assertEqual(world.start_y, 0)

        #Sprawdzamy czy poprawnie policzył jedną ścianę ('O') i jednego wroga ('E')
        self.assertEqual(len(world.obstacles), 1)
        self.assertEqual(len(world.enemies), 1)

        #Sprawdzamy czy powstała platforma meta ('M')
        self.assertIsNotNone(world.landing_pad)


if __name__ == '__main__':
    unittest.main()