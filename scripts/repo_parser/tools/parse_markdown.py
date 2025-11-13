# tools/parse_markdown.py
import re

def parse_markdown(raw: str) -> str:
    """
    Clean markdown / text files for LLM processing.
    Removes HTML, collapses whitespace, keeps headings.
    """
    # Remove HTML tags
    cleaned = re.sub(r"<[^>]+>", "", raw)

    # Strip extra whitespace
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = cleaned.strip()

    return cleaned
