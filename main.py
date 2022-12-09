import os
import shutil
import sys

from src.scraper import main


# Function to extract all txt files from ./output and save them to ./liwc/ in the folder structure of ./output
def extract_txt():
    for root, dirs, files in os.walk("./outputs"):
        for file in files:
            if file.endswith(".txt"):
                # Check if the folders exist and create them if they don't
                if not os.path.exists("./liwc/" + root[10:]):
                    os.makedirs("./liwc/" + root[10:])
                # Copy the file to the new folder

                shutil.copy(os.path.join(root, file), "./liwc/" + root[10:] + "/" + file)
                # shutil.copy(os.path.join(root, file), os.path.join("./liwc", root[9:]))
                print("Copied " + file + " to " + os.path.join("./liwc", root[9:]))


def run(argv):
    if len(argv) == 1:
        print("No ARGV")
    elif argv[1] == "-m":
        _DEV = argv[2] == "DEV"
        _TEST = argv[3] == "TEST"
        main(dev=_DEV, test=_TEST)


if __name__ == '__main__':
    run(sys.argv)
    # extract_txt()
