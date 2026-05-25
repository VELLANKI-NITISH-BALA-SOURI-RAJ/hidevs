# SmartHire Resume Analyzer

## Description

SmartHire Resume Analyzer is a Python-based application
that automates resume screening.

The system:
- extracts candidate information
- analyzes resumes
- calculates match scores
- generates recruiter reports
- stores results in JSON format

---

# Features

- Resume Parsing
- Skill Extraction
- Match Score Calculation
- JSON File Handling
- Hiring Recommendations
- Professional Report Generation
- Multiple Resume Analysis

---

# Technologies Used

- Python
- Regular Expressions
- JSON
- File Handling
- Matching Algorithms

---

# Project Structure

project/
│
├── main.py
├── parser.py
├── matcher.py
├── report_generator.py
├── json_handler.py
├── utils.py
│
├── resumes/
├── reports/
│
├── requirements.json
├── candidates.json
└── README.md

---

# How to Run

## Step 1

Place resumes inside the resumes folder.

Supported formats:
- TXT
- PDF

Example resume files can be added to the `resumes/` folder to run the analyzer.

---

## Step 2

Run the command-line program:

python main.py

---

## Step 3

Run the Streamlit UI:

python -m streamlit run app.py

Supported resume formats in the UI:
- TXT
- PDF

---

# Output

The system generates:
- Match Scores
- Hiring Recommendations
- JSON Candidate Data
- Text Reports

---

# Evaluation Criteria Covered

✔ Python Programming  
✔ Text Processing  
✔ Data Extraction Algorithms  
✔ JSON File Handling  
✔ Matching Algorithms  
✔ Error Handling  
✔ Report Generation

---

# Future Improvements

- PDF Resume Support
- GUI Interface
- Advanced Ranking System
- Better Skill Intelligence"# hidevs" 
