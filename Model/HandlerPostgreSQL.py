import logging
from Model.HandlerSQL import HandlerSQL
import psycopg2


class HandlerPostgreSQL(HandlerSQL):

    database = None

    @staticmethod
    def sql_connection() -> bool:

        logging.info("Connecting to PostgreSQL")

        try:
            HandlerPostgreSQL.database = psycopg2.connect(
                host="localhost",
                user="testuser",
                passwd="Develop_1",
                database="DictionariesDB"
            )
        except psycopg2.Error as err:
            logging.error("Could not connect to MySQL. {}".format(err))
            return False

        logging.info("Connected to PostgreSQL successfully.")
        return True

    @staticmethod
    def check_sql() -> bool:

        try:
            cursor = HandlerPostgreSQL.database.cursor()
            cursor.execute("SELECT datname FROM pg_database Where datname = 'dictionariesdb")
            for x in cursor:
                print(x)
        except psycopg2.Error as err:
            logging.error("Could check SQL. {}".format(err))
            return False
        return True
