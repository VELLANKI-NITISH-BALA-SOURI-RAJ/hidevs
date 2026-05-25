"""Simple JSON helpers for requirements and candidate storage.

Provides functions to load job requirements and to store candidate
analyses in a de-duplicated JSON array. The functions handle common
errors and keep the API small for educational use.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


OUTPUT_FILE = Path("candidates.json")


def load_requirements(file_path: str) -> Dict[str, Any]:
    """Load job requirements from a JSON file.

    Returns an empty dict on error.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        print("Requirements file not found.")
        return {}
    except json.JSONDecodeError:
        print("Invalid JSON format in requirements file.")
        return {}


def load_candidates(file_path: Path | None = None) -> List[Dict[str, Any]]:
    """Return the list of saved candidate analyses.

    If the file doesn't exist or is invalid, an empty list is returned.
    """
    path = file_path or OUTPUT_FILE
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return []


def save_candidate_analysis(candidate_result: Dict[str, Any], file_path: Path | None = None) -> None:
    """Save or update a candidate analysis in the JSON store.

    De-duplicates entries by `email` if available, otherwise by candidate name.
    """
    path = file_path or OUTPUT_FILE
    data = load_candidates(path)

    key_map: Dict[str, Dict[str, Any]] = {}
    for item in data:
        key = item.get("email") or item.get("candidate_name")
        if key:
            key_map[key] = item

    incoming_key = candidate_result.get("email") or candidate_result.get("candidate_name")
    if incoming_key:
        key_map[incoming_key] = candidate_result
        deduped = list(key_map.values())
    else:
        # Fallback: append if no reliable key
        deduped = data + [candidate_result]

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(deduped, fh, indent=4)


# Backwards-compatible name
def save_analysis(candidate_result: Dict[str, Any]) -> None:
    save_candidate_analysis(candidate_result)
