from itertools import combinations
from models.game import Game
from collections import Counter


class Solver:
    def __init__(self, game: Game):
        self.game = game

    def _is_pair(self, combo):
        return combo[0] == combo[1]

    def _is_chow(self, combo):
        try:
            combo = sorted(combo, key=lambda t: t.name)
            houses = [tile.name.split("_")[0] for tile in combo]
            values = [int(tile.name.split("_")[-1]) for tile in combo]
            return (list(Counter(houses).values())[0] == 3) and sorted(values) == list(
                range(min(values), max(values) + 1)
            )
        except:
            return False

    def _is_pong(self, combo):
        return list(Counter(combo).values())[0] == 3

    def compute_victory_distance(self):
        related_tiles = set()

        for combo in combinations(self.game.player_hand_up, 3):
            if self._is_pong(combo):
                print("Pong:", ", ".join([tile.name for tile in combo]))
                related_tiles |= set(combo)
            elif self._is_chow(combo):
                print("Chow:", ", ".join([tile.name for tile in combo]))
                related_tiles |= set(combo)

        for combo in combinations(self.game.player_hand_up, 2):
            if self._is_pair(combo):
                print("Pair:", ", ".join([tile.name for tile in combo]))
                related_tiles |= set(combo)

        stray_tiles = [
            tile.name for tile in set(self.game.player_hand_up) - related_tiles
        ]
        print("Stray tiles:", ", ".join(stray_tiles))
        print()

    def solve(self):
        pass
        self.game.player_hand_up
