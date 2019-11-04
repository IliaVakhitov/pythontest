import logging.handlers
import mysql.connector
from typing import Dict

# MYSQL connection
from Model.Model import Model


class ModelSQL:
    my_db = None

    @staticmethod
    def initialisation():

        ModelSQL.sql_connection()
        ModelSQL.drop_db()
        ModelSQL.create_database()
        ModelSQL.initialise_tables_list()
        ModelSQL.populate_from_json()

    @staticmethod
    def populate_from_json():
        my_cursor = ModelSQL.my_db.cursor()
        my_query = "INSERT IGNORE INTO languages (name) VALUES ('English'), ('Russian')"
        try:
            my_cursor.execute(my_query)
        except mysql.connector.Error as err:
            logging.error("Could insert values. {}".format(err.msg))
            exit(1)

        # ModelSQL.my_db.commit()

        my_model = Model()
        my_model.load_dictionaries()
        my_query_insert_dictionary = \
            "INSERT IGNORE INTO dictionaries (" \
            "   name," \
            "   native_language, " \
            "   foreign_language) " \
            "VALUES " \
            "   (%s, %s, %s);"
        my_query_insert_word = \
            "INSERT IGNORE INTO words (" \
            "   dictionary," \
            "   spelling," \
            "   translation," \
            "   learning_index) " \
            "VALUES " \
            "   (%s, %s, %s, %s);"

        for next_dictionary in my_model.my_dictionaries:
            dictionary_values = (next_dictionary.name,
                                 next_dictionary.native_language,
                                 next_dictionary.foreign_language)
            ModelSQL.insert_query(my_cursor, my_query_insert_dictionary, dictionary_values)
            for next_word in next_dictionary.words:
                word_values = (next_dictionary.name,
                               next_word.word,
                               next_word.translation,
                               next_word.learning_index)
                ModelSQL.insert_query(my_cursor, my_query_insert_word, word_values)

        ModelSQL.my_db.commit()

    @staticmethod
    def insert_query(my_cursor, my_query, values):
        try:
            my_cursor.execute(my_query, values)
        except mysql.connector.Error as err:
            logging.error("Could insert values. {}".format(err.msg))
            exit(1)

    @staticmethod
    def check_sql():
        try:
            my_cursor = ModelSQL.my_db.cursor()
            my_cursor.execute("SHOW TABLES")
            for x in my_cursor:
                print(x)
        except mysql.connector.Error as err:
            logging.error("Could check MySQL. {}".format(err.msg))
            exit(1)

    @staticmethod
    def sql_connection() -> None:
        logging.info("Connecting to MySQL")
        try:
            ModelSQL.my_db = mysql.connector.connect(
                host="localhost",
                user="test_user",
                passwd="Developer"
            )
        except mysql.connector.Error as err:
            logging.error("Could not connect to MySQL. {}".format(err.msg))
            exit(1)

        logging.info("Connected to MySQL successfully.")

    @staticmethod
    def create_database() -> None:
        # Check if DB exist and create
        logging.info("Connecting to SQL database 'DictionariesDB'")
        try:
            my_cursor = ModelSQL.my_db.cursor()
            my_cursor.execute("SHOW DATABASES LIKE 'DictionariesDB';")
            db_exist = my_cursor.fetchone()
            if db_exist is None:
                my_cursor.execute("CREATE DATABASE DictionariesDB;")
            my_cursor.execute("USE DictionariesDB;")
        except mysql.connector.Error as err:
            logging.error("Could not create database. {}".format(err.msg))
            exit(1)

        logging.info("Connected to database successfully.")

    @staticmethod
    def close_connection() -> None:
        logging.info("Closing SQL connection")
        ModelSQL.my_db.close()

    @staticmethod
    def drop_tables() -> None:
        logging.info("Dropping SQL tables")
        try:
            my_cursor = ModelSQL.my_db.cursor()
            my_cursor.execute("DROP TABLE IF EXISTS words;")
            my_cursor.execute("DROP TABLE IF EXISTS dictionaries;")
            my_cursor.execute("DROP TABLE IF EXISTS languages;")
        except mysql.connector.Error as err:
            logging.error("Could not drop table. {}".format(err.msg))
            exit(1)

    @staticmethod
    def drop_db() -> None:
        logging.info("Dropping database")
        try:
            my_cursor = ModelSQL.my_db.cursor()
            my_cursor.execute("DROP DATABASE IF EXISTS DictionariesDB;")
        except mysql.connector.Error as err:
            logging.error("Could not database. {}".format(err.msg))
            exit(1)

    @staticmethod
    def initialise_tables_list():
        my_sql_tables: Dict[str, str] = {}
        my_sql_tables['languages'] = (
            "CREATE TABLE "
            "   `languages` ("
            "       `name` varchar(25) NOT NULL PRIMARY KEY"
            "    );"
        )

        my_sql_tables['dictionaries'] = (
            "CREATE TABLE "
            "   `dictionaries` ("
            "       `name` varchar(50) NOT NULL PRIMARY KEY, "
            "       `native_language` varchar(25), "
            "       `foreign_language` varchar(25), "
            "       FOREIGN KEY (`native_language`) REFERENCES `languages`(`name`), "
            "       FOREIGN KEY (`foreign_language`) REFERENCES `languages`(`name`) "
            "   );"
        )

        my_sql_tables['words'] = (
            "CREATE TABLE "
            "   `words` ("
            "       `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "       `dictionary` varchar(50) NOT NULL, "
            "       `spelling` varchar(255) NOT NULL, "
            "       `translation` varchar(255) NOT NULL, "
            "       `learning_index` INT(3) NOT NULL, "
            "       FOREIGN KEY (`dictionary`) REFERENCES `dictionaries`(`name`) "
            "   );"
        )

        for table_name, table_description in my_sql_tables.items():
            ModelSQL.check_create_table(table_name, table_description)

    # Creating tables
    @staticmethod
    def check_create_table(table_name, table_description):
        logging.info("Checking table {}".format(table_name))
        try:
            my_cursor = ModelSQL.my_db.cursor()
            my_query = "SHOW TABLES LIKE '{}';".format(table_name)
            my_cursor.execute(my_query)
            table_exist = my_cursor.fetchone()
            if table_exist is None:
                my_cursor.execute(table_description)
            else:
                logging.info("Table {} already exist".format(table_name))
        except mysql.connector.Error as err:
            logging.error("Could not create table. {}".format(err.msg))
            exit(1)
