import hashlib
import subprocess

from flask import Flask, request

app = Flask(__name__)

# Vulnerability: hardcoded credentials.
# Bandit can flag this because secrets should not be stored in source code.
ADMIN_PASSWORD = "SuperSecretPassword123"


@app.route("/")
def index():
    return """
    <h1>Bandit SAST Python Demo</h1>
    <p>This Flask application intentionally contains security issues.</p>
    <ul>
        <li>/login?password=...</li>
        <li>/ping?host=127.0.0.1</li>
        <li>/md5?value=hello</li>
    </ul>
    """


@app.route("/login")
def login():
    password = request.args.get("password", "")

    if password == ADMIN_PASSWORD:
        return "Login successful"

    return "Invalid password", 401


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # Vulnerability: user input is concatenated into a shell command.
    # This can lead to command injection, for example: ?host=127.0.0.1 && whoami
    command = f"ping -n 1 {host}"

    # Vulnerability: shell=True executes the command through the system shell.
    # Bandit detects this pattern because it increases command injection risk.
    result = subprocess.check_output(command, shell=True, text=True)
    return f"<pre>{result}</pre>"


@app.route("/md5")
def md5_hash():
    value = request.args.get("value", "demo")

    # Vulnerability: MD5 is a weak hashing algorithm for security-sensitive data.
    digest = hashlib.md5(value.encode("utf-8")).hexdigest()
    return {"algorithm": "md5", "value": value, "digest": digest}


if __name__ == "__main__":
    # Vulnerability: debug=True can expose sensitive information in production.
    app.run(host="0.0.0.0", port=5000, debug=True)
