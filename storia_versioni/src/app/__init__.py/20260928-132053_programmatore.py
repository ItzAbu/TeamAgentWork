"""
app package initialization.

Exports the public interface of the package.
"""

from .cli import cli  # noqa: F401
from .core import add  # noqa: F401

__all__ = ["cli", "add"]
