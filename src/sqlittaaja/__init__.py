from .extractor import extract, zipped_file, find_init_scripts, student_infos
from .checker import init_database
import argparse


def main():
    args = read_args()

    with args.answers as answers:
        base_db = init_database(find_init_scripts(extract(answers)))
        print("\n".join(base_db.iterdump()))

    with args.exercises as exercises:
        extracted = extract(exercises)
        print(student_infos(extracted.keys()))


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
