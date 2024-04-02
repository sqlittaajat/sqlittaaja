from .extractor import extract, zipped_file, find_init_scripts
import argparse


def main():
    args = read_args()
    with args.answers as answers:
        print(find_init_scripts(extract(answers)))
    with args.exercises as exercises:
        print(extract(exercises))


def read_args():
    """Reads command line arguments."""

    parser = argparse.ArgumentParser(description="Check SQLite exercises",
                                     epilog="Created by TIKO")

    parser.add_argument("answers",
                        type=zipped_file,
                        help="correct answers ZIP file")
    parser.add_argument("exercises",
                        type=zipped_file,
                        help="exercises ZIP file")
    parser.add_argument("-e", "--exercise",
                        type=int,
                        help="check a specific exercise")

    return parser.parse_args()
