"""Command-line runner for SmartHire Resume Analyzer.

This script iterates through resumes in the `resumes/` folder,
parses each file, computes a match score against `requirements.json`,
saves the result and generates a text report for recruiters.

The CLI is intentionally simple to remain beginner-friendly.
"""

from pathlib import Path
import logging
import argparse
from typing import Dict

from parser import ResumeParser
from matcher import ResumeMatcher
from json_handler import load_requirements, save_analysis
from report_generator import generate_report
from utils import rank_candidates


LOG = logging.getLogger("smart_hire")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


RESUME_DIR = Path("resumes")
REPORT_DIR = Path("reports")
REQUIREMENTS_FILE = Path("requirements.json")
PRINT_RANKINGS = True


def analyze_resume(path: Path, requirements: Dict) -> Path:
    """Parse, match and create a report for a single resume file.

    Args:
        path: Path to the resume file (txt or pdf).
        requirements: Loaded job requirements dictionary.

    Returns:
        Path to the generated report file.
    """
    LOG.info("Processing %s", path.name)

    parser = ResumeParser(str(path))
    candidate = parser.parse_resume()

    matcher = ResumeMatcher(candidate, requirements)
    result = matcher.calculate_match_score()

    save_analysis(result)
    report_path = generate_report(result, REPORT_DIR)

    LOG.info("Completed: %s (score: %s)", result.get("candidate_name"), result.get("match_score"))
    return report_path


def main(resume_path: Path | None = None) -> None:
    """Main entry point.

    If `resume_path` is provided, analyze the single file. Otherwise,
    iterate all files in the `resumes/` directory.
    """
    requirements = load_requirements(REQUIREMENTS_FILE)

    if resume_path:
        if not resume_path.exists():
            LOG.error("Specified resume not found: %s", resume_path)
            return
        analyze_resume(resume_path, requirements)
    else:
        if not RESUME_DIR.exists():
            LOG.error("Resume folder not found: %s", RESUME_DIR)
            return

        files = sorted([p for p in RESUME_DIR.iterdir() if p.is_file()])
        if not files:
            LOG.info("No resumes found in %s", RESUME_DIR)
            return

        for file_path in files:
            try:
                analyze_resume(file_path, requirements)
            except Exception as exc:  # pragma: no cover - top-level safety
                LOG.exception("Error while processing %s: %s", file_path.name, exc)

    if PRINT_RANKINGS:
        rank_candidates(Path("candidates.json"))


def _cli() -> None:
    parser = argparse.ArgumentParser(description="SmartHire Resume Analyzer CLI")
    parser.add_argument("--file", "-f", type=str, help="Optional single resume file to analyze")
    args = parser.parse_args()

    resume_file = Path(args.file) if args.file else None
    main(resume_file)


if __name__ == "__main__":
    _cli()