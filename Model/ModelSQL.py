from typing import List, Tuple, Optional

from Model.Dictionary import DictEntry
from Model.GameGenerator import GameGenerator
from Model.GameRound import GameRound
from Model.HandlerSQL import HandlerSQL
from Model.GameType import GameType


class ModelSQL:
    """ Uses SQL as database
    """
    def __init__(self):
        HandlerSQL.initialisation()

    @staticmethod
    def generate_game(game_type: GameType, words_number, dictionaries: List[str]) -> Optional[List[GameRound]]:
        words_query = """
        SELECT 
            spelling, 
            translation,
            learning_index
        FROM
            words
        WHERE
            learning_index = %s
        ORDER BY 
            learning_index DESC
        LIMIT %s;
        """
        cursor = HandlerSQL.database.cursor()
        values:Tuple = (0,words_number)
        if not HandlerSQL.select_query(cursor, words_query, values):
            print("Error in Select query")
            return None
        words_list: List[DictEntry] = []
        for entry in cursor:
            words_list.append(DictEntry(entry[0], entry[1], entry[2]))
        return GameGenerator.generate_game(words_list, game_type)


    @staticmethod
    def play_game(game_rounds, automatic_mode: bool = False) -> None:
        pass
