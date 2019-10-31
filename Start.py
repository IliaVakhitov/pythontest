import logging.handlers
from Model.model import Model, GameType

logging.basicConfig(level=logging.INFO,
                    filename='app.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

log_fh = open("app.log", "a", encoding="utf-8")
ch = logging.StreamHandler(log_fh)
ch.setLevel(logging.DEBUG)
log = logging.getLogger("MAIN")
log.addHandler(ch)

my_model = Model()
my_model.load_dictionaries()
game_rounds = my_model.generate_game(GameType.FindWord, 5)
if game_rounds is None:
    exit()

my_model.play_game(game_rounds)

