import logging
from typing import Dict

from Model.ModelConsole import ModelConsole
from Model.SQLType import SQLType


class TablesMaker:

    def __init__(self, database_connector):
        self.database_connector = database_connector
        self.database_creation()

    def populate_from_json(self) -> bool:
        cursor = self.database_connector.cursor
        query = """
            INSERT INTO languages                 
                (language_name) 
            VALUES 
                ('English'), ('Russian')
            """
        try:
            cursor.execute(query)
        except BaseException as err:
            logging.error(f"Could insert values. {err}")
            return False

        model = ModelConsole()
        model.load_dictionaries()
        model.reset_progress(model.words)

        query_insert_dictionary = """
            INSERT INTO dictionaries (
               dictionary_name,
               native_language, 
               foreign_language)
            VALUES 
               (%s, %s, %s);
            """

        query_insert_word = """
            INSERT INTO words (
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

            self.database_connector.execute_query(query_insert_dictionary, dictionary_values)
            for next_word in next_dictionary.words:
                word_values = (next_dictionary.name,
                               next_word.spelling,
                               next_word.translation,
                               next_word.learning_index)
                self.database_connector.execute_query(query_insert_word, word_values)

        self.database_connector.commit()

        return True

    def database_creation(self) -> bool:

        result = self.drop_tables()
        result = result and self.initialise_tables_list()
        result = result and self.populate_from_json()
        return result

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
        column_type = "INT" if self.database_connector.sql_type == SQLType.MySQL else "SMALLSERIAL"
        sql_tables['words'] = (f"""
                    CREATE TABLE 
                       \"words\" (
                           \"id\" {column_type} NOT NULL  PRIMARY KEY, 
                           \"dictionary\" VARCHAR(50) NOT NULL, 
                           \"spelling\" VARCHAR(255) NOT NULL, 
                           \"translation\" VARCHAR(255) NOT NULL, 
                           \"learning_index\" SMALLINT NOT NULL, 
                           FOREIGN KEY (\"dictionary\") REFERENCES \"dictionaries\"(\"dictionary_name\") 
                       );
                    """)

        for table_name, table_description in sql_tables.items():
            if not self.check_create_table(table_name, table_description):
                logging.error(f"Could not create table \'{table_name}\'")
                return False

        return True

    def check_create_table(self, table_name, table_description) -> bool:

        """
        TODO
        :param table_name:
        :param table_description:
        :return:
        """

        logging.info(f"Checking table \'{format(table_name)}\'")
        try:
            cursor = self.database_connector.cursor
            query = ""
            if self.database_connector.sql_type == SQLType.MySQL:
                query = "SHOW TABLES LIKE '%(table_name)s';"
            elif self.database_connector.sql_type == SQLType.PostgreSQL:
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
            # TODO
            if table_exist is None:
                cursor.execute(table_description)
                logging.info(f"Table \'{table_name}\' created")
            elif table_exist[0] is False:
                cursor.execute(table_description)
                logging.info(f"Table \'{table_name}\' created")
            else:
                logging.info(f"Table \'{table_name}\' already exist")

        except BaseException as err:
            logging.error(f"Could not create table \'{table_name}\' {err}")
            return False

        return True

    def drop_tables(self) -> bool:

        """

        :return:
        """
        logging.info("Dropping SQL tables")
        try:
            cursor = self.database_connector.cursor
            cursor.execute("DROP TABLE IF EXISTS words;")
            cursor.execute("DROP TABLE IF EXISTS dictionaries;")
            cursor.execute("DROP TABLE IF EXISTS languages;")
        except BaseException as err:
            logging.error(f"Could not drop table. {format(err)}")
            return False

        logging.info("SQL tables dropped successful")
        return True
