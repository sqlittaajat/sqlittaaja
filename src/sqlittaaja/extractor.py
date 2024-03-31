import sys, getopt, zipfile


# reads command line arguments
def readArgs():
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

    extract(zip)


# extracts the zip file
def extract(file):
    filepath = "src/testfiles/"
    try:
        with zipfile.ZipFile(filepath + file, "r") as zip_ref:
            zip_ref.extractall(filepath + "extracted")
        print(f"File {file} extracted to src/testfiles/extracted")
    except:
        print("Error with unzipping")
