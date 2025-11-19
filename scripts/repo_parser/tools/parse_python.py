import ast

def parse_python(raw: str) -> str:
    """
    Extracts imports, classes, functions, and docstrings from a Python file.
    Returns a clean textual summary.
    """

    try:
        tree = ast.parse(raw)
    except Exception:
        # If AST fails (bad syntax), return cleaned raw text
        return _clean_raw_python(raw)

    imports = []
    functions = []
    classes = []
    docstrings = {}

    for node in ast.walk(tree):

        # Imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        if isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

        # Functions
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            docstrings[node.name] = ast.get_docstring(node) or ""

        # Classes
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
            docstrings[node.name] = ast.get_docstring(node) or ""
    
    summary = []

    if imports:
        summary.append("## Imports:\n" + "\n".join(f"- {i}" for i in imports))

    if classes:
        summary.append("## Classes:\n" + "\n".join(f"- {c}" for c in classes))

    if functions:
        summary.append("## Functions:\n" + "\n".join(f"- {f}" for f in functions))

    if docstrings:
        summary.append("## Docstrings:\n")
        for name, doc in docstrings.items():
            if doc:
                summary.append(f"### {name}\n{doc}\n")

    # Return readable summary
    # print(f"Summary Debug 2: {summary}")
    return "\n".join(summary) or _clean_raw_python(raw)


def _clean_raw_python(raw: str):
    """
    Fallback: remove excessive whitespace and comments.
    """
    cleaned = []
    for line in raw.splitlines():
        if line.strip().startswith("#"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)
