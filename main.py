import sys

from src.scraper import main


def run(argv):
    if len(argv) == 1:
        print("No ARGV")
    elif argv[1] == "-m":
        _DEV = argv[2] == "DEV"
        _TEST = argv[3] == "TEST"
        main(self="", dev=_DEV, test=_TEST)


if __name__ == '__main__':
    run(sys.argv)
