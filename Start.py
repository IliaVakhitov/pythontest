import logging.handlers
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
game = model_sql.generate_game(GameType.FindTranslation, 5, [])
Model.play_game(game, False)
