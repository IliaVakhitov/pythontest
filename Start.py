import logging.handlers

from Model.GameType import GameType
from Model.HandlerMySQL import HandlerMySQL
from Model.HandlerPostgreSQL import HandlerPostgreSQL
from Model.HandlerSQL import HandlerSQL
from Model.ModelConsole import ModelConsole
from Model.ModelSQL import ModelSQL
from Model.SQLType import SQLType

logging.basicConfig(
    handlers=[logging.FileHandler('app.log', 'a', 'utf-8')],
    format='%(levelname)s %(asctime)s - %(message)s',
    level=logging.INFO,
)


model_sql = ModelSQL(SQLType.PostgreSQL)

if not model_sql.handler_sql.connected:
    logging.info()

game = model_sql.generate_game(GameType.FindSpelling, 50)
model_sql.play_game(game, True)
model_sql.save_state(game)

game = model_sql.generate_game(GameType.FindTranslation, 50)
model_sql.play_game(game, True)
model_sql.save_state(game)

