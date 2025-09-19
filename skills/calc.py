# skills/calc.py
import math
import re

SAFE_FUNCS = {
    "abs": abs, "round": round,
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "pi": math.pi, "e": math.e
}

def handle_calc(entities):
    expr = entities.get("expr")
    if not expr:
        return "Calc what? e.g., calc 2+2*3"
    # Very minimal safety: only digits, operators, parentheses, dot, spaces, and known names
    if not re.fullmatch(r"[0-9+\-*/().\s^%eipasincoqrtdu]+", expr):
        return "Sorry, that looks unsafe."
    expr = expr.replace("^", "**")
    try:
        val = eval(expr, {"__builtins__": {}}, SAFE_FUNCS)
        return f"{expr} = {val}"
    except Exception as e:
        return f"Error: {e}"
