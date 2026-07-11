"""Contains all menus used by the framework."""

from typing import Any
import subprocess

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


MENU_ITEMS: dict[str, Any] = {
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


def main_menu() -> None:
    """Display the main menu and dispatch the selected action."""
    while True:
        try:
            subprocess.run("cls", shell=True, check=False)
            menu_header("Databricks dbt Sample Project")
            items: list[str] = list(MENU_ITEMS.keys())[1:]
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
                continue

            action = MENU_ITEMS[option]
            if action is None:
                break
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
