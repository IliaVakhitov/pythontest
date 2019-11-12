from typing import List, Optional
import logging
from Model.Dictionary import DictEntry
from Model.GameGenerator import GameGenerator
from Model.GameRound import GameRound
from Model.HandlerSQL import HandlerSQL
from Model.GameType import GameType
from Model.Model import Model


class ModelSQL(Model):

    """
    Uses SQL as database
    Different options to generate games
        Amount of words
        Less knows words
        Words from selected dictionaries
    """

    def __init__(self) -> None:
        HandlerSQL.initialisation()

    def save_state(self, game_rounds: Optional[List[GameRound]]) -> bool:

        """
        Making UPDATE request into database to update learning index
        :return:
            True - updated successful
            False - entries did not updated
        """
        if game_rounds is None:
            return False

        update_query = """
            UPDATE 
                words
            SET 
                learning_index = %(learning_index)s
            WHERE 
                id = %(id)s;
            """
        # Log
        logging.info("Updating learning_index in database")
        for game_round in game_rounds:
            if not game_round.learning_index_changed:
                continue
            logging.info("ID {}, word {}, new learning_index {}".format(
                game_round.dictionary_entry.sql_id,
                game_round.dictionary_entry.spelling,
                game_round.new_learning_index
            ))
            args = {
                'learning_index': game_round.new_learning_index,
                'id': game_round.dictionary_entry.sql_id}

            result = HandlerSQL.update_query(update_query, args)
            if not result:
                return False

        return HandlerSQL.commit()

    def load_dictionaries(self):
        pass

    def reset_progress(self, words):
        super().reset_progress(words)

    def print_dictionaries(self, dictionaries) -> None:
        super().print_dictionaries(dictionaries)

    def generate_game(
            self,
            game_type: GameType,
            word_limit: int = 0,
            dictionaries: Optional[List[str]] = None) -> Optional[List[GameRound]]:

        """
        Generates list of game rounds with query to SQL database.
        Query used to get list of DictEntries.
        Than game generated with GameGenerator class.
        :param game_type: enum game type
        :param word_limit: 0 or higher than 4. 4 - minimum for a game
        :param dictionaries: list of str with names of dictionaries
        :return:
            None - could not generate game
            List of game rounds
        """
        # Logs
        logging.info("Generating game.")
        if 0 < word_limit < 4:
            logging.info("Not enough words to generate game!")
            return None

        logging.info("Game type {}".format(game_type))
        logging.info("Word_limit {}".format(word_limit))
        logging.info("Dictionaries {}".format(dictionaries))

        words_query = """
            SELECT
                id, 
                spelling, 
                translation,
                learning_index
            FROM
                words
            """
        # Condition is used if param dictionaries if defined
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
        # Condition is used if param word_limit if defined
        limit_condition = """
            LIMIT %s;
            """

        # Generating list of parameters for cursor query
        args: List = list()
        if dictionaries is not None and len(dictionaries) > 0:
            args = list(dictionaries)
        if word_limit != 0:
            words_query += limit_condition
            args.append(word_limit)

        cursor = HandlerSQL.database.cursor()
        if not HandlerSQL.select_query(cursor, words_query, args):
            print("Error in Select query.")
            logging.error("Error in Select query.")
            return None

        words_list: List[DictEntry] = []
        for entry in cursor:
            words_list.append(DictEntry(entry[1], entry[2], entry[3], entry[0]))

        logging.info("Total game rounds {}".format(len(words_list)))

        return GameGenerator.generate_game(words_list, game_type)

    def play_game(self, game_rounds: List[GameRound], automatic_mode: bool = False) -> None:
        super().play_game(game_rounds, automatic_mode)
