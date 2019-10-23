from View import view
from Model import Dictionary


my_dict = Dictionary.Dictionary("")
my_dict.read_from_json("Numbers.json")
view.print_str(my_dict.print_information())
