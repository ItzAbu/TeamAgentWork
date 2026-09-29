"""Business logic del progetto."""


def add(a: float, b: float) -> float:
    """Somma due numeri."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Moltiplica due numeri."""
    return a * b


def calculate(expression: str) -> float:
    """
    Calcola una semplice espressione aritmetica.
    Supporta: addizione, sottrazione, moltiplicazione, divisione.
    Formato: 'a op b' dove op è uno di +, -, *, /
    """
    parts = expression.split()
    if len(parts) != 3:
        raise ValueError(f"Espressione non valida: '{expression}'. Usa formato 'a op b'.")
    
    a = float(parts[0])
    op = parts[1]
    b = float(parts[2])
    
    if op == "+":
        return add(a, b)
    elif op == "-":
        return a - b
    elif op == "*":
        return multiply(a, b)
    elif op == "/":
        if b == 0:
            raise ZeroDivisionError("Divisione per zero.")
        return a / b
    else:
        raise ValueError(f"Operatore non supportato: '{op}'")
