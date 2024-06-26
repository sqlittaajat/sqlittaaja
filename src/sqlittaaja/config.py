import argparse
import tomllib
import os
import sys
from typing import Any


class Config:
    """Application level configuration options."""

    initialize_script: str = ""
    exercises: list[(str, str, list[str], list[str])] = []
    threshold_pct: float = 0.9
    open_report: bool = False

    def parse(self, config: dict[str, Any]):
        match config.get("answer"):
            case dict(answer_section):
                match answer_section.get("initialize"):
                    case str(value):
                        self.initialize_script = value
                    case None:
                        # Check for the initialization script file instead.
                        match answer_section.get("initialize_path"):
                            case str(path):
                                with open(path, "r") as file:
                                    self.initialize_script = "\n".join(file.readlines())
                            case value if value is not None:
                                raise ValueError(
                                    "Invalid type for 'answer.initialize_path'"
                                )
                    case value if value is not None:
                        raise ValueError("Invalid type for 'answer.initialize'")

        match config.get("exercises"):
            case list(exercises_section):

                def get_exercise(exercise) -> (str, str, list[str], list[str]):
                    must_contain = process_word_list(exercise, "must_contain")
                    must_not_contain = process_word_list(exercise, "must_not_contain")
                    match exercise:
                        case {"path": str(path), "answer": str(answer)}:
                            return (path, answer, must_contain, must_not_contain)
                        case {"path": str(path), "answer_path": str(answer_path)}:
                            with open(answer_path, "r") as file:
                                return (
                                    path,
                                    "\n".join(file.readlines()),
                                    must_contain,
                                    must_not_contain,
                                )
                        case _:
                            raise ValueError(
                                "Invalid or missing path/answer values in some exercise"
                            )

                # Extract each path/answer value from exercises.
                self.exercises = list(map(get_exercise, exercises_section))
            case _:
                raise ValueError("No exercises defined")

        match config.get("check_options"):
            case dict(check_options_section):
                match check_options_section.get("threshold_pct"):
                    case int(value) | float(value):
                        if 0.0 <= value <= 1.0:
                            # Make sure threshold is actually a float.
                            self.threshold_pct = float(value)
                        else:
                            raise ValueError(
                                "Value 'check_options.threshold_pct' must be in range [0.0, 1.0]"
                            )
                    case value if value is not None:
                        raise ValueError(
                            "Invalid type for 'check_options.threshold_pct'"
                        )

    def __init__(self, path: str):
        with open(path, "rb") as file:
            self.parse(tomllib.load(file))


def process_word_list(value, name: str):
    """Ensure that the word list contains only strings."""

    value = value.get(name, [])
    match value:
        case list if all(isinstance(item, str) for item in value):
            return value
        case _:
            raise ValueError(f"Invalid type for '{name}'")


def read_args() -> Config:
    """Reads command line arguments. Returns the parsed configuration file."""

    parser = argparse.ArgumentParser(
        description="Check SQLite exercises", epilog="Created by TIKO"
    )

    # Helper function for converting the command line argument into `Config`.
    def load_config(path: str) -> Config:
        try:
            config_path = os.path.abspath(path)
            # Change the current working directory to where the config is.
            os.chdir(os.path.abspath(os.path.dirname(path)))
            return Config(config_path)
        except Exception as e:
            # Convert any exception to ArgumentTypeError.
            raise argparse.ArgumentTypeError(e)

    parser.add_argument(
        "config",
        type=load_config,
        default="config.toml",
        nargs="?",
        help="configuration file for the exercises (in TOML format)",
    )

    parser.add_argument(
        "-o",
        "--open-report",
        action=argparse.BooleanOptionalAction,
        default=not sys.stdin.isatty(),
        help="open HTML report in the default web browser",
    )

    args = parser.parse_args()
    args.config.open_report = args.open_report
    return args.config
