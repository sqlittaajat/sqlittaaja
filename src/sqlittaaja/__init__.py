from .extractor import extract
import sys
import getopt


def main():
    print("SQLittaaja")
    read_args()


def read_args():
    """Reads command line arguments."""

    argv = sys.argv[1:]
    if not argv:
        print("-z <zipfile> -e <exercise>")
        sys.exit(2)

    zip = ""
    exercise = ""

    try:
        opts, args = getopt.getopt(argv, "hz:e:", ["zipfile=", "exercise="])
    except getopt.GetoptError:
        # error
        print("-z <zipfile> -e <exercise>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            # help
            print("-z <zipfile> -e <exercise>")
            sys.exit()
        elif opt in ("-z", "--zipfile"):
            # zip name
            zip = arg
        elif opt in ("-e", "--exercise"):
            # exercise name
            exercise = arg

    files = extract(zip)
    print(files)
