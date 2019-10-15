from View import view
from Model import model



dict = model.Dictionary()
dict.addNewEntry("one", "один")
dict.addNewEntry("two", "два")
dict.addNewEntry("three", "три")
dict.addNewEntry("four", "четыре")
view.printStr(dict.printWords())

