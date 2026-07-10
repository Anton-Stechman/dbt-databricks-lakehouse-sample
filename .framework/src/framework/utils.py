"""Contains generic utils, used by the framework menus."""
import os
from typing import Literal, Any

class DirectoryNotFound(BaseException):
    def __init__(self, *args):
        super().__init__(*args)

def validate_args(*args, t: type = str) -> bool:
    for arg  in args:
        if not isinstance(arg, t):
            raise TypeError(f"Expected type {t} got {type(arg)} for value `{arg}`")
    if not args:
        raise ValueError(f"`args` is {None}")
    return True

def dir_exists(*args: str, target: str | None = None, autocreate: bool = True, on_fail: Literal["raise", "return"] = "return") -> bool:
    """
        Check if directory exists

        ## Params
            - args `<type=str>` **optional** `(default=None)`: if args are passed these will be concatenmated into a path string.
            - target `<type=str | None>` **optional** `(default=None)`: target directory
            - autocreate`<type=bool>` **optional** `(default=True)`: if directory is not found, it will be created

        ## Raises
            - `TypeError`: when any one of either `args` or `target` are not of `type=str`.
            - `DirectoryNotFound`: when `on_fail` is set to raise and the target directory is not locatable.

        ## Returns
            - `boolen`:
                - `True`: when the path is a valid directory or one has been created.
                - `False`: when `autocreate` is set  to `False`and the  directory is not valid
    """
    if validate_args(*args, target if target else "", t=str):
        _path_ = os.path.join(*args) if args else target
        if autocreate:
            if not os.path.isdir(_path_):
                os.makedirs(_path_)
        _targ_exists_: bool = os.path.isdir(_path_)
        if on_fail =="return":
            return _targ_exists_
        if not _targ_exists_:
            raise DirectoryNotFound(f"directory {_path_} not found")
        return True

def file_exists(*args: str, target: str | None = None, on_fail: Literal["raise", "return"] = "return") -> bool:
    """
        Check if directory exists

        ## Params
            - args `<type=str>` **optional** `(default=None)`: if args are passed these will be concatenmated into a path string.
            - target `<type=str | None>` **optional** `(default=None)`: target directory
            - autocreate`<type=bool>` **optional** `(default=True)`: if directory is not found, it will be created

        ## Raises
            - `Type Error`: when any one of either `args` or `target` are not of `type=str`.

        ## Returns
            - `boolen`:
                - `True`: when the path is a valid directory or one has been created.
                - `False`: when `autocreate` is set  to `False`and the  directory is not valid
    """
    if validate_args(*args, target if target else "", t=str):
        _path_: str = os.path.join(*args) if args else target
        _targ_exists_: bool = os.path.isfile(_path_)
        if on_fail == "return":
            return _targ_exists_
        if not  _targ_exists_:
            raise FileNotFoundError(f"File {_path_} not found")
        return True

def concatenate(*args: str, sep=" ") -> str:
    if validate_args(*args):
        return sep.join(args)

def menu_header(text: str, width: int=50, decorator: str = "="):
    """print menu header"""
    print(f"{decorator * width}")
    print(text)
    print(f"{decorator * width}")

def menu_items(*args: str):
    """print menu items"""
    index: int = 1
    if args:
        for arg in args:
            print(f"[{index}] {arg}")
            index += 1
        print("[0] exit")
        return int(input("select an option: "))
