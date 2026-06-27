import hashlib
import os
import subprocess

from flask import Flask, request

app = Flask(__name__)

# Improvement: the password comes from an environment variable instead of source code.
# Example for local testing:
# PowerShell: $env:ADMIN_PASSWORD="change-me"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


@app.route("/")
def index():
    return """
    <h1>Secure Bandit SAST Python Demo</h1>
    <p>This version fixes the issues intentionally included in app.py.</p>
    <ul>
        <li>/login?password=...</li>
        <li>/ping?host=127.0.0.1</li>
        <li>/sha256?value=hello</li>
    </ul>
    """


@app.route("/login")
def login():
    password = request.args.get("password", "")

    if ADMIN_PASSWORD and password == ADMIN_PASSWORD:
        return "Login successful"

    return "Invalid password", 401


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # Improvement: pass arguments as a list and avoid shell=True.
    # The user input is treated as one argument, not as shell syntax.
    result = subprocess.check_output(
        ["ping", "-n", "1", host],
        text=True,
        stderr=subprocess.STDOUT,
    )
    return f"<pre>{result}</pre>"


@app.route("/sha256")
def sha256_hash():
    value = request.args.get("value", "demo")

    # Improvement: SHA-256 is stronger than MD5 for hashing demonstrations.
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return {"algorithm": "sha256", "value": value, "digest": digest}


if __name__ == "__main__":
    # Improvement: debug mode is disabled for safer execution.
    app.run(host="127.0.0.1", port=5000, debug=False)
