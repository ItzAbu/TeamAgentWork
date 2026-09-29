import sys
import pathlib

# Add the project’s src directory to sys.path so that tests can import the
# ``app`` package directly (e.g. ``from app.core import add``).
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
