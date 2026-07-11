"""Contains all menus used by the framework"""
# Builtins
from typing import Any
import subprocess

# Framework imports
from .utils import menu_items, menu_header
from .dbt_utils import (
        dbt_run
        , dbt_run_specific
        , dbt_build
        , dbt_seed
        , dbt_compile
        , dbt_docs_generate
        , dbt_docs_view
        , dbt_test
)


# Menu items distpatcher
MENU_ITEMS: dict[str, Any] = {
    "exit": None
    , "dbt-run": dbt_run
    , "dbt-run-specific": dbt_run_specific
    , "dbt-run-full": dbt_build
    , "dbt-seed": dbt_seed
    , "dbt-compile": dbt_compile
    , "dbt-docs-generate": dbt_docs_generate
    , "dbt-docs-view":  dbt_docs_view
    , "dbt-test": dbt_test
}

def main_menu():
    """main menu - no protection added, intended to break on invalid input"""
    try:
        subprocess.run("cls", shell=True)
        menu_header("Databricks dbt Sample Project")
        items: list[str] = list(MENU_ITEMS.keys())[1:]
        raw_response: Any = menu_items(*items)
        try:
            response = int(raw_response)
        except ValueError:
            print(f"selection '{raw_response}' is invalid and not of type {int}")
            input("press enter to try again... ")
            main_menu()
        while response != 0:
            if response == 0:
                break
            item = response - 1
            option = items[item]
            action = MENU_ITEMS[option]
            action()
            return main_menu()
    except KeyboardInterrupt:
        print("\nExiting menu...")
        raise SystemExit(0)
    except KeyError:
        print("Invalid selection")
    except Exception as ex:
        print(f"An exception occured: {ex}")
        raise SystemExit(0)
