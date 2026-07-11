"""Framework's CLI script - the main user-entry point for the framework."""
# builtins
import os
import argparse
import subprocess

# 3rd Party impoorts
import yaml

# Framework imports
from .menus import main_menu
from .utils import (
    dir_exists
    , file_exists
    , menu_header
)

def check_profile() -> bool:
    """Check user profile exists"""
    return file_exists(".locals", "profiles.yml", on_fail="return")

def create_profile() -> bool:
    """Create a new profile"""
    print("dbt profile not found... creating a new profile...")
    project_name = input("project name: ")
    user_profile: dict = {
        project_name: {
            "target": "dev"
            , "outputs": {
                "dev": {
                    "type": "databricks"
                }
            }
        }
    }
    catalog = input("catalog name: ")
    schema = input("schema name: ")
    host = input("host name: ")
    http_path = input("http path: ")
    token = input("token: ")
    user_profile[project_name]["outputs"]["dev"]["catalog"] = catalog
    user_profile[project_name]["outputs"]["dev"]["schema"] = schema
    user_profile[project_name]["outputs"]["dev"]["host"] = host
    user_profile[project_name]["outputs"]["dev"]["http_path"] = http_path
    user_profile[project_name]["outputs"]["dev"]["token"] = token
    user_profile[project_name]["outputs"]["dev"]["threads"] = 4
    fpath: str = os.path.join(".locals", "profiles.yml")
    with open(fpath, "w", encoding="utf-8") as file:
        file.write(yaml.dump(user_profile, sort_keys=False))
    return check_profile()

def initialise() -> None:
    """Initialise the project configuration."""
    subprocess.run("cls", shell=True, check=False)
    menu_header("dbt-databricks-sample framework cli")
    print("Initialising framework")
    print("checking for .locals folder")
    dir_exists(".locals", autocreate=True)
    print("cheking for dbt profile")
    if not check_profile():
        if create_profile():
            print("profile configuration complete..")
        else:
            raise FileNotFoundError("Could not find profiles.yml in './.locals/'")
    else:
        print("profile found...")

def main() -> None:
    """Run the CLI entry point."""
    subprocess.run("cls", shell=True, check=False)
    parser = argparse.ArgumentParser(
        prog="framework"
        , description="dbt-databricks-sample framework cli"
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("run", help="Run framework")
    args = parser.parse_args()
    if args.command == "run":
        initialise()
        main_menu()
