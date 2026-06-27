# Video Script: Bandit SAST Python Demo

Hello, my name is [Your Name], and in this short presentation I will demonstrate how to use Bandit as a SAST tool for a Python Flask application.

SAST means Static Application Security Testing. It is a technique used to analyze source code without running the application. The objective is to detect insecure coding patterns early, before the application is deployed.

For this demo, I am using Bandit. Bandit is a security analysis tool designed for Python projects. It scans Python files and reports issues such as hardcoded credentials, dangerous subprocess usage, weak cryptographic algorithms, and insecure configuration.

The repository contains two main files. The first one is `app.py`, which is intentionally vulnerable. It includes a hardcoded administrator password, uses `subprocess` with `shell=True`, builds a command using user input, uses `hashlib.md5`, and runs Flask with `debug=True`.

These issues are useful for the demo because Bandit can detect them and show the file, line number, severity, and confidence of each finding.

To run Bandit locally, first I install the dependencies with:

```bash
python -m pip install -r requirements.txt
```

Then I scan the repository with:

```bash
python -m bandit -r .
```

If I want to save the output as a report, I use:

```bash
python -m bandit -r . -f txt -o bandit-report.txt
```

The second important file is `app_secure.py`. This file shows a safer version of the same application. The password is loaded from an environment variable, `shell=True` is removed, subprocess receives a list of arguments, MD5 is replaced with SHA-256, and Flask debug mode is disabled.

The project also includes GitHub Actions automation. The workflow runs on pushes and pull requests to the `main` branch. It uses Ubuntu latest, sets up Python 3.11, installs the dependencies, and runs Bandit against the repository.

In conclusion, this demo shows how Bandit can help developers identify common Python security issues using SAST. It can be executed locally and automated in CI/CD, making it useful for both learning and real development workflows.
