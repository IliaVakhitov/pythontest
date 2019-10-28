from Model.model import *
from Model.Dictionary import DictionaryLoaderJson
from Test.ModelTestClasses import ModelTests

load_dictionaries()
game_rounds = generate_game(5)
if game_rounds is None:
    pass

play_game(game_rounds)
