import logging
from abc import ABC, abstractmethod

import mysql.connector
from typing import List
from Model.ModelConsole import ModelConsole


class HandlerSQL(ABC):

    def __init__(self) -> None:
        self.database = self.sql_connection()
        self.connected = self.database is not None
        self.connected = self.connected and self.check_create_database()

    @abstractmethod
    def sql_connection(self):
        pass

    @abstractmethod
    def close_connection(self, ) -> bool:
        pass

    @abstractmethod
    def database_creation(self) -> bool:
        pass

    @abstractmethod
    def select_query(self, cursor, query: str, values: List) -> bool:
        pass

    @abstractmethod
    def select_unconditional_query(self, cursor, query: str) -> bool:
        pass

    @abstractmethod
    def insert_query(self, cursor, query, values) -> bool:
        pass

    @abstractmethod
    def update_query(self, query, values) -> bool:
        pass

    @abstractmethod
    def check_create_database(self) -> bool:
        pass

    @abstractmethod
    def drop_tables(self) -> bool:
        pass

    @abstractmethod
    def drop_db(self) -> bool:
        pass

    @abstractmethod
    def initialise_tables_list(self, ) -> bool:
        pass

    @abstractmethod
    def check_create_table(self, table_name, table_description) -> bool:
        pass

    @abstractmethod
    def commit(self) -> bool:
        pass

    def populate_from_json(self) -> bool:
        cursor = self.database.cursor()
        query = """
            INSERT INTO languages                 
                (language_name) 
            VALUES 
                ('English'), ('Russian')
            """
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            logging.error(f"Could insert values. {err.msg}")
            return False

        model = ModelConsole()
        model.load_dictionaries()
        model.reset_progress(model.words)

        query_insert_dictionary = """
            INSERT INTO dictionaries (
               dictionary_name,
               native_language, 
               foreign_language)
            VALUES 
               (%s, %s, %s);
            """

        query_insert_word = """
            INSERT INTO words (
               dictionary,
               spelling,
               translation,
               learning_index) 
            VALUES 
               (%s, %s, %s, %s);
            """

        for next_dictionary in model.dictionaries:
            dictionary_values = (next_dictionary.name,
                                 next_dictionary.native_language,
                                 next_dictionary.foreign_language)
            self.insert_query(cursor, query_insert_dictionary, dictionary_values)
            for next_word in next_dictionary.words:
                word_values = (next_dictionary.name,
                               next_word.spelling,
                               next_word.translation,
                               next_word.learning_index)
                self.insert_query(cursor, query_insert_word, word_values)

        self.commit()

        return True
