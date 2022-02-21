import pandas as pd
from models.game import Game
from models.tile import Tile
from solver import Solver

print("Initializing game...")
game = Game()
print(f"\n\nThere are {len(game.deck)} tiles in the deck!")

print("Initializing hands...")
game.random_hand()
# game.player_hand_up = [
#     Tile.BAMBOO_1,
#     Tile.BAMBOO_2,
#     Tile.BAMBOO_3,
#     Tile.BAMBOO_4,
#     Tile.BAMBOO_5,
#     Tile.BAMBOO_6,
#     Tile.BAMBOO_7,
#     Tile.BAMBOO_8,
#     Tile.BAMBOO_9,
#     Tile.CHARACTER_1,
#     Tile.CHARACTER_2,
#     Tile.CHARACTER_3,
#     Tile.CHARACTER_4,
#     Tile.CHARACTER_5,
#     Tile.CHARACTER_6,
#     Tile.NORTH,
#     Tile.NORTH
# ]
print(f"\n\nThere are {len(game.deck)} tiles in the deck!")

print(f"\n\nThere are {len(game.player_hand_up)} tiles in the player's hand!\n")
for tile in game.player_hand_up:
    print("\t" + tile.name)

# print()
# print(
#     pd.Series([t.value for t in game.deck])
#     .value_counts()
#     .sort_index()
#     .rename(index=lambda i: Tile(i).name)
# )

print("\n\n")

solver = Solver(game)

solver.compute_victory_distance()