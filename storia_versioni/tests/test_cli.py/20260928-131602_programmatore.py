import subprocess
import sys
import os

def run_cli(args):
    """Helper to run the CLI command."""
    env = os.environ.copy()
    # Ensure the src directory is on PYTHONPATH
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(
        [sys.executable, "-m", "app.cli"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
    )
    return result

def test_cli_add():
    result = run_cli(["add", "4", "5"])
    assert result.returncode == 0
    assert "Result: 9" in result.stdout

def test_cli_help():
    result = run_cli(["--help"])
    assert result.returncode == 0
    assert "Usage:" in result.stdout
