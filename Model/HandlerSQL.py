import logging
import mysql.connector
from typing import Optional, Dict, List
from Model.ModelConsole import ModelConsole


class HandlerSQL:

    def __init__(self) -> None:
        self.database = self.sql_connection()
        self.connected = self.database is not None
        self.connected = self.connected and self.check_create_database()

    def sql_connection(self):

        logging.info("Connecting to SQL")

        try:
            database = mysql.connector.connect(
                host="localhost",
                user="testuser",
                passwd="Develop_1"
            )
        except mysql.connector.Error as err:
            logging.error("Could not connect to SQL. {}".format(err.msg))
            return None

        logging.info("Connected to SQL successfully.")
        return database

    def close_connection(self, ) -> bool:

        logging.info("Closing SQL connection")
        try:
            self.database.close()
        except mysql.connector.Error as err:
            logging.error("Could not close sql connection. {}".format(err.msg))
            return False
        return True

    def database_creation(self) -> bool:
        result = self.drop_db()
        result = result and self.check_create_database()
        result = result and self.initialise_tables_list()
        result = result and self.populate_from_json()
        return result

    def populate_from_json(self) -> None:
        cursor = self.database.cursor()
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
            self.insert_query(cursor, query_insert_dictionary, dictionary_values)
            for next_word in next_dictionary.words:
                word_values = (next_dictionary.name,
                               next_word.spelling,
                               next_word.translation,
                               next_word.learning_index)
                self.insert_query(cursor, query_insert_word, word_values)

        self.commit()

    def select_query(self, cursor, query: str, values: List) -> bool:

        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not select values. {}".format(err.msg))
            return False
        return True

    def select_unconditional_query(self, cursor, query: str) -> bool:

        try:
            cursor.execute(query)
        except mysql.connector.Error as err:
            logging.error("Could not select values. {}".format(err.msg))
            return False
        return True

    def insert_query(self, cursor, query, values) -> bool:

        try:
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not insert values. {}".format(err.msg))
            return False
        return True

    def update_query(self, query, values) -> bool:

        try:
            cursor = self.database.cursor()
            cursor.execute(query, values)
        except mysql.connector.Error as err:
            logging.error("Could not update values. {}".format(err.msg))
            return False
        return True

    def check_sql(self, ) -> bool:

        try:
            cursor = self.database.cursor()
            cursor.execute("SHOW TABLES")
            for x in cursor:
                print(x)
        except mysql.connector.Error as err:
            logging.error("Could check SQL. {}".format(err.msg))
            return False
        return True

    def check_create_database(self) -> bool:

        # Check if DB exist and create
        logging.info("Connecting to SQL database 'DictionariesDB'")
        try:
            cursor = self.database.cursor()
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

    def drop_tables(self, ) -> None:

        logging.info("Dropping SQL tables")
        try:
            cursor = self.database.cursor()
            cursor.execute("DROP TABLE IF EXISTS words;")
            cursor.execute("DROP TABLE IF EXISTS dictionaries;")
            cursor.execute("DROP TABLE IF EXISTS languages;")
        except mysql.connector.Error as err:
            logging.error("Could not drop table. {}".format(err.msg))
            exit(1)

    def drop_db(self, ) -> bool:

        logging.info("Dropping database")
        try:
            cursor = self.database.cursor()
            cursor.execute("DROP DATABASE IF EXISTS DictionariesDB;")
        except mysql.connector.Error as err:
            logging.error("Could not database. {}".format(err.msg))
            return False
        return True

    def initialise_tables_list(self, ) -> bool:

        sql_tables: Dict[str, str] = {}
        sql_tables['languages'] = ("""
            CREATE TABLE 
               `languages` (
                   `language_name` varchar(25) NOT NULL PRIMARY KEY
                );
            """)

        sql_tables['dictionaries'] = ("""
            CREATE TABLE 
               `dictionaries` (
                   `dictionary_name` varchar(50) NOT NULL PRIMARY KEY, 
                   `native_language` varchar(25), 
                   `foreign_language` varchar(25), 
                   FOREIGN KEY (`native_language`) REFERENCES `languages`(`language_name`), 
                   FOREIGN KEY (`foreign_language`) REFERENCES `languages`(`language_name`) 
               );
            """)

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
            """)

        for table_name, table_description in sql_tables.items():
            if not self.check_create_table(table_name, table_description):
                return False
        return True

    # Create table
    def check_create_table(self, table_name, table_description) -> bool:

        logging.info("Checking table {}".format(table_name))
        try:
            cursor = self.database.cursor()
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

    def commit(self) -> bool:
        try:
            self.database.commit()
        except mysql.connector.Error as err:
            logging.error("Could not commit database. {}".format(err.msg))
            return False

        return True
