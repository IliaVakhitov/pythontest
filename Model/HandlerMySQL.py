import logging
import mysql.connector
from mysql.connector import Error
from typing import Dict, List
from Model.HandlerSQL import HandlerSQL


class HandlerMySQL(HandlerSQL):

    def __init__(self) -> None:
        super().__init__()

    def sql_connection(self):

        logging.info("Connecting to MySQL")

        try:
            database = mysql.connector.connect(
                host="localhost",
                user=self.username,
                passwd=self.password
            )
        except Error as err:
            logging.error(f"Could not connect to MySQL. {err.msg}")
            return None

        logging.info("Connected to MySQL successfully.")
        return database

    def close_connection(self, ) -> bool:

        logging.info("Closing SQL connection")
        try:
            self.database.close()
        except Error.msg as err:
            logging.error(f"Could not close sql connection. {err.msg}")
            return False
        return True

    def database_creation(self) -> bool:

        result = self.initialise_tables_list()
        result = result and self.populate_from_json()
        return result

    def select_query(self, cursor, query: str, values: List) -> bool:

        try:
            cursor.execute(query, values)
        except Error.msg as err:
            logging.error(f"Could not select values. {err.msg}")
            return False
        return True

    def select_unconditional_query(self, cursor, query: str) -> bool:

        try:
            cursor.execute(query)
        except Error.msg as err:
            logging.error(f"Could not select values. {err.msg}")
            return False
        return True

    def insert_query(self, cursor, query, values) -> bool:

        try:
            cursor.execute(query, values)
        except Error.msg as err:
            logging.error(f"Could not insert values. {err.msg}")
            return False
        return True

    def update_query(self, query, values) -> bool:

        try:
            cursor = self.database.cursor()
            cursor.execute(query, values)
        except Error.msg as err:
            logging.error(f"Could not update values. {err.msg}")
            return False
        return True

    def check_create_database(self) -> bool:
        """
        Check if DB exist
        If not create DB, tables and fill dada from JSON
        :return:
            True - created successful
            False - error in creating db
        """

        logging.info("Connecting to SQL database 'DictionariesDB'")
        try:
            cursor = self.database.cursor()
            cursor.execute("SHOW DATABASES LIKE 'DictionariesDB';")
            db_exist = cursor.fetchone()
            if db_exist is None:
                cursor.execute("CREATE DATABASE DictionariesDB character set utf8;")
                cursor.execute("USE DictionariesDB;")
                self.database_creation()

        except Error.msg as err:
            logging.error(f"Could not create database. {err.msg}")
            return False
        cursor.execute("USE DictionariesDB;")
        logging.info("Connected to database successfully.")
        return True

    def drop_tables(self) -> bool:

        logging.info("Dropping SQL tables")
        try:
            cursor = self.database.cursor()
            cursor.execute("DROP TABLE IF EXISTS words;")
            cursor.execute("DROP TABLE IF EXISTS dictionaries;")
            cursor.execute("DROP TABLE IF EXISTS languages;")
        except Error.msg as err:
            logging.error(f"Could not drop table. {err.msg}")
            return False
        logging.info("SQL tables dropped successful")
        return True

    def drop_db(self) -> bool:

        logging.info("Dropping database")
        try:
            cursor = self.database.cursor()
            cursor.execute("DROP DATABASE IF EXISTS DictionariesDB;")
        except Error.msg as err:
            logging.error(f"Could not drop database. {err.msg}")
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

        logging.info(f"Checking table \'{table_name}")
        try:
            cursor = self.database.cursor()
            query = f"SHOW TABLES LIKE '{table_name}';"
            cursor.execute(query)
            table_exist = cursor.fetchone()
            if table_exist is None:
                cursor.execute(table_description)
                logging.info(f"Table {table_name} created")
            else:
                logging.info(f"Table {table_name} already exist")
        except Error.msg as err:
            logging.error(f"Could not create table. {err.msg}")
            return False
        return True

    def commit(self) -> bool:
        try:
            self.database.commit()
        except Error.msg as err:
            logging.error(f"Could not commit database. {err.msg}")
            return False

        return True

    def populate_from_json(self) -> bool:
        super().populate_from_json()