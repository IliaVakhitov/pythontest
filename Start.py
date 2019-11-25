import logging.handlers
from Model.GameType import GameType
from Model.ModelSQL import ModelSQL
from Model.SQLType import SQLType
from View import view

logging.basicConfig(
    handlers=[logging.FileHandler('app.log', 'a', 'utf-8')],
    format='%(levelname)s %(asctime)s - %(message)s',
    level=logging.INFO,
)



"""
view.print_str("Hello and welcome!")
view.print_str("Available games")
view.print_str("1. Find translation")
view.print_str("2. Find spelling")
view.print_str("Print \'exit\' for exit.")
user_choice = view.input_user_choice("Select game type:", "[1-2](?!\\d)")
"""

model_sql = ModelSQL(SQLType.PostgreSQL)

if not model_sql.handler_sql.connected:
    logging.info()
    exit(1)

#if user_choice == 1:
game = model_sql.generate_game(GameType.FindSpelling, 10)
model_sql.play_game(game, True)
model_sql.save_state(game)
#else:
game = model_sql.generate_game(GameType.FindTranslation, 10)
model_sql.play_game(game, True)
model_sql.save_state(game)


#view.print_str("Goodbye!")
