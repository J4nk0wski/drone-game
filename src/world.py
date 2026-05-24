from shared import GameObject, ObjectType
from drone import Enemy, Coin  # Dodano import Coin

# Baza wszystkich poziomów w grze
LEVELS = {
    #Przykladowy poziom 1
    1: [
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
        "O                                                                              O",
        "O   S                  C                                                       O",
        "O                                                                              O",
        "O                                      E               C                       O",
        "O                                   OOOOOOO                                    O",
        "O               C                                                              O",
        "O             E                                              E                 O",
        "OOOOOOOOOOOOOOOOOOOOO                                  OOOOOOOOOOOOOOOOOOOOOOOOO",
        "O                                                                              O",
        "O                                C                                       M     O",
        "O                                                                              O",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    ],
    2: [
        # Przykładowy poziom 2
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO",
        "O   S                                                                          O",
        "O                                                                              O",
        "O                               E               E                              O",
        "O                            OOOOOOO         OOOOOOO                           O",
        "O                                                                        M     O",
        "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    ]
}

class World:
    def __init__(self, tile_size=60):
        self.tile_size = tile_size
        self.obstacles = []
        self.enemies = []
        self.coins = []  # Nowa lista przechowująca monety
        self.landing_pad = None
        self.start_x = 0
        self.start_y = 0
        self.current_level = 1

    def load_level(self, level_id):
        """Czyści poprzedni stan i buduje poziom na podstawie ID ze słownika LEVELS"""
        self.obstacles.clear()
        self.enemies.clear()
        self.coins.clear()  # Czyszczenie monet przy ładowaniu nowego poziomu
        self.landing_pad = None
        self.current_level = level_id

        if level_id not in LEVELS:
            print(f"Błąd: Poziom {level_id} nie istnieje w bazie!")
            return

        level_map = LEVELS[level_id]

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
                    # Generowanie wieżyczki UGV
                    self.enemies.append(Enemy(x=x, y=y, reload_time=5000))
                elif tile == "C":
                    # Generowanie monety (przesunięcie +10 żeby wyśrodkować 40x40 w kafelku 60x60)
                    self.coins.append(Coin(x=x + 10, y=y + 10))