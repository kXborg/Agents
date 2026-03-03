docs = {
    "aws": "AWS is Amazon's cloud platform.",
    "agent": "An agent uses LLM + tools to take actions.",
    "mcp": "Model Context Protocol allows structured tool calling."
}

def simple_search(query: str):
    for key, value in docs.items():
        if key in query.lower():
            return value
    return "No relevant document found."