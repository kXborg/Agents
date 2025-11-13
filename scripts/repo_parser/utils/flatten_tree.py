def flatten_tree(tree, parent_path=""):
    """
    Recursively flattens nested repo tree structure into
    a list of file metadata dicts with folder information.
    """
    files = []
    for key, val in tree.items():
        # folder
        if isinstance(val, dict) and "type" not in val:
            files.extend(flatten_tree(val, parent_path + key))
        # file
        elif isinstance(val, dict) and val.get("type") == "file":
            files.append({**val, "folder": parent_path})
    return files
