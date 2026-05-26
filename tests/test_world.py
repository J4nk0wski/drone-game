import unittest
import sys
import os

# Poprawka ścieżki, żeby test widział pliki z folderu src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

#Importujemy też słownik LEVELS, żeby móc na nim operować
from world import World, LEVELS


class TestWorldLoading(unittest.TestCase):
    def test_load_simple_map(self):
        # Definiujemy miniaturową makietę mapy do testu
        mock_map = [
            "OS",
            "EM"
        ]
        LEVELS[999] = mock_map

        world = World(tile_size=60)

        # Przekazujemy ID poziomu, tak jak wymaga tego nowa funkcja
        world.load_level(999)

        # Sprawdzamy czy punkt startowy drona ustawił się na x=60, y=0
        self.assertEqual(world.start_x, 60)
        self.assertEqual(world.start_y, 0)

        # Sprawdzamy czy poprawnie policzył jedną ścianę ('O') i jednego wroga ('E')
        self.assertEqual(len(world.obstacles), 1)
        self.assertEqual(len(world.enemies), 1)

        # Sprawdzamy czy powstała platforma meta ('M')
        self.assertIsNotNone(world.landing_pad)

        # Sprzątamy po teście, żeby nie zostawiać śmieci w globalnym słowniku
        del LEVELS[999]


if __name__ == '__main__':
    unittest.main()