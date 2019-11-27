import codecs
import json
import logging
from typing import List, Optional
from os import path
from Model.Dictionary import DictEntry
from Model.GameGenerator import GameGenerator
from Model.GameRound import GameRound
from Model.HandlerMySQL import HandlerMySQL
from Model.HandlerPostgreSQL import HandlerPostgreSQL
from Model.HandlerSQL import HandlerSQL
from Model.GameType import GameType
from Model.Model import Model
from Model.SQLType import SQLType


class ModelSQL(Model):

    """
    Uses SQL as database
    Different options to generate games
        Amount of words
        Less knows words
        Words from selected dictionaries
    """

    def __init__(self, sql_type: SQLType = SQLType.PostgreSQL) -> None:

        # Default values
        self.sql_type = SQLType.PostgreSQL
        self.game_rounds = 10
        self.load_properties()

        if self.sql_type == SQLType.MySQL:
            self.handler_sql: HandlerSQL = HandlerMySQL()
        elif self.sql_type == SQLType.PostgreSQL:
            self.handler_sql: HandlerSQL = HandlerPostgreSQL()
        else:
            logging.error(f"Undefined SQL type \'{sql_type}\'")
            exit(1)

    def save_state(self, game_rounds: Optional[List[GameRound]]) -> bool:

        """
        Making UPDATE request into database to update learning index
        :return:
            True - updated successful
            False - entries did not updated
        """
        self.save_properties()

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
            logging.info("ID \'{}\', word \'{}\', new learning_index \'{}\'".format(
                game_round.dictionary_entry.sql_id,
                game_round.dictionary_entry.spelling,
                game_round.new_learning_index
            ))
            args = {
                'learning_index': game_round.new_learning_index,
                'id': game_round.dictionary_entry.sql_id}

            result = self.handler_sql.update_query(update_query, args)
            if not result:
                return False

        return self.handler_sql.commit()

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

        logging.info(f"game_type {game_type}")
        logging.info(f"Word_limit {word_limit}")
        logging.info(f"Dictionaries {dictionaries}")

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

        if isinstance(self.handler_sql, HandlerMySQL):
            words_query += """
                ORDER BY 
                    RAND()
                """
        elif isinstance(self.handler_sql, HandlerPostgreSQL):
            words_query += """
                ORDER BY 
                    RANDOM()
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

        cursor = self.handler_sql.database.cursor()
        if not self.handler_sql.select_query(cursor, words_query, args):
            logging.error("Error in Select query.")
            return None

        words_list: List[DictEntry] = []
        for entry in cursor:
            words_list.append(DictEntry(entry[1], entry[2], entry[3], entry[0]))

        logging.info(f"Total game rounds {len(words_list)}")

        return GameGenerator.generate_game(words_list, game_type)

    def play_game(self, game_rounds: List[GameRound], automatic_mode: bool = False) -> None:
        super().play_game(game_rounds, automatic_mode)

    def load_properties(self) -> bool:
        filename = "properties.json"
        if not path.exists(filename):
            logging.info(f"File properties.json was not found. Saving default values.")
            self.save_properties()
            return True
        try:
            with codecs.open(filename, 'r', "utf-8") as json_file:
                json_data = json.load(json_file)
        except IOError:
            error_message = f"File read error {filename}"
            print(error_message)
            logging.error(error_message)
            return False
        except:
            error_message = f"File general error {filename}"
            print(error_message)
            logging.error(error_message)
            return False

        self.sql_type = SQLType(json_data['sql_type'])
        self.game_rounds = json_data['game_rounds']
        logging.info(f"Properties loaded.")
        logging.info(f"SQL type \'{self.sql_type.name}\'")
        logging.info(f"Game rounds \'{self.game_rounds}\'")

        return True

    def save_properties(self) -> bool:
        filename = "properties.json"
        json_data = {
            'sql_type': self.sql_type.value,
            'game_rounds': self.game_rounds}

        try:
            with codecs.open(filename, 'w', "utf-8") as outfile:
                json.dump(json_data, outfile, indent=4, ensure_ascii=False)
        except:
            logging.error(f"Error writing file \'{filename}\'")
            return False
        return True
