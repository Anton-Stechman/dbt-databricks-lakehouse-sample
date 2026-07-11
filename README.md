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
- `framework-ci-build.yml` - Validates the framework package with pylint, pytest, and a build step for non-main branches.
![diagram](./dbt%20databricks%20sample%20project%20-%20framework-ci-build.png)
- `dbt-ci-build.yml` - Runs the dbt validation pipeline for non-main branches, including dependency installation, SQL linting, dbt parse, seed, run, test, schema cleanup, and docs generation.
![diagram](./dbt%20databricks%20sample%20project%20-%20dbt-ci-build.png)
- `dbt-release.yml` - Executes the production dbt release flow on `prod` or `test`, including seed and run steps for the target environment.
![diagram](./dbt%20databricks%20sample%20project%20-%20dbt-release-build.png)
- `dbt-docs-release.yml` - Publishes generated dbt documentation to GitHub Pages when changes land on the `prod`branch.
![diagram](./dbt%20databricks%20sample%20project%20-%20dbt-docs-release.png)


# dbt docs
dbt docs for this project are now available at [dbt-docs](https://anton-stechman.github.io/dbt-databricks-lakehouse-sample/)

## ⚠️ Project Status & Limitations

**This project was built in a single day as a portfolio/learning project.** While it demonstrates production-grade patterns and DevOps practices, there are intentional tradeoffs made for speed:

**Known Limitations:**
- Code duplication in framework utilities (would benefit from refactoring into a full class-driven architecture)
- Some cross-over between modules that could be consolidated
- Limited error handling/edge cases
- Documentation could be more comprehensive

**This is intentional.** The goal was to demonstrate:
- How to architect a lakehouse implementation
- DevOps/CI patterns on Databricks
- Meta-programming concepts (source generation from metadata)
- Rapid learning and shipping on new platforms

**This is NOT:**
- Production-hardened
- Optimized for scale
- Fully tested across all edge cases

**This IS:**
- A solid foundation for learning
- A reference implementation of dbt + Databricks patterns
- A starting point for your own framework

---

## 🤝 Contributing

This project is open source. **Contributions welcome.** Areas that would benefit:

- Refactoring framework utilities into proper class architecture
- Additional error handling
- Expanded test coverage
- Documentation improvements
- Performance optimizations
