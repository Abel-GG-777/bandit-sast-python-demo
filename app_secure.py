import hashlib
import ipaddress
import os
import platform
import shutil
# Used with validated input and shell=False in this educational demo.
import subprocess  # nosec B404

from flask import Flask, request

app = Flask(__name__)

# Improvement: the password comes from an environment variable instead of source code.
# Example for local testing:
# PowerShell: $env:ADMIN_PASSWORD="change-me"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


def validate_ip_address(host):
    """Accept only valid IP addresses for this demo endpoint."""
    try:
        return str(ipaddress.ip_address(host))
    except ValueError:
        return None


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
    safe_host = validate_ip_address(host)

    if safe_host is None:
        return {"error": "Only valid IP addresses are allowed"}, 400

    ping_path = shutil.which("ping")

    if ping_path is None:
        return {"error": "ping command was not found"}, 500

    count_flag = "-n" if platform.system().lower() == "windows" else "-c"

    # Improvement: the host is validated, shell=True is avoided, and arguments
    # are passed as a list so shell metacharacters are not interpreted.
    # IP input is validated above.
    result = subprocess.check_output(  # nosec B603
        [ping_path, count_flag, "1", safe_host],
        text=True,
        stderr=subprocess.STDOUT,
        timeout=5,
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
