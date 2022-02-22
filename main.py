import pandas as pd
from models.game import Game
from models.tile import Tile
from solver import Solver, TIMES

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
#     Tile.CHARACTER_2,
#     Tile.CHARACTER_3,
#     Tile.CHARACTER_4,
#     Tile.CHARACTER_5,
#     Tile.CHARACTER_6,
#     Tile.NORTH,
#     Tile.NORTH,
# ]
# game.player_hand_up = [
#     Tile.BAMBOO_1,
#     Tile.BAMBOO_1,
#     Tile.BAMBOO_2,
#     Tile.BAMBOO_2,
#     Tile.BAMBOO_3,
#     Tile.BAMBOO_3,
#     Tile.BAMBOO_4,
#     Tile.BAMBOO_4,
#     Tile.BAMBOO_5,
#     Tile.BAMBOO_5,
#     Tile.BAMBOO_6,
#     Tile.BAMBOO_6,
#     Tile.BAMBOO_7,
#     Tile.BAMBOO_7,
#     Tile.BAMBOO_8,
#     Tile.BAMBOO_8,
# ]
# game.player_hand_up = [
#     Tile.BAMBOO_1,
#     Tile.BAMBOO_1,
#     Tile.BAMBOO_1,
#     Tile.BAMBOO_2,
#     Tile.BAMBOO_2,
#     Tile.BAMBOO_2,
#     Tile.BAMBOO_3,
#     Tile.BAMBOO_3,
#     Tile.BAMBOO_3,
#     Tile.BAMBOO_4,
#     Tile.BAMBOO_4,
#     Tile.BAMBOO_4,
#     Tile.BAMBOO_5,
#     Tile.BAMBOO_5,
#     Tile.BAMBOO_5,
#     Tile.BAMBOO_6,
# ]
# game.player_hand_up = [
#     Tile[i]
#     for i in """
# SOUTH
# RED
# BAMBOO_2
# BAMBOO_4
# BAMBOO_6
# BAMBOO_8
# DOT_1
# DOT_3
# DOT_3
# DOT_4
# DOT_6
# DOT_8
# DOT_9
# CHARACTER_1
# CHARACTER_2
# CHARACTER_3
# """.strip().split()
# ]

assert len(game.player_hand_up) == 16
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

best_triple_combo, best_double_combo = solver.compute_victory_distance(debug=True)
print(best_triple_combo, best_double_combo)

solver.forecast().to_csv("results.csv", index=False)
pd.Series(TIMES).to_csv("times.csv", float_format="%.3f")
pd.Series(solver.cache).to_csv("cache.csv")
