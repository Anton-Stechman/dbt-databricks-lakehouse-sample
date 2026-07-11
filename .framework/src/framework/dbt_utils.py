"""Contains dbt-specific utilities."""
# builtins
import subprocess
from enum import Enum

# Framework imports
from .utils import (
    concatenate
    , dir_exists
    , file_exists
    , menu_header
)

class COMMAND(Enum):
    """Supported dbt command names."""
    RUN = "dbt run"
    BUILD = "dbt build"
    SEED = "dbt seed"
    COMPILE = "dbt compile"
    TEST = "dbt test"
    PARSE = "dbt parse"
    DOCS = "dbt docs"
    DEPS = "dbt deps"

class SUBCOMMAND(Enum):
    """Supported dbt subcommands."""
    SELECT = "--select"
    GENERATE = "generate"
    SERVE = "serve"

def dbt_command(
    cmd: COMMAND
    , profiles_dir: str = ".locals"
    , project_dir: str = "dbt"
    , subcmd: dict[SUBCOMMAND, str | None] | None = None
) -> None:
    """Run a dbt command using the provided command and subcommands."""
    subprocess.run("cls", shell=True, check=False)
    menu_header(cmd.value)

    _ = dir_exists(profiles_dir, autocreate=False, on_fail="raise")
    _ = dir_exists(project_dir, autocreate=False, on_fail="raise")
    _ = file_exists(profiles_dir, "profiles.yml", on_fail="raise")

    cmd_hooks = concatenate("--project-dir", project_dir, "--profiles-dir", profiles_dir, "--target dev")
    command = cmd.value
    subcommands = []
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

    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"dbt command failed with exit code {exc.returncode}")
        print("See the dbt output above for details.")
    finally:
        input("Press enter to continue... ")


def dbt_run() -> None:
    """Run the dbt models."""
    dbt_command(COMMAND.RUN)

def dbt_run_specific() -> None:
    """Run a specific dbt model or selection."""
    node = input("enter node name: ")
    dbt_command(COMMAND.RUN, subcmd={SUBCOMMAND.SELECT: node})

def dbt_build() -> None:
    """Run the full dbt build pipeline."""
    dbt_command(COMMAND.BUILD)

def dbt_seed() -> None:
    """Load dbt seeds."""
    dbt_command(COMMAND.SEED)

def dbt_compile() -> None:
    """Compile the dbt project."""
    dbt_command(COMMAND.COMPILE)

def dbt_parse() -> None:
    """Run dbt Parse."""
    dbt_command(COMMAND.PARSE)

def dbt_deps() -> None:
    """Run dbt deps."""
    dbt_command(COMMAND.DEPS)

def dbt_docs_generate() -> None:
    """Generate dbt documentation."""
    dbt_command(COMMAND.DOCS, subcmd={SUBCOMMAND.GENERATE: None})

def dbt_docs_view() -> None:
    """Serve dbt documentation locally."""
    dbt_command(COMMAND.DOCS, subcmd={SUBCOMMAND.SERVE: None})

def dbt_test() -> None:
    """Run the dbt tests."""
    dbt_command(COMMAND.TEST)
