import logging

from Model.model import Model

logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

my_model = Model()
my_model.load_dictionaries()
game_rounds = my_model.generate_game(5)
if game_rounds is None:
    exit()

#my_model.play_game(game_rounds)

