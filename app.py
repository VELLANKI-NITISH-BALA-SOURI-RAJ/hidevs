import os
import json

import streamlit as st
from parser import ResumeParser
from matcher import ResumeMatcher
from report_generator import generate_report
from json_handler import load_requirements, save_analysis
from utils import rank_candidates

RESUME_FOLDER = "resumes"
REPORT_FOLDER = "reports"
CANDIDATE_FILE = "candidates.json"
REQUIREMENTS_FILE = "requirements.json"

if not os.path.exists(RESUME_FOLDER):
    os.makedirs(RESUME_FOLDER)

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


def analyze_uploaded_resume(uploaded_file):
    file_name = uploaded_file.name
    file_path = os.path.join(RESUME_FOLDER, file_name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    requirements = load_requirements(REQUIREMENTS_FILE)
    parser = ResumeParser(file_path)
    candidate_data = parser.parse_resume()

    matcher = ResumeMatcher(candidate_data, requirements)
    result = matcher.calculate_match_score()

    save_analysis(result)
    report_path = generate_report(result, REPORT_FOLDER)

    return result, report_path


def display_candidate_summary(result, report_path):
    st.subheader("Candidate Summary")
    st.write(f"**Name:** {result['candidate_name']}")
    st.write(f"**Email:** {result['email']}")
    st.write(f"**Phone:** {result['phone']}")
    st.write(f"**Experience:** {result['experience']} years")
    st.write(f"**Education:** {result['education']}")
    st.write(f"**Match Score:** {result['match_score']}/100")
    st.write(f"**Recommendation:** {result['recommendation']}")
    st.write(f"**Report Path:** {report_path}")

    st.markdown("**Matched Skills:**")
    for skill in result["matched_skills"]:
        st.write(f"- {skill}")

    st.markdown("**Missing Skills:**")
    for skill in result["missing_skills"]:
        st.write(f"- {skill}")


def load_candidate_rankings(file_path):
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            candidates = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

    return sorted(candidates, key=lambda x: x.get("match_score", 0), reverse=True)


def main():
    st.set_page_config(
        page_title="SmartHire UI",
        page_icon="🧠",
        layout="wide"
    )

    st.title("SmartHire Resume Analyzer UI")
    st.markdown(
        "Upload a resume and analyze match scores, then view candidate rankings."
    )

    with st.sidebar:
        st.header("Upload Guide")
        st.write("Supported resume formats: TXT, PDF")
        st.write("The uploaded resume is saved in the `resumes/` folder.")
        st.write("Generated reports are stored in the `reports/` folder.")

        st.header("Quick Actions")
        if st.button("Show ranking list"):
            st.session_state.show_rankings = True

    uploaded_file = st.file_uploader(
        "Upload resume for analysis",
        type=["txt", "pdf"],
        help="Upload a .txt or .pdf resume file."
    )

    if uploaded_file:
        st.info(f"Uploaded file: {uploaded_file.name}")
        if st.button("Analyze Resume"):
            try:
                result, report_path = analyze_uploaded_resume(uploaded_file)
                display_candidate_summary(result, report_path)
                st.success("Resume analyzed successfully.")
            except Exception as exc:
                st.error(f"Error analyzing resume: {exc}")

    rankings = load_candidate_rankings(CANDIDATE_FILE)
    if st.checkbox("Display candidate rankings", value=False) or st.session_state.get("show_rankings"):
        st.subheader("Candidate Rankings")
        if not rankings:
            st.warning("No candidate rankings available yet.")
        else:
            for index, candidate in enumerate(rankings, start=1):
                st.write(
                    f"{index}. {candidate.get('candidate_name', 'Unknown')} "
                    f"- {candidate.get('match_score', 0)}"
                )


if __name__ == "__main__":
    main()
