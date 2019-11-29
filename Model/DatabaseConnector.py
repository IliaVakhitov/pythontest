import logging
import mysql.connector
import psycopg2

from Model.TablesMaker import TablesMaker
from Model.SQLType import SQLType
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
        TODO
        :return:
        """
        logging.info(f"Connecting to {self.sql_type.name}")
        database = None
        try:
            if self.sql_type == SQLType.MySQL:
                database = mysql.connector.connect(
                    host=self.host,
                    user=self.username,
                    passwd=self.password,
                    database=self.database_name
                )
            elif self.sql_type == SQLType.PostgreSQL:
                database = psycopg2.connect(
                    host=self.host,
                    user=self.username,
                    password=self.password,
                    database=self.database_name
                )
                database.autocommit = True

        except BaseException as err:
            logging.error(f"Could not connect to {self.sql_type.name}")
            logging.error(f"Message: {err}")
            return None

        logging.info(f"Connected to {self.sql_type.name} successful.")
        return database

    def close_connection(self) -> bool:

        """
        TODO
        :return:
        """
        logging.info("Closing SQL connection")
        try:
            self.database.close()
        except BaseException as err:
            logging.error("Could not close sql connection. {}".format(err))
            return False

    def execute_query(self, query: str, values=None) -> bool:

        """
        TODO
        :param query:
        :param values:
        :return:
        """
        try:
            if values is None or len(values) == 0:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)
        except BaseException as err:
            logging.error("Could not select values. {}".format(err))
            return False
        return True

    def commit(self) -> bool:

        """
        TODO
        :return:
        """
        try:
            self.database.commit()
        except BaseException as err:
            logging.error(f"Could not commit database. {err}")
            return False

        return True
