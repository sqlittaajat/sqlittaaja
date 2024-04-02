import sys
import getopt
import zipfile
import os


def readArgs():
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


def extract(file):
    """Reads the zip file and returns the contents."""

    try:
        with zipfile.ZipFile(file, "r") as zip_ref:
            return {name: zip_ref.read(name) for name in zip_ref.namelist()}
    except:
        print("Error with unzipping")
