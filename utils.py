"""Utility helpers used across the SmartHire project.

Small, self-contained helpers for text normalization and a utility
to rank candidates stored in a JSON file.
"""

from __future__ import annotations

import json
from typing import List, Dict


def clean_text(text: str) -> str:
    """Normalize whitespace characters in `text` to single spaces."""
    return text.replace("\n", " ").replace("\t", " ").strip()


def normalize_text(text: str) -> str:
    """Return a lower-cased, trimmed copy of `text`."""
    return text.lower().strip()


def remove_special_characters(text: str) -> str:
    """Strip a small set of punctuation characters used in resumes."""
    for ch in [",", ".", ":", ";", "(", ")", "[", "]"]:
        text = text.replace(ch, "")
    return text


def rank_candidates(file_path: str) -> List[Dict]:
    """Load candidate analyses from JSON and print a ranked list.

    Returns the sorted candidate list for further programmatic use.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            candidates = json.load(fh)
    except FileNotFoundError:
        print("Candidate data not found.")
        return []
    except json.JSONDecodeError:
        print("Invalid candidate JSON format.")
        return []

    sorted_candidates = sorted(candidates, key=lambda x: x.get("match_score", 0), reverse=True)

    print("\n================================")
    print(" TOP CANDIDATE RANKINGS")
    print("================================\n")
    for i, c in enumerate(sorted_candidates, 1):
        print(f"{i}. {c.get('candidate_name', 'Unknown')} - {c.get('match_score', 0)}")
    print("\n================================\n")

    return sorted_candidates
