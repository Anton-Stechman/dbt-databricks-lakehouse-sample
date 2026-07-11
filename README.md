# dbt-databricks-lakehouse-sample
Simple Data Lakehouse implementation using Databricks and DBT

___

The purposee of this project is to implement a simple dbt framework and data lakehouse in Databricks.
This project was built in the space of one day with no prior experience or usage with databricks.

# Project Requirements
- `python>=3.13, <3.14`
- `pip>=26.0.1`
- databricks account [signup](databricks.com)
- GitHub repository secrets:
  - `DBT_HOST`
  - `DBT_HTTP_PATH`
  - `DBT_TOKEN`
  - `GITHUB_TOKEN` (provided automatically by GitHub Actions)

## Setup
to setup this project on a new machine:
- Ensure all pre-reqs are installed
- in a shell run the setup script:
```powershell
.\setup.ps1
```

## Running Framework
to run the framework use the below command in a terminal
```powerrshell
menu run
```

### Framework features:
- full dbt menu
  handles dbt cli commands making local-dev deployments easier
- create models menu
  generates source models from metadata.
- lint
  runs sqlfluff over the dbt codebase

## Workflows
This repository includes four GitHub Actions workflows that cover CI validation, dbt execution, docs publishing, and framework testing:

- `dbt-ci-build.yml` - Runs the dbt validation pipeline for non-main branches, including dependency installation, SQL linting, dbt parse, seed, run, test, schema cleanup, and docs generation.
- `dbt-docs-release.yml` - Publishes generated dbt documentation to GitHub Pages when changes land on the `prod` branch.
- `dbt-release.yml` - Executes the production dbt release flow on `prod`, including seed and run steps for the target environment.
- `framework-ci-build.yml` - Validates the framework package with pylint, pytest, and a build step for non-main branches.


# dbt docs
dbt docs for this project are now available at [dbt-docs](https://anton-stechman.github.io/dbt-databricks-lakehouse-sample/)
