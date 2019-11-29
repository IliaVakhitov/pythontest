from typing import List, Optional, Dict

from Model.SQLType import SQLType


class QueryManager:

    def __init__(self, sql_type: SQLType):
        self.sql_type = sql_type

    @staticmethod
    def total_words_query() -> str:
        return """
            SELECT 
                COUNT(spelling)
            FROM
                words
            """

    @staticmethod
    def query_insert_languages() -> str:
        return """
            INSERT INTO languages                 
                (language_name) 
            VALUES 
                ('English'), ('Russian')
            """

    @staticmethod
    def query_insert_dictionary() -> str:
        return """
            INSERT INTO dictionaries (
               dictionary_name,
               native_language, 
               foreign_language)
            VALUES 
               (%s, %s, %s);
            """

    @staticmethod
    def query_insert_word() -> str:
        return """
            INSERT INTO words (
               dictionary,
               spelling,
               translation,
               learning_index) 
            VALUES 
               (%s, %s, %s, %s);
            """

    def query_table_exists(self) -> str:

        if self.sql_type == SQLType.MySQL:
            return "SHOW TABLES LIKE %(table_name)s;"
        elif self.sql_type == SQLType.PostgreSQL:
            return """
                SELECT EXISTS 
                (
                    SELECT 1 
                    FROM information_schema.tables
                    WHERE table_catalog='DictionariesDB' 
                    AND table_name = %(table_name)s
                );
            """

    @staticmethod
    def query_drop_table(table_name: str) -> str:
        return f"DROP TABLE IF EXISTS {table_name};"


    @staticmethod
    def query_create_languages():
        return """
                CREATE TABLE 
                   languages (
                       language_name VARCHAR(25) NOT NULL PRIMARY KEY
                    );
                """

    @staticmethod
    def query_create_dictionaries():
        return """
            CREATE TABLE 
               dictionaries (
                   dictionary_name VARCHAR(50) NOT NULL PRIMARY KEY, 
                   native_language VARCHAR(25), 
                   foreign_language VARCHAR(25), 
                   FOREIGN KEY (native_language) REFERENCES languages(language_name), 
                   FOREIGN KEY (foreign_language) REFERENCES languages(language_name) 
               );
            """

    def query_create_words(self):
        column_type = "INT AUTO_INCREMENT" if self.sql_type == SQLType.MySQL else "SMALLSERIAL"
        return f""" CREATE TABLE 
               words (
                   id {column_type} NOT NULL  PRIMARY KEY, 
                   dictionary VARCHAR(50) NOT NULL, 
                   spelling VARCHAR(255) NOT NULL, 
                   translation VARCHAR(255) NOT NULL, 
                   learning_index SMALLINT NOT NULL, 
                   FOREIGN KEY (dictionary) REFERENCES dictionaries(dictionary_name) 
               );
            """

    @staticmethod
    def query_update_words():
        return """
            UPDATE 
                words
            SET 
                learning_index = %(learning_index)s
            WHERE 
                id = %(id)s;
            """

    def query_select_words(self,
                           word_limit: int = 0,
                           dictionaries: Optional[List[str]] = None) -> Dict:

        query_select_words = """
            SELECT
                id, 
                spelling, 
                translation,
                learning_index
            FROM
                words
            """

        # Condition is used if param dictionaries is defined
        dictionary_condition = """
            WHERE
                dictionary in (%s)
            """
        # Generating list of parameters for cursor query
        args: List = list()
        if dictionaries is not None and len(dictionaries) > 0:
            in_condition = ','.join(['%s'] * len(dictionaries))
            query_select_words += dictionary_condition % in_condition
            args = list(dictionaries)

        rand_function = "RAND()" if self.sql_type == SQLType.MySQL else "RANDOM()"
        query_select_words += f"""
                    ORDER BY 
                        {rand_function}
                    """

        # Condition is used if param word_limit if defined
        limit_condition = """
            LIMIT %s;
            """

        if word_limit != 0:
            query_select_words += limit_condition
            args.append(word_limit)

        return {'query_select_words': query_select_words, 'args': args}
