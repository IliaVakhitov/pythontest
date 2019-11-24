import logging
from typing import List, Dict

from Model.HandlerSQL import HandlerSQL
import psycopg2


class HandlerPostgreSQL(HandlerSQL):

    def __init__(self) -> None:
        self.database = self.sql_connection()
        self.connected = self.database is not None
        self.connected = self.connected and self.check_sql()

    def close_connection(self) -> bool:
        logging.info("Closing SQL connection")
        try:
            self.database.close()
        except psycopg2.Error as err:
            logging.error("Could not close sql connection. {}".format(err))
            return False

        return True

    def select_query(self, cursor, query: str, values: List) -> bool:
        pass

    def select_unconditional_query(self, cursor, query: str) -> bool:
        pass

    def insert_query(self, cursor, query, values) -> bool:
        pass

    def update_query(self, query, values) -> bool:
        pass

    def drop_tables(self) -> bool:
        logging.info("Dropping SQL tables")
        try:
            cursor = self.database.cursor()
            cursor.execute("DROP TABLE IF EXISTS words;")
            cursor.execute("DROP TABLE IF EXISTS dictionaries;")
            cursor.execute("DROP TABLE IF EXISTS languages;")
        except psycopg2.Error as err:
            logging.error(f"Could not drop table. {format(err.msg)}")
            return False
        logging.info("SQL tables dropped successful")
        return True

    def sql_connection(self):

        logging.info("Connecting to PostgreSQL")

        try:
            database = psycopg2.connect(
                host="localhost",
                user="testuser",
                password="Develop_1",
                database="DictionariesDB"
            )
            database.autocommit = True
        except psycopg2.Error as err:
            logging.error("Could not connect to PostgreSQL. {}".format(err))
            return None

        logging.info("Connected to PostgreSQL successfully.")

        return database

    def check_sql(self) -> bool:

        logging.info("Checking database")
        try:
            cursor = self.database.cursor()
            cursor.execute("SELECT datname FROM pg_database Where datname = \'DictionariesDB\'")
            for x in cursor:
                logging.info(x)
        except psycopg2.Error as err:
            logging.error("Could not check SQL. {}".format(err))
            return False

        return True

    def check_create_database(self) -> bool:

        # Check if DB exist and create
        logging.info("Connecting to SQL database 'DictionariesDB'")
        try:
            cursor = self.database.cursor()
            cursor.execute("SELECT datname FROM pg_database Where datname = \'DictionariesDB\'")
            db_exist = cursor.fetchone()
            if db_exist is None:
                query_create = """
                    CREATE DATABASE \"DictionariesDB\"
                        ENCODING 'UTF8';
                    """
                cursor.execute(query_create)
                self.commit()

        except psycopg2.Error as err:
            logging.error("Could not create database. {}".format(err))
            return False

        logging.info("Connected to database successfully.")
        return True

    def database_creation(self) -> bool:
        result = self.drop_db()
        result = result and self.check_create_database()
        result = result and self.initialise_tables_list()
        result = result and self.populate_from_json()
        return result

    def populate_from_json(self) -> bool:

        return super().populate_from_json()

    def initialise_tables_list(self) -> bool:
        sql_tables: Dict[str, str] = {}
        sql_tables['languages'] = ("""
                    CREATE TABLE 
                       \"languages\" (
                           \"language_name\" VARCHAR(25) NOT NULL PRIMARY KEY
                        );
                    """)

        sql_tables['dictionaries'] = ("""
                    CREATE TABLE 
                       dictionaries (
                           \"dictionary_name\" VARCHAR(50) NOT NULL PRIMARY KEY, 
                           \"native_language\" VARCHAR(25), 
                           \"foreign_language\" VARCHAR(25), 
                           FOREIGN KEY (\"native_language\") REFERENCES \"languages\"(\"language_name\"), 
                           FOREIGN KEY (\"foreign_language\") REFERENCES \"languages\"(\"language_name\") 
                       );
                    """)

        sql_tables['words'] = ("""
                    CREATE TABLE 
                       \"words\" (
                           \"id\" SMALLINT NOT NULL  PRIMARY KEY, 
                           \"dictionary\" VARCHAR(50) NOT NULL, 
                           \"spelling\" VARCHAR(255) NOT NULL, 
                           \"translation\" VARCHAR(255) NOT NULL, 
                           \"learning_index\" SMALLINT NOT NULL, 
                           FOREIGN KEY (\"dictionary\") REFERENCES \"dictionaries\"(\"dictionary_name\") 
                       );
                    """)

        for table_name, table_description in sql_tables.items():
            if not self.check_create_table(table_name, table_description):
                logging.error(f"Could not create table {table_name}")
                return False

        return True

    def check_create_table(self, table_name, table_description) -> bool:

        logging.info(f"Checking table {format(table_name)}")
        try:
            cursor = self.database.cursor()
            query = """
                SELECT EXISTS 
                (
                    SELECT 1 
                    FROM information_schema.tables
                    WHERE table_catalog='DictionariesDB' 
                    AND table_name = %(table_name)s
                );
            """
            cursor.execute(query, {'table_name': table_name})
            table_exist = cursor.fetchone()
            if table_exist[0] is False:
                cursor.execute(table_description)
                logging.info(f"Table {table_name} created")
            else:
                logging.info("Table {} already exist".format(table_name))
        except psycopg2.Error as err:
            logging.error(f"Could not create table. {err}")
            return False

        return True

    def drop_db(self) -> bool:
        return self.drop_tables()

    def commit(self) -> bool:
        try:
            self.database.commit()
        except psycopg2.Error as err:
            logging.error("Could not commit database. {}".format(err))
            return False

        return True
