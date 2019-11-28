import unittest
from Model.ModelConsole import ModelConsole
from Model.GameType import GameType
from Model.GameGenerator import GameGenerator
from Model.ModelSQL import ModelSQL
from Model.SQLType import SQLType


class ModelTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        super(ModelTests, self).__init__(*args, **kwargs)
        self.initialise_dictionaries()

    def initialise_dictionaries(self):

        self.model = ModelConsole()
        self.model.load_dictionaries()

    def test_game_generation(self):

        # Arrange
        # in initialisation

        for i in range(100):
            # Act
            game_rounds = self.model.generate_game(GameType.FindTranslation, i+1)
            # Assert
            self.assertEqual(i+1, len(game_rounds), "Rounds in game should be equal!")

    def test_automatic_games(self):

        # Arrange
        # in initialisation

        # Act
        result = True
        for i in range(100):
            game_rounds = self.model.generate_game(GameType.FindTranslation, 50)
            if game_rounds is None:
                result = False
            self.model.play_game(game_rounds, True)

            game_rounds = self.model.generate_game(GameType.FindSpelling, 50)
            if game_rounds is None:
                result = False
            self.model.play_game(game_rounds, True)

        # Assert
        self.assertEqual(result, True, "Automatic games did not work!")


class GameGeneratorTests(unittest.TestCase):

    def test_game_generation(self):

        # Arrange
        for i in range(4):
            # Act
            game = GameGenerator.generate_game(range(i), GameType.FindTranslation)

            # Assert
            self.assertIsNone(game, "No game if words less than 4!")

    def test_sort_lists(self):

        # Arrange
        my_list = list(range(500))

        for i in range(100):
            # Act
            new_list = GameGenerator.mix_list(my_list)
            new_list.sort()

            # Assert
            self.assertEqual(my_list, new_list, "List should be equal after mixing!")

    def test_sort_length(self):

        for i in range(100):
            # Arrange
            my_list = list(range(i))
            init_length = len(my_list)
            for j in range(i):
                # Act
                new_list = GameGenerator.mix_list(my_list)

                # Assert
                self.assertEqual(init_length, len(new_list), "Should be equal after mixing!")


class ModelSQLCases:

    class ModelSQLTests(unittest.TestCase):

        def __init__(self, *args, **kwargs):

            super(ModelSQLCases.ModelSQLTests, self).__init__(*args, **kwargs)
            self.initialise_sql()

        def initialise_sql(self):

            self.model_sql = ModelSQL()
            total_words_query = """
            SELECT 
                COUNT(spelling)
            FROM
                words
            """

            cursor = self.model_sql.database_connector.database.cursor
            if not self.model_sql.database_connector.execute_query(total_words_query):
                self.fail("Could not get total words in dictionaries!")

            self.total_words = cursor.fetchone()[0]

        def test_sql_game_all_words(self):

            # Arrange

            # Act
            game = self.model_sql.generate_game(GameType.FindTranslation)

            # Assert
            self.assertEqual(len(game), self.total_words, "Number of game rounds should be equal!")

            # Act
            game = self.model_sql.generate_game(GameType.FindSpelling)

            # Assert
            self.assertEqual(len(game), self.total_words, "Number of game rounds should be equal!")

        def test_sql_game_words_number(self):

            # Arrange
            for i in range(10, self.total_words):
                # Act
                game = self.model_sql.generate_game(GameType.FindTranslation, i)

                # Assert
                self.assertEqual(len(game), i, "Number of game rounds should be defined!")

                # Act
                game = self.model_sql.generate_game(GameType.FindSpelling, i)

                # Assert
                self.assertEqual(len(game), i, "Number of game rounds should be defined!")

        def test_sql_game_dictionaries(self):

            # Arrange
            dictionaries = list()
            dictionaries.append('Idioms')
            dictionaries.append('Everyday')
            words_number = 50

            # Act
            game = self.model_sql.generate_game(GameType.FindTranslation, words_number, dictionaries)

            # Assert
            self.assertEqual(len(game), words_number, "Number of game rounds should be defined!")


class ModelPostgreSQLTests(ModelSQLCases.ModelSQLTests):

    def initialise_sql(self):

        self.model_sql = ModelSQL()
        total_words_query = """
        SELECT 
            COUNT(spelling)
        FROM
            words
        """

        cursor = self.model_sql.database_connector.cursor
        if not self.model_sql.database_connector.execute_query(total_words_query):
            self.fail("Could not get total words in dictionaries!")

        self.total_words = cursor.fetchone()[0]


if __name__ == '__main__':
    unittest.main()
