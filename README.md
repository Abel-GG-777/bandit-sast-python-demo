# Bandit SAST Python Demo

This repository is a simple academic demo that shows how to apply **Bandit**, a Static Application Security Testing tool, to a vulnerable Python Flask application.

The project intentionally includes insecure code in `app.py` and a corrected version in `app_secure.py`. The goal is to make the findings easy to explain during a presentation about SAST tools for applications.

## What Is SAST?

Static Application Security Testing, or SAST, analyzes source code without running the application. It helps developers find insecure patterns early in the software development lifecycle, before the code reaches production.

SAST tools are useful because they can be integrated into local development workflows and CI/CD pipelines. This allows security checks to run automatically whenever code changes.

## What Is Bandit?

Bandit is a SAST tool focused on Python. It scans Python source files and reports common security issues such as hardcoded passwords, dangerous subprocess usage, weak cryptographic algorithms, and unsafe application configuration.

This demo uses only Bandit. It does not use Sonar, Snyk, Semgrep, Veracode, or any other SAST platform.

## Vulnerabilities Included in `app.py`

The vulnerable Flask application includes the following intentional issues:

- **Hardcoded password**: `ADMIN_PASSWORD` is stored directly in the source code.
- **Subprocess with `shell=True`**: the application executes a command through the system shell.
- **Possible command injection**: user input from the `host` query parameter is concatenated into a shell command.
- **Weak hash algorithm**: the application uses `hashlib.md5`, which is not recommended for security-sensitive hashing.
- **Debug mode enabled**: Flask runs with `debug=True`, which can expose sensitive information.

These issues are included for educational purposes so Bandit can detect and report them clearly.

## Secure Version in `app_secure.py`

The secure version demonstrates simple improvements:

- The password is read from the `ADMIN_PASSWORD` environment variable.
- `shell=True` is avoided.
- `subprocess.check_output` receives a list of arguments.
- The `host` parameter is validated as an IP address before running `ping`.
- The remaining safe `subprocess` usage is documented with `# nosec` comments.
- MD5 is replaced with SHA-256.
- Flask debug mode is disabled.

## Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the Vulnerable Application

```bash
python app.py
```

Example endpoints:

```text
http://127.0.0.1:5000/login?password=SuperSecretPassword123
http://127.0.0.1:5000/ping?host=127.0.0.1
http://127.0.0.1:5000/md5?value=hello
```

## Run the Secure Application

PowerShell:

```powershell
$env:ADMIN_PASSWORD="change-me"
python app_secure.py
```

Bash:

```bash
export ADMIN_PASSWORD="change-me"
python app_secure.py
```

## Run Bandit Locally

```bash
python -m bandit -r .
```

## Generate a Bandit Report

```bash
python -m bandit -r . -f txt -o bandit-report.txt
```

The generated `bandit-report.txt` file is ignored by Git so local scan output does not need to be committed.

## GitHub Actions Automation

The workflow in `.github/workflows/bandit.yml` runs automatically on `push` and `pull_request` events targeting the `main` branch.

The pipeline:

1. Checks out the repository.
2. Configures Python 3.11.
3. Installs dependencies from `requirements.txt`.
4. Runs `python -m bandit -r . -f txt`.

This shows that Bandit can analyze the repository automatically as part of a CI/CD workflow.

Because `app.py` intentionally contains vulnerabilities, Bandit returns a non-zero exit code when it finds issues. The workflow uses `continue-on-error: true` so the GitHub Actions run can display the findings clearly without stopping the academic demo.

## Vulnerable vs Secure Comparison

| Topic | `app.py` vulnerable version | `app_secure.py` improved version |
| --- | --- | --- |
| Password handling | Hardcoded in source code | Loaded from environment variable |
| Command execution | Uses `shell=True` | Uses a list of arguments |
| User input | Concatenated into a command string | Validated as an IP address |
| Hashing | Uses MD5 | Uses SHA-256 |
| Flask debug | Enabled | Disabled |
