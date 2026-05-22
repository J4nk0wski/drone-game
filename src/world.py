import pygame
from shared import GameObject, ObjectType
from drone import Enemy


class World:
    def __init__(self, tile_size=60):
        self.tile_size = tile_size
        self.obstacles = []
        self.enemies = []
        self.landing_pad = None
        self.start_x = 0
        self.start_y = 0

    def load_level(self, level_map):
        """Czyści poprzedni stan i buduje poziom na podstawie tablicy stringów"""
        self.obstacles.clear()
        self.enemies.clear()
        self.landing_pad = None

        for row_idx, row in enumerate(level_map):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.tile_size
                y = row_idx * self.tile_size

                if tile == "O":
                    self.obstacles.append(
                        GameObject(x=x, y=y, width=self.tile_size, height=self.tile_size,
                                   object_type=ObjectType.OBSTACLE)
                    )
                elif tile == "S":
                    self.start_x = x
                    self.start_y = y
                elif tile == "M":
                    # Strefa lądowania o szerokości 2 kafelków
                    self.landing_pad = GameObject(x=x, y=y + 40, width=self.tile_size * 2, height=20,
                                                  object_type=ObjectType.FLOOR)
                elif tile == "E":
                    #Tworzenie przeciwnika na mapie
                    self.enemies.append(Enemy(x=x, y=y, reload_time=5000))