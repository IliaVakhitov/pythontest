import logging.handlers

from Model.GameType import GameType
from Model.HandlerSQL import HandlerSQL
from Model.ModelSQL import ModelSQL

logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s')

model_sql = ModelSQL()

game = model_sql.generate_game(GameType.FindTranslation, 500)

model_sql.play_game(game, True)

model_sql.save_state(game)


