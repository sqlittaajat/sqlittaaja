import zipfile
import argparse


def extract(file: zipfile.ZipFile):
    """Reads a ZIP file and returns the contents."""

    with file as zip:
        return {name: zip.read(name).decode() for name in zip.namelist()}


def zipped_file(path):
    """ZIP file type for `argparse`. Use as type for `add_argument`."""

    try:
        return zipfile.ZipFile(path, "r")
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f"\"{path}\" file does not exist")
    except zipfile.BadZipfile:
        raise argparse.ArgumentTypeError(f"\"{path}\" is not a ZIP file")
