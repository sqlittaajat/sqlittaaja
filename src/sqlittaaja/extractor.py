import sys, getopt

# reads command line arguments
def readArgs():
    argv = sys.argv[1:]
    if not argv:
        print('-z <zipfile> -e <exercise>')
        sys.exit(2)

    zipfile = ''
    exercise = ''

    try:
        opts, args = getopt.getopt(argv,"hz:e:",["zipfile=","exercise="])
    except getopt.GetoptError:
        # error
        print ('-z <zipfile> -e <exercise>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            # help
            print ('-z <zipfile> -e <exercise>')
            sys.exit()
        elif opt in ("-z", "--zipfile"):
            # zip name
            zipfile = arg
        elif opt in ("-e", "--exercise"):
            # exercise name
            exercise = arg

    print(f"Zip file name {zipfile}")
    print(f"Exercise name {exercise}")
