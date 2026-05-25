"""Generate plain-text recruiter reports from candidate analysis results."""

from pathlib import Path
from typing import Dict


def _sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in name).strip().replace(" ", "_")


def generate_report(result: Dict[str, object], report_folder: Path | str) -> str:
    """Create a human-readable plain-text report and return its path.

    The function is resilient to missing fields and always returns the
    path where the report was written.
    """
    folder = Path(report_folder)
    folder.mkdir(parents=True, exist_ok=True)

    candidate = str(result.get("candidate_name") or "candidate")
    filename = f"{_sanitize_filename(candidate)}_report.txt"
    report_path = folder / filename

    lines = [
        "====================================",
        " SMART HIRE RESUME ANALYSIS REPORT",
        "====================================\n",
        f"Candidate Name : {result.get('candidate_name', 'N/A')}",
        f"Email          : {result.get('email', 'N/A')}",
        f"Phone          : {result.get('phone', 'N/A')}",
        f"Experience     : {result.get('experience', 'N/A')} years",
        f"Education      : {result.get('education', 'N/A')}\n",
        "Matched Skills:",
    ]

    for s in result.get("matched_skills", []):
        lines.append(f"- {s}")

    lines.append("\nMissing Skills:")
    for s in result.get("missing_skills", []):
        lines.append(f"- {s}")

    lines.extend([
        f"\nFinal Match Score : {result.get('match_score', 0)}/100",
        f"Recommendation    : {result.get('recommendation', 'N/A')}",
    ])

    report_text = "\n".join(lines)

    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(report_text)

    return str(report_path)