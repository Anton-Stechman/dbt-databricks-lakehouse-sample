"""Contains dbt specific utils"""
# Builtins
import subprocess
from enum import Enum

# Framework imports
from .utils import (
    file_exists
    , dir_exists
    , concatenate
    , menu_header
)

class COMMAND(Enum):
    RUN ="dbt run"
    SEED = "dbt seed"
    COMPILE = "dbt compile"
    TEST = "dbt test"
    PARSE = "dbt parse"
    DOCS = "dbt docs"

class SUBCOMMAND(Enum):
    SELECT ="--select"
    GENERATE = "generate"
    SERVE = "serve"

def dbt_command(cmd: COMMAND, profiles_dir: str = ".locals", project_dir: str = "dbt", subcmd: dict[SUBCOMMAND, str] = None):
    """
    Run a dbt command using the COMMAND and SUBCOMMAND enum classes
    """
    subprocess.run("cls", shell=True)
    menu_header(cmd.value)
    # Validate required directories and files exist
    _ = dir_exists(profiles_dir, autocreate=False, on_fail="raise")
    _ = dir_exists(project_dir, autocreate=False, on_fail="raise")
    _ = file_exists(profiles_dir, "profiles.yml", on_fail="raise")

    cmd_hooks: str = concatenate("--project-dir", project_dir, "--profiles-dir", profiles_dir)
    command: str = cmd.value
    subcommands: list = []
    if subcmd:
        for key, val in subcmd.items():
            if not isinstance(key, SUBCOMMAND):
                raise TypeError(f"Expected type {SUBCOMMAND} got {type(key)} for {key}")
            if not val:
                subcommands.append(key.value)
                continue
            subcommands.append(concatenate(key.value, val))
        command = concatenate(command, *subcommands, cmd_hooks)
    else:
        command = concatenate(command, cmd_hooks)

    subprocess.run(command, shell=True, check=True)
