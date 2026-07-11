"""Contains all menus used by the framework."""

from typing import Any
import subprocess

from .code_gen import (
    get_list_schemas
    , get_list_models
    , generate_selected_model
)
from .dbt_utils import (
    dbt_build
    , dbt_compile
    , dbt_docs_generate
    , dbt_docs_view
    , dbt_run
    , dbt_run_specific
    , dbt_seed
    , dbt_test
)
from .utils import menu_header, menu_items


DBT_MENU_ITEMS: dict[str, Any] = {
    "exit": None
    , "dbt-run": dbt_run
    , "dbt-run-specific": dbt_run_specific
    , "dbt-run-full": dbt_build
    , "dbt-seed": dbt_seed
    , "dbt-compile": dbt_compile
    , "dbt-docs-generate": dbt_docs_generate
    , "dbt-docs-view": dbt_docs_view
    , "dbt-test": dbt_test
}

def dbt_menu() -> None:
    """Display the dbt menu and dispatch the selected action."""
    subprocess.run("cls", shell=True, check=False)
    menu_header("Sample Project: dbt menu")
    items: list[str] = list(DBT_MENU_ITEMS.keys())[1:]
    raw_response: Any = menu_items(*items)
    try:
        response = int(raw_response)
    except ValueError:
        print(f"selection '{raw_response}' is invalid and not of type {int}")
        try:
            input("press enter to try again... ")
        except (EOFError, OSError):
            print("No input available; returning to the menu.")
        return None

    if response == 0:
        return None

    try:
        option = items[response - 1]
    except IndexError:
        print("Invalid selection")
        return None

    action = DBT_MENU_ITEMS[option]
    if action is None:
        return None
    action()

def create_model() -> None:
    """Display the create-model menu"""
    def sel_schema() -> str:
        subprocess.run("cls", shell=True, check=False)
        menu_header("Create Model: Select Schema")
        schemas: list[str] = get_list_schemas()
        raw_response: Any = menu_items(*schemas)
        try:
            response = int(raw_response)
        except ValueError:
            print(f"selection '{raw_response}' is invalid and not of type {int}")
            try:
                input("press enter to try again... ")
            except (EOFError, OSError):
                print("No input available; returning to the main menu.")
                return None
        if response == 0:
            return None

        try:
            option = schemas[response - 1]
        except IndexError:
            print("Invalid selection")
            return None
        return option

    def sel_model(tschema: str | None = None) -> str:
        subprocess.run("cls", shell=True, check=False)
        menu_header("Create Model: Select Schema")
        models: list[str] = get_list_models(target_schema=tschema)
        raw_response: Any = menu_items(*models)
        try:
            response = int(raw_response)
        except ValueError:
            print(f"selection '{raw_response}' is invalid and not of type {int}")
            try:
                input("press enter to try again... ")
            except (EOFError, OSError):
                print("No input available; returning to the main menu.")
                return None
        if response == 0:
            return None

        try:
            option = models[response - 1]
        except IndexError:
            print("Invalid selection")
            return None
        return option

    _schema: str = sel_schema()
    if not _schema:
        return None

    _model: str = sel_model(_schema)
    if not _model:
        return None

    if str(input(f"create model {_model}? [y/n] ")) == "y":
        generate_selected_model(_model)
    return None

def sqlfluff() -> None:
    """fluff dbt project"""
    subprocess.run("cls", shell=True, check=False)
    menu_header("SqlFluff")
    subprocess.run("sqlfluff lint --dialect databricks dbt/", shell=True, check=False)
    input("press enter to continue... ")

MAIN_MENU_ITEMS: dict[str, Any] = {
    "exit": None
    , "dbt": dbt_menu
    , "create-models": create_model
    , "lint": sqlfluff
}

def main_menu() -> None:
    """Display the main menu and dispatch the selected action."""
    while True:
        try:
            subprocess.run("cls", shell=True, check=False)
            menu_header("Databricks dbt Sample Project")
            items: list[str] = list(MAIN_MENU_ITEMS.keys())[1:]
            raw_response: Any = menu_items(*items)
            try:
                response = int(raw_response)
            except ValueError:
                print(f"selection '{raw_response}' is invalid and not of type {int}")
                try:
                    input("press enter to try again... ")
                except (EOFError, OSError):
                    print("No input available; returning to the menu.")
                continue
            if response == 0:
                break

            try:
                option = items[response - 1]
            except IndexError:
                print("Invalid selection")
                return None

            action = MAIN_MENU_ITEMS[option]
            if action is None:
                return None
            action()

        except KeyboardInterrupt as exc:
            print("\nExiting menu...")
            raise SystemExit(0) from exc
        except KeyError:
            print("Invalid selection")
            continue
        except Exception as ex:
            print(f"An exception occurred: {ex}")
            raise SystemExit(0) from ex
