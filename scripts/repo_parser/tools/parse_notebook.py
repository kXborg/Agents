# tools/parse_notebook.py
import nbformat

def parse_notebook(raw: str) -> str:
    """
    Extracts markdown + code cells from a .ipynb file.
    Converts them to readable text for LLMs.
    """

    try:
        nb = nbformat.reads(raw, as_version=4)
    except Exception:
        return raw[:5000]

    out = []

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            out.append("## Markdown Cell:\n" + cell.source)
        elif cell.cell_type == "code":
            out.append("## Code Cell:\n" + cell.source)
    # print(f"Checking Execution of parse_notebook tool: {out}")

    return "\n\n".join(out)[:8000]
