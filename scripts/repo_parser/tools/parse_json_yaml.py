# tools/parse_json_yaml.py
import json
import yaml

def parse_json_yaml(raw: str) -> str:
    """
    Safely prettify JSON or YAML.
    Returns clean structure up to a safe token limit.
    """

    # Try JSON first
    try:
        data = json.loads(raw)
        pretty = json.dumps(data, indent=2)
        return pretty[:5000]    # safe trimming
    except:
        pass

    # Try YAML
    try:
        data = yaml.safe_load(raw)
        pretty = yaml.dump(data, default_flow_style=False)
        return pretty[:5000]
    except:
        pass

    # Fallback = raw head
    return raw[:5000]
