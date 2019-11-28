import logging.handlers
from Model.GameType import GameType
from Model.ModelSQL import ModelSQL
from View import view

logging.basicConfig(
    handlers=[logging.FileHandler('app.log', 'a', 'utf-8')],
    format='%(levelname)s %(asctime)s - %(message)s',
    level=logging.INFO,
)


model_sql = ModelSQL()

if not model_sql.database_connector.connected:
    logging.info("SQL didn't connected")
    exit(1)


view.print_str("Hello and welcome!")
view.print_str("Available games:")
view.print_str("1. Find translation")
view.print_str("2. Find spelling")
view.print_str("Print \'exit\' for exit.")
user_choice = view.input_user_choice("Select game type:", "[1-2](?!\\d)")

game = model_sql.generate_game(GameType(user_choice), model_sql.game_rounds)
model_sql.play_game(game, False)
model_sql.save_state(game)

view.print_str("Goodbye!")
