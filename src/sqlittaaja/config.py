import argparse
import tomllib


class Config:
    """Application level configuration options."""

    initialize_script: str = ""
    answer: str
    exercise_paths: list[str] = []
    threshold_pct: float = 0.9

    def __init__(self, path: str):
        with open(path, "rb") as file:
            config = tomllib.load(file)

            match config.get("answer"):
                case dict(answer_section):
                    match answer_section.get("initialize"):
                        case str(value):
                            self.initialize_script = value
                        case value if value is not None:
                            raise ValueError("invalid type for 'answer.initialize'")
                    match answer_section.get("exercise"):
                        case str(value):
                            self.answer = value
                        case None:
                            raise ValueError("missing 'answer.exercise' value")
                        case _:
                            raise ValueError("invalid type for 'answer.exercise'")

            match config.get("exercises"):
                case list(exercises_section):

                    def get_exercise_path(exercise) -> str:
                        match exercise:
                            case {"path": str(path)}:
                                return path
                            case _:
                                raise ValueError(
                                    "invalid or missing path value in some exercise"
                                )

                    # Extract each path value from exercises.
                    self.exercise_paths = list(
                        map(get_exercise_path, exercises_section)
                    )
                case _:
                    raise ValueError("no exercises defined")

            match config.get("check_options"):
                case dict(check_options_section):
                    match check_options_section.get("threshold_pct"):
                        case int(value) | float(value):
                            if 0.0 <= value <= 1.0:
                                # Make sure threshold is actually a float.
                                self.threshold_pct = float(value)
                            else:
                                raise ValueError(
                                    "'check_options.threshold_pct' must be in range [0.0, 1.0]"
                                )
                        case value if value is not None:
                            raise ValueError(
                                "invalid type for 'check_options.threshold_pct'"
                            )


def read_args() -> argparse.Namespace:
    """Reads command line arguments."""

    parser = argparse.ArgumentParser(
        description="Check SQLite exercises", epilog="Created by TIKO"
    )

    # Helper function for converting the command line argument into `Config`.
    def load_config(path: str) -> Config:
        try:
            return Config(path)
        except FileNotFoundError:
            raise argparse.ArgumentTypeError(f"file '{path}' doesn't exist")
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

    return parser.parse_args()
