from zipfile import ZipFile
import os


def extract(path: str) -> dict[str, str]:
    """Reads a ZIP file and returns the contents."""

    with ZipFile(path, "r") as zip:
        return {
            name: zip.read(name).decode()
            for name in
            # Filter out directories.
            filter(lambda name: not name.endswith(os.path.sep), zip.namelist())
        }


def student_info(name: str) -> str:
    """Extract student information (name) from file path."""

    dir = name.split(os.path.sep)[0]
    parts = dir.split("_")
    # First should be student's name.
    return parts[0]
