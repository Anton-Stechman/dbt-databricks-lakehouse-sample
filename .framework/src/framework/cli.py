"""Framework's cli script - this is the main user-entry point for the framework."""
import subprocess
import argparse

from .menus import main_menu

def main():
    subprocess.run(["cls"], check=True, shell=True)
    parser = argparse.ArgumentParser(
        prog="framework"
        , description="dbt-databricks-sample framework cli"
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("run", help="Run framework")
    args = parser.parse_args()
    if args.command == "run":
        main_menu()
