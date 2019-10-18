from View import view
from Model import model

my_dict = model.Dictionary("English")
my_dict.add_new_entry("one", "один")
my_dict.add_new_entry("two", "два")
my_dict.add_new_entry("three", "три")
my_dict.add_new_entry("four", "четыре")

view.printStr(my_dict.name)
my_dict.write_to_json(my_dict.name + ".json")
view.printStr(my_dict.json_data)
