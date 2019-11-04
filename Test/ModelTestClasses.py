import unittest
from Model.Model import Model, GameGenerator, GameType


class ModelTests(unittest.TestCase):

    def test_game_generation(self):
        model = Model()
        model.load_dictionaries()
        for i in range(100):
            game_rounds = model.generate_game(GameType.FindTranslation, i+1)
            self.assertEqual(i+1, len(game_rounds), "Rounds in game should be equal!")

    def test_sort_length(self):
        for i in range(100):
            my_list = list(range(i))
            init_length = len(my_list)
            for j in range(i):
                new_list = GameGenerator.mix_list(my_list)
                self.assertEqual(init_length, len(new_list), "Should be equal!")

    def test_automatic_games(self):
        my_model = Model()
        my_model.load_dictionaries()
        for i in range(100):
            game_rounds = my_model.generate_game(GameType.FindTranslation, 50)
            if game_rounds is None:
                exit()
            my_model.play_game(game_rounds, True)

            game_rounds = my_model.generate_game(GameType.FindWord, 50)
            if game_rounds is None:
                exit()
            my_model.play_game(game_rounds, True)

        my_model.save_dictionaries()

    def test_sort_lists(self):
        my_list = list(range(500))
        for i in range(100):
            new_list = GameGenerator.mix_list(my_list)
            new_list.sort()
            self.assertEqual(my_list, new_list, "List should be equal after sorting!")


if __name__ == '__main__':
    unittest.main()
