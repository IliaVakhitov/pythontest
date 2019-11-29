import logging
from typing import Dict

from Model import DatabaseConnector
from Model.ModelDictionariesConsole import ModelConsole
from Model.QueryManager import QueryManager
from View import view


class TablesMaker:

    def __init__(self, database_connector: DatabaseConnector):
        self.database_connector: DatabaseConnector = database_connector
        self.query_manager: QueryManager = QueryManager(database_connector.sql_type)

    def check_tables(self) -> bool:

        """
        Check tables
        If table doesn't exist, creates it
        :return:
            True - created successful
            False - error in creating tables
        """

        result = self.initialise_tables_list()
        if result:
            return self.check_table_words()
        else:
            return False

    def check_table_words(self) -> bool:

        """
        If table words is empty, ask to fill from json
        :return:
            True - table is not empty
            False - could not fill the table
        """

        logging.info("Checking entries in table words")
        if not self.database_connector.execute_query(self.query_manager.total_words_query()):
            logging.error("Could not get total words in dictionaries!")
            return False

        total_words = self.database_connector.cursor.fetchone()[0]
        logging.info(f"Total words: {total_words}")
        if total_words == 0:
            logging.info("Request to refill data from Json")
            view.print_str("No words in table Words!")
            user_answer = view.input_str("Would you like to refill data from JSON? y/n")
            if user_answer == "y":
                logging.info("Refilling from Json")
                return self.database_creation()

        return True

    def populate_from_json(self) -> bool:

        """
        Fill database with data, loaded by ModelConsole from Json files
        :return:
            True: Databases filled successful
            False: Error in log
        """

        result = self.database_connector.execute_query(self.query_manager.query_insert_languages())
        if not result:
            return False

        model = ModelConsole()
        model.load_dictionaries()
        model.reset_progress(model.words)

        for next_dictionary in model.dictionaries:
            dictionary_values = (next_dictionary.name,
                                 next_dictionary.native_language,
                                 next_dictionary.foreign_language)

            result = self.database_connector.execute_query(
                self.query_manager.query_insert_dictionary(),
                dictionary_values)
            if not result:
                return False

            for next_word in next_dictionary.words:
                word_values = (next_dictionary.name,
                               next_word.spelling,
                               next_word.translation,
                               next_word.learning_index)
                result = self.database_connector.execute_query(
                    self.query_manager.query_insert_word(),
                    word_values)
                if not result:
                    return False

        self.database_connector.commit()
        return True

    def database_creation(self) -> bool:

        result = self.drop_tables()
        result = result and self.initialise_tables_list()
        result = result and self.populate_from_json()
        return result

    def initialise_tables_list(self) -> bool:

        """
        Create SQL tables in database
        :return:
            True: Tables created in database
            False: Error in log
        """

        sql_tables: Dict[str, str] = {}
        sql_tables['languages'] = (self.query_manager.query_create_languages())
        sql_tables['dictionaries'] = (self.query_manager.query_create_dictionaries())
        sql_tables['words'] = (self.query_manager.query_create_words())

        for table_name, table_description in sql_tables.items():
            if not self.check_create_table(table_name, table_description):
                return False

        return True

    def check_create_table(self, table_name, table_description) -> bool:

        """
        Check if table exists in database and create if not
        :param table_name:str
        :param table_description: query to create table
        :return:
            True: table created successful
            False: Error in log
        """

        logging.info(f"Checking table \'{format(table_name)}\'")

        result = self.database_connector.execute_query(
            self.query_manager.query_table_exists(),
            {'table_name': table_name})

        if not result:
            return False

        table_exist = self.database_connector.cursor.fetchone()

        if (table_exist is None) or (table_exist is not None and table_exist[0] is False):
            result = self.database_connector.execute_query(table_description)
            if not result:
                return False
            logging.info(f"Table \'{table_name}\' created")
        else:
            logging.info(f"Table \'{table_name}\' already exist")

        return True

    def drop_tables(self) -> bool:

        """
        Drop tables to refill with Json data
        :return:
            True: Tables dropped successful
            False: Error in log
        """
        logging.info("Dropping SQL tables")
        result = self.database_connector.execute_query(self.query_manager.query_drop_table("words"))
        if not result:
            return False
        result = self.database_connector.execute_query(self.query_manager.query_drop_table("dictionaries"))
        if not result:
            return False

        result = self.database_connector.execute_query(self.query_manager.query_drop_table("languages"))
        if not result:
            return False

        logging.info("SQL tables dropped successful")
        return True
