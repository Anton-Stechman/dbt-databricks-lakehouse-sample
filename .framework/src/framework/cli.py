"""Framework's cli script - this is the main user-entry point for the framework."""
# builtins
import os
import subprocess
import argparse

# 3rd Party imports
import yaml

# Framework imports
from .menus import main_menu
from .utils import file_exists, dir_exists, menu_header

def initialise():
    """initialise project"""
    subprocess.run("cls", shell=True)
    menu_header("dbt-databricks-sample framework cli")
    print("Initialising framework")
    print("checking for .locals folder")
    _ =  dir_exists(".locals") # creates dir if not exists
    print("cheking for dbt profile")
    if not file_exists(".locals", "profiles.yml", on_fail="return"):
        print("dbt profile not found... creating a new profile...")
        user_profile: dict = {
            "databricks_lakehouse_sample": {
                "target": "dev"
                , "ouputs": {
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
        user_profile["databricks_lakehouse_sample"]["outputs"]["dev"]["catalog"] = catalog
        user_profile["databricks_lakehouse_sample"]["outputs"]["dev"]["schema"] = schema
        user_profile["databricks_lakehouse_sample"]["outputs"]["dev"]["host"] = host
        user_profile["databricks_lakehouse_sample"]["outputs"]["dev"]["http_path"] = http_path
        user_profile["databricks_lakehouse_sample"]["outputs"]["dev"]["token"] = token
        user_profile["databricks_lakehouse_sample"]["outputs"]["dev"]["threads"] = 4
        fpath: str = os.path.join(".locals", "profiles.yml")
        with open(fpath, "w", encoding="utf-8") as file:
            file.write(yaml.dump(user_profile))
        if file_exists(fpath, on_fail="return"):
            print("profile configuration complete..")
    else:
        print("profile found...")
        return



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
        initialise()
        main_menu()
