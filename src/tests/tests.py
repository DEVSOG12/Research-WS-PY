# from src.scraper import main

from os import listdir
from os.path import isfile, join


class Test(object):

    def __init__(self, folder_name, map_of_items):
        self.folder_name = folder_name
        self.map_of_items = map_of_items

    def test1(self):
        only_files = [f for f in listdir(self.folder_name) if isfile(join(self.folder_name, f))]
        count = 0
        for i in list(self.map_of_items.keys()):
            name_of_file = "{0}_{1}_{2}_{3}.pdf".format(self.map_of_items[str(i)]["Organization Name"],
                                                        self.map_of_items[str(i)]["Topic area"],
                                                        self.map_of_items[str(i)][
                                                            "type"], str(i))
            if only_files.__contains__(name_of_file):
                count += 1
        if count == len(only_files):
            print("Test Passed")
        else:
            print("Test Failed")
            print("")


# run_test()