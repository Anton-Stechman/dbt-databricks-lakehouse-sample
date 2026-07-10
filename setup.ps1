[CmdletBinding()]
param(
    [switch]$rebuild
)

$PY_VERSION = "3.13"
$VENV_PATH = Join-Path $PSScriptRoot ".venv"
$DBT_DEPS = Join-Path $PSScriptRoot "dbt/dbt-deps.txt"
$BUILD_DEPS = Join-Path $PSScriptRoot ".framework/build-deps.txt"
$ACTIVATE_VENV = Join-Path $VENV_PATH "Scripts/Activate.ps1"
$INIT_SCRIPT = Join-Path $PSScriptRoot ".framework/init.ps1"

function Initialize-ProjectEnvironment {
    param(
        [string]$VenvPath,
        [string]$ActivateScript,
        [string]$DepsPath,
        [string]$InitScript,
        [string]$PythonVersion
    )

    if (-not (Test-Path $ActivateScript)) {
        Write-Host "Creating virtual environment at $VenvPath..." -ForegroundColor Cyan
        py -$PythonVersion -m venv $VenvPath
    }

    if (Test-Path $ActivateScript) {
        Write-Host "Activating virtual environment..." -ForegroundColor Cyan
        & $ActivateScript

        if (Test-Path $DepsPath) {
            Write-Host "Installing dbt dependencies..." -ForegroundColor Cyan
            python -m pip install -r $DepsPath
        }
        else {
            Write-Warning "Dependency file not found: $DepsPath"
        }

        if (Test-Path $InitScript) {
            Write-Host "Running initialization script..." -ForegroundColor Cyan
            & $InitScript
        }
    }
    else {
        throw "Unable to locate virtual environment activation script at $ActivateScript"
    }
}

if ($rebuild -and (Test-Path $VENV_PATH)) {
    Write-Host "Removing existing environment to rebuild..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $VENV_PATH
}

if ($rebuild -or -not (Test-Path $ACTIVATE_VENV)) {
    Initialize-ProjectEnvironment -VenvPath $VENV_PATH -ActivateScript $ACTIVATE_VENV -DepsPath $DBT_DEPS -InitScript $INIT_SCRIPT -PythonVersion $PY_VERSION
}
else {
    Write-Host "Project Already Setup, rerun using .\setup.ps1 -rebuild to overwrite current installation" -ForegroundColor Yellow
}
