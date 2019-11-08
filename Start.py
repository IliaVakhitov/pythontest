import logging.handlers
from typing import List, Tuple

from Model.ModelConsole import Model
from Model.GameType import GameType
from Model.HandlerSQL import HandlerSQL
from Model.ModelSQL import ModelSQL

logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s')


HandlerSQL.initialisation()

model_sql = ModelSQL()
dictionaries = list()
dictionaries.append('Idioms')
dictionaries.append('Everyday')
game = model_sql.generate_game(GameType.FindTranslation, 5, dictionaries)
Model.play_game(game, True)
