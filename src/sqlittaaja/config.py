import argparse
import tomllib
import os
from typing import Any


class Config:
    """Application level configuration options."""

    initialize_script: str = ""
    answer: str
    exercise_paths: list[str] = []
    threshold_pct: float = 0.9

    def parse(self, config: dict[str, Any]):
        match config.get("answer"):
            case dict(answer_section):
                match answer_section.get("initialize"):
                    case str(value):
                        self.initialize_script = value
                    case value if value is not None:
                        raise ValueError("Invalid type for 'answer.initialize'")
                match answer_section.get("exercise"):
                    case str(value):
                        self.answer = value
                    case None:
                        raise ValueError("Missing 'answer.exercise' value")
                    case _:
                        raise ValueError("Invalid type for 'answer.exercise'")

        match config.get("exercises"):
            case list(exercises_section):

                def get_exercise_path(exercise) -> str:
                    match exercise:
                        case {"path": str(path)}:
                            return path
                        case _:
                            raise ValueError(
                                "Invalid or missing path value in some exercise"
                            )

                # Extract each path value from exercises.
                self.exercise_paths = list(map(get_exercise_path, exercises_section))
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


def read_args() -> Config:
    """Reads command line arguments. Returns the parsed configuration file."""

    parser = argparse.ArgumentParser(
        description="Check SQLite exercises", epilog="Created by TIKO"
    )

    # Helper function for converting the command line argument into `Config`.
    def load_config(path: str) -> Config:
        try:
            config = Config(path)
            # Change the current working directory to where the config is.
            os.chdir(os.path.abspath(os.path.dirname(path)))
            return config
        except Exception as e:
            # Convert any exception to ArgumentTypeError.
            raise argparse.ArgumentTypeError(e)

    parser.add_argument(
        "-c",
        "--config",
        type=load_config,
        default="config.toml",
        help="configuration file for the exercises (in TOML format)",
    )

    args = parser.parse_args()
    return args.config
