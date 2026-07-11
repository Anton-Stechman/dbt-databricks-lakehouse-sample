"""Contains generic utils used by the framework menus."""

import os
from typing import Literal


class DirectoryNotFound(BaseException):
    """Raised when a required directory cannot be found."""

    def __init__(self, *args):
        super().__init__(*args)


def validate_args(*args: str, t: type = str) -> bool:
    """Validate that all provided values are strings and non-empty."""
    if not args:
        raise ValueError("`args` is None")
    for arg in args:
        if not isinstance(arg, t):
            raise TypeError(f"Expected type {t} got {type(arg)} for value `{arg}`")
        if t is str and arg == "":
            raise ValueError("values cannot be empty")
    return True


def dir_exists(
    *args: str
    , target: str | None = None
    , autocreate: bool = True
    , on_fail: Literal["raise", "return"] = "return"
) -> bool:
    """Check if a directory exists or create it if required."""
    values = list(args)
    if target is not None:
        values.append(target)
    validate_args(*values, t=str)
    path = os.path.join(*args) if args else target
    if autocreate and not os.path.isdir(path):
        os.makedirs(path)

    exists = os.path.isdir(path)
    if on_fail == "return":
        return exists
    if not exists:
        raise DirectoryNotFound(f"directory {path} not found")
    return True


def file_exists(
    *args: str
    , target: str | None = None
    , on_fail: Literal["raise", "return"] = "return"
) -> bool:
    """Check if a file exists."""
    values = list(args)
    if target is not None:
        values.append(target)
    validate_args(*values, t=str)
    path = os.path.join(*args) if args else target
    exists = os.path.isfile(path)
    if on_fail == "return":
        return exists
    if not exists:
        raise FileNotFoundError(f"File {path} not found")
    return True


def concatenate(*args: str, sep: str = " ") -> str:
    """Join one or more strings with a separator."""
    validate_args(*args)
    return sep.join(args)


def menu_header(text: str, width: int = 50, decorator: str = "=") -> None:
    """Print a formatted menu header."""
    print(f"{decorator * width}")
    print(text)
    print(f"{decorator * width}")


def menu_items(*args: str, response_type: type = int) -> int:
    """Print menu items and return the chosen option."""
    index = 1
    if args:
        for arg in args:
            print(f"[{index}] {arg}")
            index += 1
        print("[0] exit")
        return response_type(input("select an option: "))
    return 0
