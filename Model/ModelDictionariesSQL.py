import codecs
import json
import logging
from json import JSONDecodeError
from os import path
from typing import List, Optional

from Model.DatabaseConnector import DatabaseConnector
from Model.DictEntry import DictEntry
from Model.GameGenerator import GameGenerator
from Model.GameRound import GameRound
from Model.GameType import GameType
from Model.ModelDictionaries import Model
from Model.QueryManager import QueryManager
from Model.SQLType import SQLType


class ModelSQL(Model):

    """
    Uses SQL as database
    Different options to generate games
        Amount of words
        Less knows words
        Words from selected dictionaries
    """

    def __init__(self) -> None:

        # Default values
        self.game_rounds = 10
        self.load_properties()
        self.database_connector: DatabaseConnector = DatabaseConnector()
        self.query_manager: QueryManager = QueryManager(self.database_connector.sql_type)

    def save_state(self, game_rounds: Optional[List[GameRound]]) -> bool:

        """
        Making UPDATE request into database to update learning index
        :return:
            True - updated successful
            False - entries did not updated
        """

        if game_rounds is None:
            return False

        logging.info("Updating learning_index in database")
        for game_round in game_rounds:
            if not game_round.learning_index_changed:
                continue
            logging.info("ID \'{}\', word \'{}\', new learning_index \'{}\'".format(
                game_round.dictionary_entry.sql_id,
                game_round.dictionary_entry.spelling,
                game_round.new_learning_index
            ))
            args = {
                'learning_index': game_round.new_learning_index,
                'id': game_round.dictionary_entry.sql_id}

            result = self.database_connector.execute_query(self.query_manager.query_update_words(), args)
            if not result:
                return False

        return self.database_connector.commit()

    def reset_progress(self, words):
        super().reset_progress(words)

    def print_dictionaries(self, dictionaries) -> None:
        super().print_dictionaries(dictionaries)

    def generate_game(
            self,
            game_type: GameType,
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
        if 0 < self.game_rounds < 4:
            logging.info("Not enough words to generate game!")
            return None

        logging.info(f"game_type {game_type}")
        logging.info(f"Word_limit {self.game_rounds}")
        logging.info(f"Dictionaries {dictionaries}")
        query_dict = self.query_manager.query_select_words(self.game_rounds, dictionaries)

        if not self.database_connector.execute_query(query_dict['query_select_words'], query_dict['args']):
            logging.error("Error in Select query.")
            return None

        words_list: List[DictEntry] = []
        for entry in self.database_connector.cursor:
            words_list.append(DictEntry(entry[1], entry[2], entry[3], entry[0]))

        logging.info(f"Total game rounds {len(words_list)}")

        return GameGenerator.generate_game(words_list, game_type)

    def play_game(self, game_rounds: List[GameRound], automatic_mode: bool = False) -> None:

        super().play_game(game_rounds, automatic_mode)

    def load_properties(self) -> bool:

        """
        TODO
        :return:
        """

        filename = "config.json"
        if not path.exists(filename):
            logging.info(f"File config.json was not found. Using default values.")
            return True

        try:
            with codecs.open(filename, 'r', "utf-8") as json_file:
                json_data = json.load(json_file)
        except IOError:
            error_message = f"File read error \'{filename}\'"
            print(error_message)
            logging.error(error_message)
            return False

        except JSONDecodeError as err:
            error_message = f"Json parse error \'{err}\'"
            print(error_message)
            logging.error(error_message)
            return False

        self.game_rounds = json_data['game_rounds']
        # TODO
        dictionaries = json_data['dictionaries']
        logging.info(f"Properties loaded.")
        logging.info(f"Game rounds \'{self.game_rounds}\'")

        return True

    def load_dictionaries(self):
        pass
