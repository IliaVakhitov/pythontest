import unittest
from Model.model import Model


class ModelTests(unittest.TestCase):

    def test_game_generation(self):
        model = Model()
        model.load_dictionaries()
        for i in range(16):
            game_rounds = model.generate_game(i+1)
            self.assertEqual(i+1, len(game_rounds), "Rounds in game should be equal!")

    def test_sort_length(self):
        model = Model()
        for i in range(100):
            my_list = list(range(i))
            init_length = len(my_list)
            for j in range(i):
                new_list = model.mix_list(my_list)
                self.assertEqual(init_length, len(new_list), "Should be equal!")

    def test_random_translation(self):
        # TODO make up this test
        model = Model()
        model.load_dictionaries()

    def test_sort_lists(self):
        model = Model()
        my_list = list(range(500))
        for i in range(100):
            new_list = model.mix_list(my_list)
            new_list.sort()
            self.assertEqual(my_list, new_list, "List should be equal after sorting!")


if __name__ == '__main__':
    unittest.main()