import logging.handlers
from Model.model import Model, GameType

logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s')

my_model = Model()
my_model.load_dictionaries()

for i in range(100):
    game_rounds = my_model.generate_game(GameType.FindTranslation, 50)
    if game_rounds is None:
        exit()
    my_model.play_game(game_rounds, True)

    game_rounds = my_model.generate_game(GameType.FindWord, 50)
    if game_rounds is None:
        exit()
    my_model.play_game(game_rounds, True)

my_model.save_dictionaries()
