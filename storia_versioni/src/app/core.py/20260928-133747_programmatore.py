"""
Core business logic for the application.
"""

def greet(name: str) -> str:
    """
    Return a greeting message for the given name.

    Parameters
    ----------
    name: str
        The name to greet.

    Returns
    -------
    str
        Greeting string.
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """
    Return the sum of two integers.

    Parameters
    ----------
    a: int
        First operand.
    b: int
        Second operand.

    Returns
    -------
    int
        The result of a + b.
    """
    return a + b
