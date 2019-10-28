from Model.model import *
from Model.Dictionary import DictionaryLoaderJson
from Test.ModelTestClasses import ModelTests

load_dictionaries()
game_rounds = generate_game(0)
for game_round in game_rounds:
    view.print_str(game_round.print_game_round())
