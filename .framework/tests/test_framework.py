import subprocess
from pathlib import Path

import pytest

import framework.dbt_utils as dbt_utils
import framework.menus as menus
import framework.utils as framework_utils


class DummyCalledProcessError(subprocess.CalledProcessError):
    pass


def test_validate_args_accepts_valid_input():
    assert framework_utils.validate_args("alpha", "beta") is True


def test_validate_args_rejects_invalid_types():
    with pytest.raises(TypeError):
        framework_utils.validate_args("alpha", 42)


def test_validate_args_rejects_empty_input():
    with pytest.raises(ValueError):
        framework_utils.validate_args("")


def test_dir_exists_creates_missing_directory(tmp_path):
    target = tmp_path / "new-dir"

    assert framework_utils.dir_exists(str(target), on_fail="return") is True
    assert target.exists()
    assert target.is_dir()


def test_dir_exists_raises_when_missing_and_not_created(tmp_path):
    target = tmp_path / "missing-dir"

    with pytest.raises(framework_utils.DirectoryNotFound):
        framework_utils.dir_exists(str(target), autocreate=False, on_fail="raise")


def test_file_exists_returns_expected_value(tmp_path):
    target = tmp_path / "example.txt"
    target.write_text("hello", encoding="utf-8")

    assert framework_utils.file_exists(str(target), on_fail="return") is True
    assert framework_utils.file_exists(str(tmp_path / "missing.txt"), on_fail="return") is False


def test_concatenate_joins_values_with_separator():
    assert framework_utils.concatenate("alpha", "beta", sep="::") == "alpha::beta"


def test_menu_items_prints_entries_and_returns_selection(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "2")

    result = framework_utils.menu_items("one", "two")

    captured = capsys.readouterr()
    assert result == 2
    assert "[1] one" in captured.out
    assert "[2] two" in captured.out
    assert "[0] exit" in captured.out


def test_dbt_command_builds_expected_command(monkeypatch):
    calls = []

    def fake_run(command, shell=False, check=False):
        calls.append((command, shell, check))
        return None

    monkeypatch.setattr(dbt_utils.subprocess, "run", fake_run)
    monkeypatch.setattr(dbt_utils, "dir_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(dbt_utils, "file_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(dbt_utils, "menu_header", lambda *args, **kwargs: None)
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    dbt_utils.dbt_command(dbt_utils.COMMAND.RUN)

    assert calls[0][0] == "cls"
    assert calls[1][0] == "dbt run --project-dir dbt --profiles-dir .locals"
    assert calls[1][1] is True
    assert calls[1][2] is True


def test_dbt_command_handles_subprocess_failure(monkeypatch, capsys):
    def fake_run(command, shell=False, check=False):
        if command == "cls":
            return None
        raise subprocess.CalledProcessError(returncode=2, cmd=command)

    monkeypatch.setattr(dbt_utils.subprocess, "run", fake_run)
    monkeypatch.setattr(dbt_utils, "dir_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(dbt_utils, "file_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(dbt_utils, "menu_header", lambda *args, **kwargs: None)
    monkeypatch.setattr("builtins.input", lambda prompt: "")

    dbt_utils.dbt_command(dbt_utils.COMMAND.COMPILE)

    captured = capsys.readouterr()
    assert "dbt command failed with exit code 2" in captured.out
    assert "See the dbt output above for details." in captured.out


def test_dbt_wrapper_functions_delegate_to_dbt_command(monkeypatch):
    calls = []

    def fake_dbt_command(command, **kwargs):
        calls.append((command, kwargs))

    monkeypatch.setattr(dbt_utils, "dbt_command", fake_dbt_command)

    dbt_utils.dbt_run()
    dbt_utils.dbt_build()
    dbt_utils.dbt_compile()

    assert calls[0][0] == dbt_utils.COMMAND.RUN
    assert calls[1][0] == dbt_utils.COMMAND.BUILD
    assert calls[2][0] == dbt_utils.COMMAND.COMPILE


def test_main_menu_exits_cleanly_on_zero(monkeypatch):
    monkeypatch.setattr(menus.subprocess, "run", lambda *args, **kwargs: None)
    monkeypatch.setattr(menus, "menu_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(menus, "menu_items", lambda *args, **kwargs: 0)

    menus.main_menu()


def test_main_menu_reprompts_on_invalid_numeric_input(monkeypatch):
    responses = iter(["invalid", "0"])

    monkeypatch.setattr(menus.subprocess, "run", lambda *args, **kwargs: None)
    monkeypatch.setattr(menus, "menu_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(menus, "menu_items", lambda *args, **kwargs: next(responses))

    menus.main_menu()


def test_main_menu_raises_system_exit_on_keyboard_interrupt(monkeypatch):
    monkeypatch.setattr(menus.subprocess, "run", lambda *args, **kwargs: None)
    monkeypatch.setattr(menus, "menu_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(menus, "menu_items", lambda *args, **kwargs: (_ for _ in ()).throw(KeyboardInterrupt()))

    with pytest.raises(SystemExit) as excinfo:
        menus.main_menu()

    assert excinfo.value.code == 0


def test_menu_items_map_to_expected_callables():
    expected = {
        "dbt-run": dbt_utils.dbt_run,
        "dbt-run-specific": dbt_utils.dbt_run_specific,
        "dbt-run-full": dbt_utils.dbt_build,
        "dbt-seed": dbt_utils.dbt_seed,
        "dbt-compile": dbt_utils.dbt_compile,
        "dbt-docs-generate": dbt_utils.dbt_docs_generate,
        "dbt-docs-view": dbt_utils.dbt_docs_view,
        "dbt-test": dbt_utils.dbt_test
    }

    assert menus.DBT_MENU_ITEMS == {**{"exit": None}, **expected}
