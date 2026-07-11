"""Contains all menus used by the framework"""
from typing import Any
import subprocess

from .utils import menu_items, menu_header
from .dbt_utils import (
        COMMAND
        , SUBCOMMAND
        , dbt_command
)

def main_menu():
    """main menu - no protection added, intrended to break on invalid input"""
    subprocess.run("cls", shell=True)
    menu_header("Databricks dbt Sample Project")
    items: list[str] = list(MENU_ITEMS.keys())
    response: int = menu_items(*items)
    while response != 0:
        if response == 0:
            break
        item = response -1
        option = items[item]
        action = MENU_ITEMS[option]
        action()
        main_menu()

def dbt_run_all():
    dbt_command(COMMAND.RUN)

def dbt_run_specific():
    node = input("enter node name: ")
    dbt_command(COMMAND.RUN,  subcmd={SUBCOMMAND.SELECT: node})

def dbt_seed():
    dbt_command(COMMAND.SEED)

def dbt_compile():
    dbt_command(COMMAND.COMPILE)

def dbt_docs_generate():
    dbt_command((COMMAND.DOCS_GEN))

def dbt_docs_view():
    dbt_command((COMMAND.DOCS_VIEW))

def dbt_test():
    dbt_command((COMMAND.TEST))

MENU_ITEMS: dict[str, Any] = {
    "dbt-run": dbt_run_all
    , "dbt-run-specific": dbt_run_specific
    , "dbt-seed": dbt_seed
    , "dbt-compile": dbt_compile
    , "dbt-docs-generate": dbt_docs_generate
    , "dbt-docs-view":  dbt_docs_view
    , "dbt-test": dbt_test
}
