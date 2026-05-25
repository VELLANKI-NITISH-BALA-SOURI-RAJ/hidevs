"""Matching logic to compute scores between candidate and job requirements."""

from typing import Dict, List, Tuple


class ResumeMatcher:
    """Compute a candidate match score against job requirements.

    The scoring model is intentionally transparent and simple:
      - Required skills: 50 points total
      - Preferred skills: 20 points total
      - Experience: 20 points total
      - Education: 10 points total
    """

    def __init__(self, candidate_data: Dict, requirements: Dict) -> None:
        self.candidate = candidate_data
        self.requirements = requirements

    def _skill_match(self) -> Tuple[float, List[str]]:
        required = [s.lower() for s in self.requirements.get("required_skills", [])]
        candidate = {s.lower() for s in self.candidate.get("skills", [])}

        if not required:
            return 0.0, []

        matched = [s for s in required if s in candidate]
        score = (len(matched) / len(required)) * 50.0
        return score, matched

    def _preferred_match(self) -> float:
        preferred = [s.lower() for s in self.requirements.get("preferred_skills", [])]
        candidate = {s.lower() for s in self.candidate.get("skills", [])}
        if not preferred:
            return 0.0
        return (len([p for p in preferred if p in candidate]) / len(preferred)) * 20.0

    def _experience_score(self) -> float:
        required = self.requirements.get("minimum_experience", 0)
        candidate_years = int(self.candidate.get("experience", 0) or 0)
        if candidate_years >= required:
            return 20.0
        if candidate_years > 0:
            return 10.0
        return 0.0

    def _education_score(self) -> float:
        required = str(self.requirements.get("education", "")).lower()
        candidate = str(self.candidate.get("education", "")).lower()
        return 10.0 if required and required in candidate else 0.0

    def calculate_match_score(self) -> Dict[str, object]:
        skill_score, matched_skills = self._skill_match()
        preferred_score = self._preferred_match()
        experience_score = self._experience_score()
        education_score = self._education_score()

        total = skill_score + preferred_score + experience_score + education_score

        required_skills = [s for s in self.requirements.get("required_skills", [])]
        missing = [s for s in required_skills if s.lower() not in {m.lower() for m in matched_skills}]

        return {
            "candidate_name": self.candidate.get("candidate_name"),
            "email": self.candidate.get("email"),
            "phone": self.candidate.get("phone"),
            "skills": self.candidate.get("skills", []),
            "experience": self.candidate.get("experience", 0),
            "education": self.candidate.get("education", "Not Found"),
            "matched_skills": matched_skills,
            "missing_skills": missing,
            "match_score": round(total, 2),
            "recommendation": self.generate_recommendation(total),
        }

    @staticmethod
    def generate_recommendation(score: float) -> str:
        if score >= 80:
            return "Strong Match"
        if score >= 60:
            return "Moderate Match"
        return "Weak Match"