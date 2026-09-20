"""
Core calculator logic — kept free of any UI code so it can be unit tested
without needing a display or a tkinter event loop.
"""

# Maps the "pretty" symbols shown on screen to real Python operators
DISPLAY_TO_PYTHON = {"×": "*", "÷": "/", "−": "-", "%": "%"}
PYTHON_TO_DISPLAY = {"*": "×", "/": "÷", "-": "−"}

# Only these characters are ever allowed in an expression before it's evaluated
ALLOWED_CHARS = set("0123456789.+-*/%()")


def to_python_expression(display_expression: str) -> str:
    """Convert a display-friendly expression (with ×, ÷, −) to valid Python."""
    expression = display_expression
    for symbol, operator in DISPLAY_TO_PYTHON.items():
        expression = expression.replace(symbol, operator)
    return expression


def to_display_expression(python_expression: str) -> str:
    """Convert a Python expression back into the friendly display form."""
    expression = python_expression
    for operator, symbol in PYTHON_TO_DISPLAY.items():
        expression = expression.replace(operator, symbol)
    return expression


def format_result(result) -> str:
    """Format a numeric result: drop trailing .0 for whole numbers, round floats."""
    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    if isinstance(result, float):
        return str(round(result, 10))
    return str(result)


def safe_eval(expression: str) -> float:
    """
    Evaluate a simple arithmetic expression safely.

    Raises:
        ValueError: if the expression contains disallowed characters or is empty.
        ZeroDivisionError: if the expression divides by zero.
        SyntaxError: if the expression is not valid arithmetic.
    """
    if not expression:
        raise ValueError("Empty expression")

    if not set(expression) <= ALLOWED_CHARS:
        raise ValueError(f"Invalid characters in expression: {expression!r}")

    # eval with no builtins available — only arithmetic operators can run
    return eval(expression, {"__builtins__": {}})


def evaluate_display_expression(display_expression: str) -> str:
    """
    Take a display-friendly expression, evaluate it, and return the
    display-friendly formatted result (or an error string).
    """
    try:
        python_expr = to_python_expression(display_expression)
        result = safe_eval(python_expr)
        return format_result(result)
    except ZeroDivisionError:
        return "Error: ÷0"
    except Exception:
        return "Error"
