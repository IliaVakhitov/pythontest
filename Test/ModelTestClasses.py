import unittest
from Model.model import mix_list


class ModelTests(unittest.TestCase):

    def test_sort_length(self):
        my_list = list(range(50))
        init_length = len(my_list)
        for i in range(100):
            new_list = mix_list(my_list)
            self.assertEqual(init_length, len(new_list), "Should be equal!")

    def test_sort_lists(self):
        my_list = list(range(50))
        for i in range(100):
            new_list = mix_list(my_list)
            new_list.sort()
            self.assertEqual(my_list, new_list, "List should be equal after sorting!")


if __name__ == '__main__':
    unittest.main()