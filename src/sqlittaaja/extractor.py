from zipfile import ZipFile, BadZipfile
from argparse import ArgumentTypeError
import os


def extract(file: ZipFile) -> dict[str, str]:
    """Reads a ZIP file and returns the contents."""

    with file as zip:
        return {
            name: zip.read(name).decode()
            for name in
            # Filter out directories.
            filter(lambda name: not name.endswith(os.path.sep), zip.namelist())
        }


def zipped_file(path: str) -> ZipFile:
    """ZIP file type for `argparse`. Use as type for `add_argument`."""

    try:
        return ZipFile(path, "r")
    except FileNotFoundError:
        raise ArgumentTypeError(f'"{path}" file does not exist')
    except BadZipfile:
        raise ArgumentTypeError(f'"{path}" is not a ZIP file')


def find_init_scripts(contents: dict[str, str]) -> str:
    """Find SQL initialization scripts."""

    # We want to use two lists here as the creation tables should come before
    # population tables.
    create_tables = []
    populate_tables = []

    for path in contents:
        name, ext = os.path.splitext(os.path.split(path)[1])
        # Skip everything that isn't a SQL file.
        if ext != ".sql":
            continue

        # Append to the correct table.
        if name.endswith("create_table"):
            create_tables.append(path)
        elif name.endswith("populate_table"):
            populate_tables.append(path)

    all_tables = create_tables + populate_tables
    return "\n".join(contents[name] for name in all_tables)


def student_info(name: str) -> (str, str):
    """Extract student information from file path."""

    dir = name.split(os.path.sep)[0]
    parts = dir.split("_")
    # First should be student's name and second some ID or something.
    return (parts[0], parts[1])
