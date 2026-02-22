import datetime
import os
from pathlib import Path


def fs_inspect(path: str = ".", depth: int = 1, include_hidden: bool = False) -> dict:
    """
    Inspects the filesystem at a given path without modification.

    Args:
        path (str): The starting path to inspect. Defaults to ".".
        depth (int): The maximum depth to traverse. 1 means only the contents of the path.
        include_hidden (bool): Whether to include hidden files and directories.

    Returns:
        dict: A dictionary representing the filesystem structure.
    """
    root_path = Path(path)
    if not root_path.exists():
        return {"error": f"Path not found: {path}"}

    def _format_time(timestamp):
        return datetime.datetime.fromtimestamp(timestamp).isoformat()

    def _inspect_path(current_path: Path, current_depth: int):
        if current_depth > depth:
            return None

        try:
            items = []
            for item in current_path.iterdir():
                if not include_hidden and item.name.startswith("."):
                    continue

                try:
                    stat = item.stat()
                    item_details = {
                        "name": item.name,
                        "path": str(item),
                        "is_dir": item.is_dir(),
                        "size_bytes": stat.st_size,
                        "modified_at": _format_time(stat.st_mtime),
                    }
                    if item.is_dir():
                        children = _inspect_path(item, current_depth + 1)
                        if children is not None:
                            item_details["children"] = children
                    items.append(item_details)
                except (OSError, PermissionError):
                    # Skip files we can't access
                    continue
            return items
        except (OSError, PermissionError):
            return {"error": f"Permission denied to read: {current_path}"}

    stat = root_path.stat()
    return {
        "path": str(root_path),
        "is_dir": root_path.is_dir(),
        "size_bytes": stat.st_size,
        "modified_at": _format_time(stat.st_mtime),
        "children": _inspect_path(root_path, 1) if root_path.is_dir() else [],
    }
