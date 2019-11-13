import logging
import mysql.connector
from typing import Dict, Optional, Tuple, List
from Model.ModelConsole import Model, ModelConsole


class HandlerSQL:
    database = None

    @staticmethod
    def initialisation() -> bool:
        result = HandlerSQL.sql_connection()
        result = result and HandlerSQL.check_create_database()
        return result
        # HandlerSQL.check_sql()

    @staticmethod
    def database_creation() -> bool:
        result = HandlerSQL.sql_connection()
        result = result and HandlerSQL.drop_db()
        result = result and HandlerSQL.check_create_database()
        result = result and HandlerSQL.initialise_tables_list()
        result = result and HandlerSQL.populate_from_json()
        return result

    @staticmethod
    def populate_from_json() -> None:
        cursor = HandlerSQL.database.cursor()
        query = """
            INSERT IGNORE INTO languages                 
                (language_name) 
            VALUES 
                ('English'), ('Russian')
            """
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            logging.error("Could insert values. {}".format(err.msg))
            exit(1)

        model = ModelConsole()
        model.load_dictionaries()
        model.reset_progress(model.words)

        query_insert_dictionary = """
            INSERT IGNORE INTO dictionaries (
               dictionary_name,
               native_language, 
               foreign_language)
            VALUES 
               (%s, %s, %s);
            """

        query_insert_word = """
            INSERT IGNORE INTO words (
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
            HandlerSQL.insert_query(cursor, query_insert_dictionary, dictionary_values)
            for next_word in next_dictionary.words:
                word_values = (next_dictionary.name,
                               next_word.spelling,
                               next_word.translation,
                               next_word.learning_index)
                HandlerSQL.insert_query(cursor, query_insert_word, word_values)

        HandlerSQL.commit()

    @staticmethod
    def select_query(cursor, query: str, values: List) -> bool:

        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not select values. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def select_unconditional_query(cursor, query: str) -> bool:

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            logging.error("Could not select values. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def insert_query(cursor, query, values) -> bool:

        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not insert values. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def update_query(query, values) -> bool:

        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not update values. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def check_sql() -> bool:

        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute("SHOW TABLES")
            for x in cursor:
                print(x)
        except mysql.connector.Error as err:
            logging.error("Could check MySQL. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def sql_connection() -> bool:

        logging.info("Connecting to MySQL")

        try:
            HandlerSQL.database = mysql.connector.connect(
                host="localhost",
                user="testuser",
                passwd="Develop_1"
            )
        except mysql.connector.Error as err:
            logging.error("Could not connect to MySQL. {}".format(err.msg))
            return False

        logging.info("Connected to MySQL successfully.")
        return True

    @staticmethod
    def check_create_database() -> bool:

        # Check if DB exist and create
        logging.info("Connecting to SQL database 'DictionariesDB'")
        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute("SHOW DATABASES LIKE 'DictionariesDB';")
            db_exist = cursor.fetchone()
            if db_exist is None:
                cursor.execute("CREATE DATABASE DictionariesDB character set utf8;")
            cursor.execute("USE DictionariesDB;")
        except mysql.connector.Error as err:
            logging.error("Could not create database. {}".format(err.msg))
            return False

        logging.info("Connected to database successfully.")
        return True

    @staticmethod
    def close_connection() -> bool:

        logging.info("Closing SQL connection")
        try:
            HandlerSQL.database.close()
        except mysql.connector.Error as err:
            logging.error("Could not close sql connection. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def drop_tables() -> None:

        logging.info("Dropping SQL tables")
        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute("DROP TABLE IF EXISTS words;")
            cursor.execute("DROP TABLE IF EXISTS dictionaries;")
            cursor.execute("DROP TABLE IF EXISTS languages;")
        except mysql.connector.Error as err:
            logging.error("Could not drop table. {}".format(err.msg))
            exit(1)

    @staticmethod
    def drop_db() -> bool:

        logging.info("Dropping database")
        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute("DROP DATABASE IF EXISTS DictionariesDB;")
        except mysql.connector.Error as err:
            logging.error("Could not database. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def initialise_tables_list() -> bool:

        sql_tables: Dict[str, str] = {}
        sql_tables['languages'] = ("""
            CREATE TABLE 
               `languages` (
                   `language_name` varchar(25) NOT NULL PRIMARY KEY
                );
            """
        )

        sql_tables['dictionaries'] = ("""
            CREATE TABLE 
               `dictionaries` (
                   `dictionary_name` varchar(50) NOT NULL PRIMARY KEY, 
                   `native_language` varchar(25), 
                   `foreign_language` varchar(25), 
                   FOREIGN KEY (`native_language`) REFERENCES `languages`(`language_name`), 
                   FOREIGN KEY (`foreign_language`) REFERENCES `languages`(`language_name`) 
               );
            """
        )

        sql_tables['words'] = ("""
            CREATE TABLE 
               `words` (
                   `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                   `dictionary` varchar(50) NOT NULL, 
                   `spelling` varchar(255) NOT NULL, 
                   `translation` varchar(255) NOT NULL, 
                   `learning_index` INT(3) NOT NULL, 
                   FOREIGN KEY (`dictionary`) REFERENCES `dictionaries`(`dictionary_name`) 
               );
            """
        )

        for table_name, table_description in sql_tables.items():
            if not HandlerSQL.check_create_table(table_name, table_description):
                return False
        return True

    # Create table
    @staticmethod
    def check_create_table(table_name, table_description) -> bool:

        logging.info("Checking table {}".format(table_name))
        try:
            cursor = HandlerSQL.database.cursor()
            query = "SHOW TABLES LIKE '{}';".format(table_name)
            cursor.execute(query)
            table_exist = cursor.fetchone()
            if table_exist is None:
                cursor.execute(table_description)
            else:
                logging.info("Table {} already exist".format(table_name))
        except mysql.connector.Error as err:
            logging.error("Could not create table. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def commit() -> bool:
        try:
            HandlerSQL.database.commit()
        except mysql.connector.Error as err:
            logging.error("Could not commit database. {}".format(err.msg))
            return False

        return True
