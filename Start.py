from Model.model import *
import logging

logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

load_dictionaries()
game_rounds = generate_game(50)
if game_rounds is None:
    exit()

play_game(game_rounds)
