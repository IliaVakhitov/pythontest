import logging

import mysql.connector
import psycopg2

from Model.SQLType import SQLType
from Model.TablesMaker import TablesMaker
from View import view


class DatabaseConnector:

    def __init__(self, sql_type: SQLType = SQLType.PostgreSQL) -> None:

        self.sql_type = sql_type
        # TODO load values from config, it not defined, then use defaults
        self.username = view.input_str("SQL user name:")
        self.password = view.input_password("SQL user password:")
        self.database_name = "DictionariesDB"
        self.host = "localhost"

        self.database = self.sql_connection()
        self.connected = self.database is not None
        if self.connected:
            self.cursor = self.database.cursor()
            tables_maker = TablesMaker(self)
            self.connected = tables_maker.check_tables()
        else:
            self.cursor = None

    def sql_connection(self):

        """
        Create an SQL connection and return database
        :return:
            database: connected to SQL sever
        """
        logging.info(f"Connecting to {self.sql_type.name}")
        if self.sql_type == SQLType.MySQL:
            database = self.mysql_connection()
        elif self.sql_type == SQLType.PostgreSQL:
            database = self.postgresql_connection()
        else:
            logging.info(f"Undefined SQL type {self.sql_type.name}")
            return None

        logging.info(f"Connected to {self.sql_type.name} successful.")
        return database

    def mysql_connection(self):

        """
        Create an SQL connection and return database
        :return:
            database: connected to MySQL sever
        """
        try:
            database = mysql.connector.connect(
                host=self.host,
                user=self.username,
                passwd=self.password,
                database=self.database_name
            )
        except mysql.connector.Error as err:
            logging.error(f"Could not connect to {self.sql_type.name}")
            logging.error(f"Message: {err}")
            return None

        return database

    def postgresql_connection(self):

        """
        Create a connection and return database
        :return:
            database: connected to PostgreSQL sever
        """
        try:
            database = psycopg2.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database_name
            )
            database.autocommit = True

        except psycopg2.Error as err:
            logging.error(f"Could not connect to {self.sql_type.name}")
            logging.error(f"Message: {err}")
            return None

        return database

    def close_connection(self) -> bool:

        """
        Closing SQL connection
        :return:
        """
        logging.info("Closing SQL connection")
        try:
            self.database.close()
        except BaseException as err:
            logging.error("Error while closing sql connection")
            logging.error(f"{err}")
            return False

    def execute_query(self, query: str, values=None) -> bool:

        """
        Execute query
        :param query:str SQL query
        :param values:None or Collection Parameters of query
        :return:
            True: executed successful
            False: error printed in log.
        """
        try:
            if values is None or len(values) == 0:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)
        except BaseException as err:
            logging.error(f"Could not select values. {err}")
            return False

        return True

    def commit(self) -> bool:

        """
        Commit database changes
        :return:
            True successful
            False: error printed in log.
        """
        try:
            self.database.commit()
        except BaseException as err:
            logging.error(f"Could not commit database. {err}")
            return False

        return True
