from collections import Counter
from itertools import chain, combinations

from models.game import Game
from models.tile import Tile


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

    def _counter_contains(self, container: Counter, contained: Counter):
        return all(container[x] >= contained[x] for x in contained)

    def compute_victory_distance(self, hypothesis_tiles=[]):
        hand = self.game.player_hand_up + hypothesis_tiles
        hand_counter = Counter(hand)
        related_tiles = set()
        pongs = []
        chows = []
        pairs = []

        for combo in combinations(hand, 3):
            if self._is_pong(combo):
                related_tiles |= set(combo)
                pongs.append(tuple(combo))
            elif self._is_chow(combo):
                related_tiles |= set(combo)
                chows.append(tuple(combo))

        for combo in combinations(hand, 2):
            if self._is_pair(combo):
                related_tiles |= set(combo)
                pairs.append(tuple(combo))

        print("Possible Pongs:\n")
        for combo in set(pongs):
            print("\t" + " ".join([tile.name for tile in combo]))
        print()

        print("Possible Chows:\n")
        for combo in set(chows):
            print("\t" + " ".join([tile.name for tile in combo]))
        print()

        print("Possible Pairs:\n")
        for combo in set(pairs):
            print("\t" + " ".join([tile.name for tile in combo]))
        print()

        strays = sorted(
            [tile.name for tile in set(hand) - related_tiles],
            key=lambda t: Tile[t].value,
        )

        print("Strays:\n")
        for tile in strays:
            print("\t" + tile)
        print()

        triples = [tuple(combo) for combo in (pongs + chows)]
        doubles = [tuple(combo) for combo in pairs]

        triple_combos = sorted(
            {
                tuple(combo)
                for combo in (
                    list(combinations(triples, 5))
                    + list(combinations(triples, 4))
                    + list(combinations(triples, 3))
                    + list(combinations(triples, 2))
                )
                if self._counter_contains(hand_counter, Counter(chain(*combo)))
            },
            key=lambda combo: -len(combo),
        )

        print(f"Triple Combos ({len(triple_combos)}):\n")
        for combos in triple_combos:
            print(
                "\n".join(
                    [
                        "\t" + " ".join([tile.name for tile in triple])
                        for triple in combos
                    ]
                )
            )
            print()
        print()

        double_combos = sorted(
            {
                tuple(combo)
                for combo in (
                    list(combinations(doubles, 7))
                    + list(combinations(doubles, 6))
                    + list(combinations(doubles, 5))
                    + list(combinations(doubles, 4))
                    + list(combinations(doubles, 3))
                    + list(combinations(doubles, 2))
                )
                if self._counter_contains(hand_counter, Counter(chain(*combo)))
            },
            key=lambda combo: -len(combo),
        )

        print(f"Double Combos ({len(double_combos)}):\n")
        for combos in double_combos:
            print(
                "\n".join(
                    [
                        "\t" + " ".join([tile.name for tile in double])
                        for double in combos
                    ]
                )
            )
            print()
        print()
