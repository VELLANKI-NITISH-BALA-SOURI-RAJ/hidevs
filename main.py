import os
from parser import ResumeParser
from matcher import ResumeMatcher
from json_handler import load_requirements, save_analysis
from report_generator import generate_report
from utils import rank_candidates

RESUME_FOLDER = "resumes"
REPORT_FOLDER = "reports"


def analyze_resume(file_path, requirements):
    parser = ResumeParser(file_path)
    candidate_data = parser.parse_resume()

    matcher = ResumeMatcher(candidate_data, requirements)
    result = matcher.calculate_match_score()

    save_analysis(result)

    report_path = generate_report(result, REPORT_FOLDER)

    print("\n===================================")
    print(" Resume Analysis Completed")
    print("===================================")
    print(f"Candidate : {result['candidate_name']}")
    print(f"Score     : {result['match_score']}")
    print(f"Report    : {report_path}")
    print("===================================\n")


def main():
    requirements = load_requirements("requirements.json")

    if not os.path.exists(RESUME_FOLDER):
        print("Resume folder not found.")
        return

    resumes = os.listdir(RESUME_FOLDER)

    if not resumes:
        print("No resumes found.")
        return

    for resume in resumes:
        file_path = os.path.join(RESUME_FOLDER, resume)

        try:
            analyze_resume(file_path, requirements)

        except Exception as error:
            print(f"Error processing {resume}: {error}")

    rank_candidates("candidates.json")


if __name__ == "__main__":
    main()