import logging.handlers

from Model.GameType import GameType
from Model.HandlerSQL import HandlerSQL
from Model.ModelConsole import ModelConsole
from Model.ModelSQL import ModelSQL

logging.basicConfig(
    handlers=[logging.FileHandler('app.log', 'a', 'utf-8')],
    format='%(levelname)s %(asctime)s - %(message)s',
    level=logging.INFO,
)


# HandlerSQL.database_creation()


model_sql = ModelSQL()

game = model_sql.generate_game(GameType.FindSpelling, 50)
model_sql.play_game(game, True)
model_sql.save_state(game)

game = model_sql.generate_game(GameType.FindTranslation, 50)
model_sql.play_game(game, True)
model_sql.save_state(game)

"""
model = ModelConsole()
model.load_dictionaries()

"""
