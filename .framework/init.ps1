$VENV_PATH = ".\.venv"

if (-not (Test-Path $VENV_PATH)) {
    throw "No Virtual environment found at $VENV_PATH, please run .\setup.ps1 to configure this project"
}

& .venv/scripts/activate.ps1
pip install -r ./.framework/build-deps.txt
python -m build .framework/src
pip install -e .framework/src
