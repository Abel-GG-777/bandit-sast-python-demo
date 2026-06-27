# Applying Bandit SAST to Detect Vulnerabilities in a Python Flask Application

## Introduction

Security should be part of the development workflow, not only a final checklist before deployment. One practical way to introduce security earlier is by using Static Application Security Testing tools. In this article, I demonstrate how to use Bandit to analyze a small Python Flask application that intentionally contains insecure code.

GitHub repository: `<ADD_GITHUB_REPOSITORY_LINK_HERE>`

## What Is SAST?

Static Application Security Testing, commonly called SAST, is a security testing approach that analyzes source code without executing the application. Instead of waiting until runtime, SAST tools inspect code patterns and identify potential vulnerabilities early in the development lifecycle.

SAST is especially useful in academic and professional environments because it can be automated in CI/CD pipelines and used by developers before code is merged.

## Why Bandit?

Bandit is a SAST tool designed specifically for Python. It scans Python files and reports common security issues such as hardcoded credentials, unsafe subprocess usage, weak cryptography, and risky configuration.

For this demo, Bandit is a good choice because it is lightweight, easy to install, simple to run from the command line, and easy to integrate with GitHub Actions.

## Demo Vulnerable Code Explanation

The demo application is a small Flask project in `app.py`. It intentionally includes several insecure patterns so Bandit can detect them:

- A hardcoded administrator password stored directly in the source code.
- A `subprocess.check_output` call using `shell=True`.
- User input from a query parameter concatenated into a shell command, creating a possible command injection risk.
- The use of `hashlib.md5`, a weak hashing algorithm for security-sensitive use cases.
- Flask running with `debug=True`.

These vulnerabilities are intentionally simple so the results are easy to explain in a classroom or presentation.

## Running Bandit Locally

First, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Then run Bandit against the repository:

```bash
python -m bandit -r .
```

To generate a text report, run:

```bash
python -m bandit -r . -f txt -o bandit-report.txt
```

## Explaining Findings

Bandit reports issues with identifiers, severity levels, confidence levels, file paths, and line numbers. In this project, the expected findings are related to hardcoded credentials, subprocess execution, shell usage, MD5 hashing, and debug mode.

The important part of the demo is not only seeing the warnings, but understanding why each pattern is risky. For example, `shell=True` becomes dangerous when combined with user-controlled input because the shell may interpret special characters as commands.

## Secure Code Improvements

The corrected version is implemented in `app_secure.py`. It applies simple improvements:

- The password is loaded from the `ADMIN_PASSWORD` environment variable.
- `shell=True` is removed.
- The subprocess call uses a list of arguments instead of a shell command string.
- MD5 is replaced with SHA-256.
- Flask debug mode is disabled.

This secure version keeps the application easy to understand while showing how vulnerable patterns can be improved.

## GitHub Actions Automation

The repository includes a GitHub Actions workflow at `.github/workflows/bandit.yml`. It runs on pushes and pull requests targeting the `main` branch.

The workflow checks out the repository, configures Python 3.11, installs dependencies, and runs:

```bash
python -m bandit -r . -f txt
```

This demonstrates how SAST can become part of a continuous integration process. Every push or pull request can be scanned automatically before changes are accepted.

## Conclusion

Bandit is a practical tool for introducing SAST into Python projects. It is simple to run locally, easy to automate, and useful for identifying common insecure coding patterns. This demo shows how a vulnerable Flask application can be scanned, how the findings can be explained, and how a corrected version can reduce the reported risks.
