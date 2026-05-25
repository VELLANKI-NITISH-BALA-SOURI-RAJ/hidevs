class ResumeMatcher:

    def __init__(self, candidate_data, requirements):
        self.candidate = candidate_data
        self.requirements = requirements

    def calculate_skill_score(self):
        required_skills = self.requirements["required_skills"]
        candidate_skills = self.candidate["skills"]

        matched = []

        for skill in required_skills:
            if skill.lower() in candidate_skills:
                matched.append(skill)

        skill_score = (
            len(matched) / len(required_skills)
        ) * 50

        return skill_score, matched

    def calculate_preferred_score(self):
        preferred = self.requirements["preferred_skills"]
        candidate_skills = self.candidate["skills"]

        matched = []

        for skill in preferred:
            if skill.lower() in candidate_skills:
                matched.append(skill)

        score = (
            len(matched) / len(preferred)
        ) * 20

        return score

    def calculate_experience_score(self):
        required_exp = self.requirements["minimum_experience"]
        candidate_exp = self.candidate["experience"]

        if candidate_exp >= required_exp:
            return 20

        elif candidate_exp > 0:
            return 10

        return 0

    def calculate_education_score(self):
        required_education = (
            self.requirements["education"].lower()
        )

        candidate_education = (
            self.candidate["education"].lower()
        )

        if required_education in candidate_education:
            return 10

        return 0

    def calculate_match_score(self):
        skill_score, matched_skills = (
            self.calculate_skill_score()
        )

        preferred_score = (
            self.calculate_preferred_score()
        )

        experience_score = (
            self.calculate_experience_score()
        )

        education_score = (
            self.calculate_education_score()
        )

        total_score = (
            skill_score +
            preferred_score +
            experience_score +
            education_score
        )

        missing_skills = []

        for skill in self.requirements["required_skills"]:
            if skill not in matched_skills:
                missing_skills.append(skill)

        recommendation = self.generate_recommendation(
            total_score
        )

        return {
            "candidate_name": self.candidate["candidate_name"],
            "email": self.candidate["email"],
            "phone": self.candidate["phone"],
            "skills": self.candidate["skills"],
            "experience": self.candidate["experience"],
            "education": self.candidate["education"],
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "match_score": round(total_score, 2),
            "recommendation": recommendation
        }

    def generate_recommendation(self, score):

        if score >= 80:
            return "Strong Match"

        if score >= 60:
            return "Moderate Match"

        return "Weak Match"