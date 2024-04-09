import argparse
from typing import Any


class ValidationError(Exception):
    """Error validating the configuration."""

    pass


class MissingSectionError(ValidationError):
    """Some section is missing from the configuration."""

    def __init__(self, section: str):
        super().__init__(f"{section} section missing")


class MissingValueError(ValidationError):
    """Some value is missing from the configuration's section."""

    def __init__(self, section: str, value: str):
        super().__init__(f"{value} value missing in the {section} section")


def validate_config(config: dict[str, Any]):
    """Validate the configuration."""

    if config.get("answer") is None:
        raise MissingSectionError("answer")
    if config.get("exercise") is None:
        raise MissingSectionError("exercise")

    if config["answer"].get("exercise") is None:
        raise MissingValueError("answer", "exercise")
    if config["exercise"].get("path") is None:
        raise MissingValueError("exercise", "path")


def read_args():
    """Reads command line arguments."""

    parser = argparse.ArgumentParser(
        description="Check SQLite exercises", epilog="Created by TIKO"
    )

    parser.add_argument(
        "-c",
        "--config",
        type=argparse.FileType("rb"),
        default="config.toml",
        help="configuration file for the exercises (in TOML format)",
    )

    return parser.parse_args()
