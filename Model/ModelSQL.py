import logging.handlers
import mysql.connector
from typing import Dict


# MYSQL connection
class ModelSQL:
    my_db = None

    @staticmethod
    def initialisation():
        ModelSQL.sql_connection()
        ModelSQL.initialise_tables_list()
        ModelSQL.check_sql()

    @staticmethod
    def check_sql():
        my_cursor = ModelSQL.my_db.cursor()
        my_cursor.execute("SHOW TABLES")
        for x in my_cursor:
            print(x)


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
            exit()

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

        logging.info("Connected to MySQL successfully.")

    @staticmethod
    def close_connection() -> None:
        logging.info("Closing SQL connection")
        ModelSQL.my_db.close()

    @staticmethod
    def initialise_tables_list():
        my_sql_tables: Dict[str,str] = {}
        my_sql_tables['languages'] = (
            "CREATE TABLE "
            "   `languages` ("
            "       `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "       `name` varchar(255)"
            "    );"
        )

        my_sql_tables['dictionaries'] = (
            "CREATE TABLE "
            "   `dictionaries` ("
            "       `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
            "       `name` varchar(255), "
            "       `native_language_id` INT, "
            "       `foreign_language_id` INT, "
            "       FOREIGN KEY (`native_language_id`) REFERENCES `languages`(`id`), "
            "       FOREIGN KEY (`foreign_language_id`) REFERENCES `languages`(`id`) "
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
            stmt = "SHOW TABLES LIKE '{}';".format(table_name)
            my_cursor.execute(stmt)
            table_exist = my_cursor.fetchone()
            if table_exist is None:
                my_cursor.execute(table_description)
            else:
                logging.info("Table {} already exist".format(table_name))
        except mysql.connector.Error as err:
            logging.error("Could not create table. {}".format(err.msg))
            exit(1)
