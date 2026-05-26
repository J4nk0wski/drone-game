import unittest
from src.shared import GameObject, ObjectType
from src.game_logic import check_collision


class TestCheckCollision(unittest.TestCase):
    def test_collision_true(self):
        """Sprawdza przypadek, w którym dwa obiekty na siebie nachodzą."""
        obj1 = GameObject(x=0, y=0, width=50, height=50, object_type=ObjectType.DRONE)
        obj2 = GameObject(x=25, y=25, width=50, height=50, object_type=ObjectType.WALL)

        result = check_collision(obj1, obj2)

        self.assertTrue(result.collision)

    def test_collision_false(self):
        """Sprawdza przypadek, w którym obiekty się nie dotykają."""
        obj1 = GameObject(x=0, y=0, width=50, height=50, object_type=ObjectType.DRONE)
        obj2 = GameObject(x=100, y=100, width=50, height=50, object_type=ObjectType.WALL)

        result = check_collision(obj1, obj2)

        self.assertFalse(result.collision)