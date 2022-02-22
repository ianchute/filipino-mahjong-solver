from collections import Counter
from itertools import chain, combinations, groupby
from typing import List

from models.game import Game
from models.tile import Tile
from time import time
import pandas as pd

CACHE_HITS = 0
TIMES = {}


def benchmark(f):
    def inner(*args, **kwargs):
        t0 = time()
        result = f(*args, **kwargs)
        t = time() - t0
        if f.__name__ not in TIMES:
            TIMES[f.__name__] = 0
        TIMES[f.__name__] += t
        return result

    return inner


def memoize(f):
    def inner(self, combo):
        global CACHE_HITS
        combo = sorted(combo, key=lambda t: t.name)
        key = f"[{f.__name__}] {combo}"
        if key in self.cache:
            CACHE_HITS += 1
            return self.cache[key]
        result = self.cache[key] = f(self, combo)
        return result

    inner.__name__ = f.__name__

    return inner


# def memoize_general(f):
#     def inner(self, *args):
#         global CACHE_HITS
#         key = f"[{f.__name__}] {args}"
#         if key in self.cache:
#             CACHE_HITS += 1
#             return self.cache[key]
#         result = self.cache[key] = f(self, *args)
#         return result

#     inner.__name__ = f.__name__

#     return inner


class Solver:
    cache = {}

    def __init__(self, game: Game):
        self.game = game

    @benchmark
    @memoize
    def _is_pair(self, combo):
        return combo[0] == combo[1]

    @benchmark
    @memoize
    def _is_chow(self, combo):
        try:
            houses = [tile.name.split("_")[0] for tile in combo]
            values = [int(tile.name.split("_")[-1]) for tile in combo]
            return (list(Counter(houses).values())[0] == 3) and sorted(values) == list(
                range(min(values), max(values) + 1)
            )
        except:
            return False

    @benchmark
    @memoize
    def _is_pong(self, combo):
        return len(set(combo)) == 1

    @benchmark
    def _counter_contains(self, container: Counter, contained: Counter):
        return len(contained - container) == 0

    @benchmark
    def _counter_to_tuple(self, counter: Counter):
        result = []
        for k, v in counter.items():
            result += [k] * v
        return tuple(result)

    @benchmark
    def _find_potential_ai_pairs(self, combo, hand_counter: Counter):
        combo_counter = self._counter_chain(combo)
        remaining = self._counter_to_tuple(hand_counter - combo_counter)
        potential_ais, _ = self._find_potential_doubles(remaining)
        return potential_ais

    @benchmark
    def _find_potential_ai_triples(self, combo, hand_counter: Counter):
        combo_counter = self._counter_chain(combo)
        remaining = self._counter_to_tuple(hand_counter - combo_counter)
        pongs, chows, _ = self._find_potential_triples_groupby_house(remaining)
        return pongs + chows

    @benchmark
    def _counter_chain(self, x):
        return Counter(chain(*x))

    @benchmark
    def _generate_triple_combos(self, triples, hand_counter: Counter):
        combos = {
            tuple(combo)
            for combo in chain(
                combinations(triples, 5),
                combinations(triples, 4),
                combinations(triples, 3),
                combinations(triples, 2),
                combinations(triples, 1),
            )
        }
        # print("Possible triple combos:", len(combos))
        combos = sorted(
            [
                combo
                for combo in combos
                if self._counter_contains(hand_counter, self._counter_chain(combo))
            ],
            key=lambda combo: -len(combo),
        )
        return combos

    @benchmark
    def _generate_double_combos(self, doubles, hand_counter: Counter):
        combos = {
            combo
            for combo in chain(
                combinations(doubles, 7),
                combinations(doubles, 6),
                combinations(doubles, 5),
                combinations(doubles, 4),
                combinations(doubles, 3),
                combinations(doubles, 2),
                combinations(doubles, 1),
            )
        }
        combos = sorted(
            [
                tuple(combo)
                for combo in combos
                if self._counter_contains(hand_counter, self._counter_chain(combo))
            ],
            key=lambda combo: -len(combo),
        )
        return combos

    @benchmark
    @memoize
    def _find_potential_triples(self, tiles):
        related_tiles = set()
        pongs = []
        chows = []
        for combo in combinations(tiles, 3):
            if self._is_pong(combo):
                related_tiles |= set(combo)
                pongs.append(tuple(combo))
            elif self._is_chow(combo):
                related_tiles |= set(combo)
                chows.append(tuple(combo))
        return pongs, chows, related_tiles

    @benchmark
    @memoize
    def _find_potential_doubles(self, tiles):
        related_tiles = set()
        pairs = []
        for combo in combinations(tiles, 2):
            if self._is_pair(combo):
                related_tiles |= set(combo)
                pairs.append(tuple(combo))
        return pairs, related_tiles

    @benchmark
    @memoize
    def _find_potential_triples_groupby_house(self, tiles):
        related_tiles = set()
        pongs = []
        chows = []
        for house, group in groupby(tiles, lambda t: t.name.split("_")[0]):
            _pongs, _chows, _related_tiles = self._find_potential_triples(group)
            pongs += _pongs
            chows += _chows
            related_tiles |= _related_tiles
        return pongs, chows, related_tiles

    def _normalize_combo_list(self, combos, hand_counter: Counter):
        normalized = []
        for combo, count in Counter(combos).items():
            max_potential_count = min(hand_counter[tile] for tile in combo)
            normalized += [combo] * min(count, max_potential_count)
        return normalized

    def compute_victory_distance(self, hypothesis_tiles=[], debug=False):
        p = print if debug else lambda *a, **k: None
        hand = self.game.player_hand_up + hypothesis_tiles
        hand = sorted(hand, key=lambda t: t.name)
        hand_counter = Counter(hand)

        (
            pongs,
            chows,
            related_tiles_triples,
        ) = self._find_potential_triples_groupby_house(hand)
        pairs, related_tiles_doubles = self._find_potential_doubles(hand)
        related_tiles = related_tiles_triples | related_tiles_doubles

        p("Possible Pongs:\n")
        for combo in set(pongs):
            p("\t" + " ".join([tile.name for tile in combo]))
        p()

        p("Possible Chows:\n")
        for combo in set(chows):
            p("\t" + " ".join([tile.name for tile in combo]))
        p()

        p("Possible Pairs:\n")
        for combo in set(pairs):
            p("\t" + " ".join([tile.name for tile in combo]))
        p()

        strays = sorted(
            [tile.name for tile in set(hand) - related_tiles],
            key=lambda t: Tile[t].value,
        )

        p("Strays:\n")
        for tile in strays:
            p("\t" + tile)
        p()

        triples = [tuple(combo) for combo in (pongs + chows)]
        triples = self._normalize_combo_list(triples, hand_counter)
        doubles = [tuple(combo) for combo in pairs]
        doubles = self._normalize_combo_list(doubles, hand_counter)

        # print(pd.Series(triples).value_counts())
        # print(pd.Series(doubles).value_counts())

        triple_combos = self._generate_triple_combos(triples, hand_counter)
        triple_combos = list(
            chain(
                *[
                    [
                        tuple(list(combo) + [ai])
                        for ai in self._find_potential_ai_pairs(combo, hand_counter)
                    ]
                    + [combo]
                    for combo in triple_combos
                ]
            )
        )

        p(f"Triple Combos ({len(triple_combos)}):\n")
        for combos in triple_combos:
            p(
                "\n".join(
                    [
                        "\t" + " ".join([tile.name for tile in triple])
                        for triple in combos
                    ]
                )
            )
            p()
        p()

        double_combos = self._generate_double_combos(doubles, hand_counter)
        double_combos = list(
            chain(
                *[
                    [
                        tuple(list(combo) + [ai])
                        for ai in self._find_potential_ai_triples(combo, hand_counter)
                    ]
                    + [combo]
                    for combo in double_combos
                ]
            )
        )

        p(f"Double Combos ({len(double_combos)}):\n")
        for combos in double_combos:
            p(
                "\n".join(
                    [
                        "\t" + " ".join([tile.name for tile in double])
                        for double in combos
                    ]
                )
            )
            p()
        p()

        best_triple_combo = (
            max([len(combo) for combo in triple_combos])
            if len(triple_combos) > 0
            else 0
        )
        best_double_combo = (
            max([len(combo) for combo in double_combos])
            if len(double_combos) > 0
            else 0
        )

        # p("Cache end size:", len(self.cache))
        # p("Cache hits:", CACHE_HITS)

        return best_triple_combo, best_double_combo
