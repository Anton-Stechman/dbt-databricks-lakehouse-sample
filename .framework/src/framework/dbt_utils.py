"""Contains dbt specific utils"""
# Builtins
import subprocess
from enum import Enum

# Framework imports
from .utils import (
    file_exists
    , dir_exists
    , concatenate
)

class COMMAND(Enum):
    RUN ="dbt run"
    SEED = "dbt seed"
    COMPILE = "dbt compile"
    TEST = "dbt test"
    PARSE = "dbt parse"
    DOCS_GEN = "dbt docs generate"
    DOCS_VIEW = "dbt docs view"

class SUBCOMMAND(Enum):
    SELECT ="--select"

def dbt_command(cmd: COMMAND, profiles_dir: str = ".locals", project_dir: str = "dbt", subcmd: dict[SUBCOMMAND, str] = None):
    """
    """
    # Validate required directories and files exist
    _ = dir_exists(profiles_dir, autocreate=False, on_fail="raise")
    _ = dir_exists(project_dir, autocreate=False, on_fail="raise")
    _ = file_exists(profiles_dir, "profiles.yml", on_fail="raise")

    command: str = concatenate(cmd.value, "--project-dir", project_dir, "--profiles-dir", profiles_dir)
    subcommands: list = []
    if subcmd:
        for key, val in subcmd.items():
            if not isinstance(key, SUBCOMMAND):
                raise TypeError(f"Expected type {SUBCOMMAND} got {type(key)} for {key}")
            subcommands.append(concatenate(key, val))
        command: str = concatenate(command, *subcommands)
    subprocess.run([command])
