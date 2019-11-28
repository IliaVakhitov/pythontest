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
            self.check_database()
        else:
            self.cursor = None

    def sql_connection(self):

        """
        TODO
        :return:
        """
        logging.info(f"Connecting to {self.sql_type}")
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
            logging.error(f"Could not connect to {self.sql_type}")
            logging.error(f"Message: {err}")
            return None

        logging.info(f"Connected to {self.sql_type} successful.")
        return database

    def check_database(self) -> bool:

        """
        Check table languages
        If table doesn't exist, call tables_creator and fill dada from JSON
        :return:
            True - created successful
            False - error in creating tables
        """

        logging.info(f"Checking connection to SQL database \'{self.database_name}\'")
        table_exist = None
        try:
            query = ""
            if self.sql_type == SQLType.MySQL:
                query = "SHOW TABLES LIKE '%(table_name)s';"
            elif self.sql_type == SQLType.PostgreSQL:
                query = """
                    SELECT EXISTS 
                    (
                        SELECT 1 
                        FROM information_schema.tables
                        WHERE table_catalog='DictionariesDB' 
                        AND table_name = %(table_name)s
                    );
                """
            self.cursor.execute(query, {'table_name': 'languages'})
            table_exist = self.cursor.fetchone()

        except BaseException as err:
            logging.error(f"Could not check table \'languages\' {err}")
            return False

        # TODO
        if table_exist is None:
            tables_creator = TablesMaker(self)
        elif table_exist[0] is False:
            tables_creator = TablesMaker(self)
        else:
            logging.info(f"Database \'{self.database_name}\' tables checked.")
        return True

    def close_connection(self, ) -> bool:

        """

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
