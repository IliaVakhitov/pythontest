from typing import List, Tuple, Optional, Dict
from Model.Dictionary import DictEntry
from Model.GameGenerator import GameGenerator
from Model.GameRound import GameRound
from Model.HandlerSQL import HandlerSQL
from Model.GameType import GameType
from Model.Model import Model


class ModelSQL(Model):
    """ Uses SQL as database
    Different options to generate games
        Amount of words
        Less knows words
        Words from selected dictionaries
    """
    def __init__(self):
        HandlerSQL.initialisation()

    def save_state(self):
        pass

    def load_dictionaries(self):
        pass

    def reset_progress(self, words):
        super().reset_progress(words)

    def print_dictionaries(self, dictionaries) -> None:
        super().print_dictionaries(dictionaries)

    def generate_game(self,
                      game_type: GameType,
                      word_limit: int = 0,
                      dictionaries: Optional[List[str]] = None) -> Optional[List[GameRound]]:

        words_query = """
        SELECT 
            spelling, 
            translation,
            learning_index
        FROM
            words
        """
        dictionary_condition = """
        WHERE
            dictionary in (%s)
        """
        if dictionaries is not None and len(dictionaries) > 0:
            in_condition = ','.join(['%s'] * len(dictionaries))
            words_query += dictionary_condition % in_condition
        words_query += """
        ORDER BY 
            RAND()
        """
        limit_condition = """
        LIMIT %s;
        """
        if word_limit != 0:
            words_query += limit_condition

        cursor = HandlerSQL.database.cursor()

        args: List = list(dictionaries)
        args.append(word_limit)

        if not HandlerSQL.select_query(cursor, words_query, args):
            print("Error in Select query")
            return None
        words_list: List[DictEntry] = []
        for entry in cursor:
            words_list.append(DictEntry(entry[0], entry[1], entry[2]))
        return GameGenerator.generate_game(words_list, game_type)

    def play_game(self, game_rounds: List[GameRound], automatic_mode: bool = False) -> None:
        super().play_game(game_rounds, automatic_mode)
