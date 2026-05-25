import os
import re

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


class ResumeParser:

    SKILLS = {
        "python": ["python", "py"],
        "json": ["json"],
        "regex": ["regex", "regular expressions"],
        "file handling": ["file handling", "files"],
        "algorithms": ["algorithms", "problem solving"],
        "data structures": ["data structures", "dsa"],
        "debugging": ["debugging", "debug"]
    }

    def __init__(self, file_path):
        self.file_path = file_path

    def read_resume(self):
        extension = os.path.splitext(self.file_path)[1].lower()

        if extension == ".pdf":
            return self.read_pdf()

        return self.read_text()

    def read_text(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()

    def read_pdf(self):
        if PdfReader is None:
            raise RuntimeError(
                "PDF support requires the 'pypdf' package."
            )

        reader = PdfReader(self.file_path)
        text_pages = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text_pages.append(page_text)

        return "\n".join(text_pages)

    def extract_name(self, text):
        lines = text.split("\n")

        for line in lines:
            cleaned = line.strip()

            if cleaned:
                return cleaned

        return "Unknown"

    def extract_email(self, text):
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        match = re.search(pattern, text)

        return match.group() if match else "Not Found"

    def extract_phone(self, text):
        pattern = r"\b\d{10}\b"

        match = re.search(pattern, text)

        return match.group() if match else "Not Found"

    def extract_experience(self, text):
        pattern = r"(\d+)\s+years?"

        match = re.search(pattern, text.lower())

        return int(match.group(1)) if match else 0

    def extract_education(self, text):
        education_keywords = [
            "b.tech",
            "bachelor",
            "m.tech",
            "master",
            "bsc",
            "msc"
        ]

        text = text.lower()

        for education in education_keywords:
            if education in text:
                return education

        return "Not Found"

    def extract_skills(self, text):
        text = text.lower()

        detected_skills = []

        for main_skill, aliases in self.SKILLS.items():

            for alias in aliases:

                if alias in text:
                    detected_skills.append(main_skill)
                    break

        return list(set(detected_skills))

    def parse_resume(self):
        text = self.read_resume()

        return {
            "candidate_name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "skills": self.extract_skills(text),
            "experience": self.extract_experience(text),
            "education": self.extract_education(text)
        }