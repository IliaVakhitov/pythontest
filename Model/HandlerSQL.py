import logging.handlers
import mysql.connector
from typing import Dict, Optional, Tuple
from Model.Model import Model


class HandlerSQL:
    database = None

    @staticmethod
    def initialisation():
        HandlerSQL.sql_connection()
        HandlerSQL.check_create_database()
        # HandlerSQL.check_sql()

    @staticmethod
    def database_creation():
        HandlerSQL.sql_connection()
        HandlerSQL.drop_db()
        HandlerSQL.check_create_database()
        HandlerSQL.initialise_tables_list()
        HandlerSQL.populate_from_json()

    @staticmethod
    def populate_from_json():
        cursor = HandlerSQL.database.cursor()
        query = """
            INSERT IGNORE INTO languages                 
                (name) 
            VALUES 
                ('English'), ('Russian')
            """
        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            logging.error("Could insert values. {}".format(err.msg))
            exit(1)

        model = Model()
        model.load_dictionaries()
        model.reset_progress()

        query_insert_dictionary = """
            INSERT IGNORE INTO dictionaries (
               name,
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

        HandlerSQL.database.commit()

    @staticmethod
    def select_query(cursor, query: str, values: Tuple) -> Optional[bool]:
        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not select values. {}".format(err.msg))
            return False
        return True

    @staticmethod
    def insert_query(cursor, query, values):
        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not insert values. {}".format(err.msg))
            exit(1)

    @staticmethod
    def check_sql():
        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute("SHOW TABLES")
            for x in cursor:
                print(x)
        except mysql.connector.Error as err:
            logging.error("Could check MySQL. {}".format(err.msg))
            exit(1)

    @staticmethod
    def sql_connection() -> None:
        logging.info("Connecting to MySQL")
        try:
            HandlerSQL.database = mysql.connector.connect(
                host="localhost",
                user="test_user",
                passwd="Developer"
            )
        except mysql.connector.Error as err:
            logging.error("Could not connect to MySQL. {}".format(err.msg))
            exit(1)

        logging.info("Connected to MySQL successfully.")

    @staticmethod
    def check_create_database() -> None:
        # Check if DB exist and create
        logging.info("Connecting to SQL database 'DictionariesDB'")
        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute("SHOW DATABASES LIKE 'DictionariesDB';")
            db_exist = cursor.fetchone()
            if db_exist is None:
                cursor.execute("CREATE DATABASE DictionariesDB;")
            cursor.execute("USE DictionariesDB;")
        except mysql.connector.Error as err:
            logging.error("Could not create database. {}".format(err.msg))
            exit(1)

        logging.info("Connected to database successfully.")

    @staticmethod
    def close_connection() -> None:
        logging.info("Closing SQL connection")
        HandlerSQL.database.close()

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
    def drop_db() -> None:
        logging.info("Dropping database")
        try:
            cursor = HandlerSQL.database.cursor()
            cursor.execute("DROP DATABASE IF EXISTS DictionariesDB;")
        except mysql.connector.Error as err:
            logging.error("Could not database. {}".format(err.msg))
            exit(1)

    @staticmethod
    def initialise_tables_list():
        sql_tables: Dict[str, str] = {}
        sql_tables['languages'] = ("""
            CREATE TABLE 
               `languages` (
                   `name` varchar(25) NOT NULL PRIMARY KEY
                );
            """
        )

        sql_tables['dictionaries'] = ("""
            CREATE TABLE 
               `dictionaries` (
                   `name` varchar(50) NOT NULL PRIMARY KEY, 
                   `native_language` varchar(25), 
                   `foreign_language` varchar(25), 
                   FOREIGN KEY (`native_language`) REFERENCES `languages`(`name`), 
                   FOREIGN KEY (`foreign_language`) REFERENCES `languages`(`name`) 
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
                   FOREIGN KEY (`dictionary`) REFERENCES `dictionaries`(`name`) 
               );
            """
        )

        for table_name, table_description in sql_tables.items():
            HandlerSQL.check_create_table(table_name, table_description)

    # Creating tables
    @staticmethod
    def check_create_table(table_name, table_description):
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
            exit(1)
