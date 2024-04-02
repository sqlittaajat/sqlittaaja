import zipfile


def extract(file):
    """Reads the zip file and returns the contents."""

    try:
        with zipfile.ZipFile(file, "r") as zip_ref:
            return {name: zip_ref.read(name) for name in zip_ref.namelist()}
    except Exception:
        print("Error with unzipping")
