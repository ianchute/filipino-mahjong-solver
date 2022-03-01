from random import shuffle, choice
from typing import List

from models.tile import Tile


class Game:
    def __init__(self):
        self.deck: List[Tile] = []  # cards still up (including other players)
        self.pile: List[Tile] = []  # cards downed (including other players)
        self.player_hand_up: List[Tile] = []
        self.player_hand_down: List[Tile] = []
        self.deck = (
            [Tile.BAMBOO_1] * 4
            + [Tile.BAMBOO_2] * 4
            + [Tile.BAMBOO_3] * 4
            + [Tile.BAMBOO_4] * 4
            + [Tile.BAMBOO_5] * 4
            + [Tile.BAMBOO_6] * 4
            + [Tile.BAMBOO_7] * 4
            + [Tile.BAMBOO_8] * 4
            + [Tile.BAMBOO_9] * 4
            + [Tile.CHARACTER_1] * 4
            + [Tile.CHARACTER_2] * 4
            + [Tile.CHARACTER_3] * 4
            + [Tile.CHARACTER_4] * 4
            + [Tile.CHARACTER_5] * 4
            + [Tile.CHARACTER_6] * 4
            + [Tile.CHARACTER_7] * 4
            + [Tile.CHARACTER_8] * 4
            + [Tile.CHARACTER_9] * 4
            + [Tile.DOT_1] * 4
            + [Tile.DOT_2] * 4
            + [Tile.DOT_3] * 4
            + [Tile.DOT_4] * 4
            + [Tile.DOT_5] * 4
            + [Tile.DOT_6] * 4
            + [Tile.DOT_7] * 4
            + [Tile.DOT_8] * 4
            + [Tile.DOT_9] * 4
            # + [Tile.FLOWER_1] * 2
            # + [Tile.FLOWER_2] * 2
            # + [Tile.FLOWER_3] * 2
            # + [Tile.FLOWER_4] * 2
            + [Tile.RED] * 4
            + [Tile.GREEN] * 4
            + [Tile.WHITE] * 4
            + [Tile.NORTH] * 4
            + [Tile.SOUTH] * 4
            + [Tile.EAST] * 4
            + [Tile.WEST] * 4
        )
        shuffle(self.deck)

    def random_hand(self):
        for _ in range(16):
            tile = choice(self.deck)
            self.deck.remove(tile)
            self.player_hand_up.append(tile)
            self.player_hand_up.sort(key=lambda t: t.value)

    def down_tile(self, tile: Tile):
        self.deck.remove(tile)
        self.pile.append(tile)

    def random_deck_tile(self):
        return choice(self.deck)

    def take_tile(self, tile_add: Tile, tile_remove: Tile):
        self.player_hand_up.append(tile_add)
        self.player_hand_up.remove(tile_remove)