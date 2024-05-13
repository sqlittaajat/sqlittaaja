# SQLittaaja

[![GitHub Release](https://img.shields.io/github/v/release/sqlittaajat/sqlittaaja?logo=github)](https://github.com/sqlittaajat/sqlittaaja/releases)

SQLittaaja is a tool that checks and grades SQLite exercises and flags possible
cases of plagiarism. It is designed for teachers that use Moodle as a learning
platform in their courses.

## Installation

Download the latest version of SQLittaaja from
[releases tab](https://github.com/sqlittaajat/sqlittaaja/releases)
or alternatively if that is not possible, using this command:

```
python –m venv venv
venv\Scripts\activate
pip install git+https://github.com/sqlittaajat/sqlittaaja.git
```

## Running SQLittaaja

To run SQLittaaja you will need:

- [a configuration file](https://github.com/sqlittaajat/sqlittaaja/wiki/Configuration-file) and
- [a zip file containing exercise submissions](https://github.com/sqlittaajat/sqlittaaja/wiki/How-to-run-SQLittaaja#student-submissions-zip-file-and-its-structure)

Run SQLittaaja from command line without arguments when your 'config.toml' file
is in the directory from which you run it, or specify a different configuration
file like so:

```
sqlittaaja your_config.toml
```

Refer to SQLittaaja Wiki for further instructions:
[How to run SQLittaaja](https://github.com/sqlittaajat/sqlittaaja/wiki/How-to-run-SQLittaaja)

## Technologies

[![Python Version](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)

The project is created using:

- Python 3.11
- [Black](https://pypi.org/project/black/) code formatter
- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

This project adheres to [Semantic Versioning](https://semver.org/)

See also: [Releases](https://github.com/sqlittaajat/sqlittaaja/releases)
