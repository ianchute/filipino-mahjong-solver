import pandas as pd
from models.game import Game
from models.tile import Tile
from solver import Solver

print("Initializing game...")
game = Game()
print(f"\n\nThere are {len(game.deck)} tiles in the deck!")

print("Initializing hands...")
game.initialize_hands()
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