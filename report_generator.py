import os


def generate_report(result, report_folder):

    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    filename = (
        result["candidate_name"]
        .replace(" ", "_")
        + "_report.txt"
    )

    report_path = os.path.join(
        report_folder,
        filename
    )

    with open(report_path, "w") as file:

        file.write(
            "====================================\n"
        )

        file.write(
            " SMART HIRE RESUME ANALYSIS REPORT\n"
        )

        file.write(
            "====================================\n\n"
        )

        file.write(
            f"Candidate Name : "
            f"{result['candidate_name']}\n"
        )

        file.write(
            f"Email          : "
            f"{result['email']}\n"
        )

        file.write(
            f"Phone          : "
            f"{result['phone']}\n"
        )

        file.write(
            f"Experience     : "
            f"{result['experience']} years\n"
        )

        file.write(
            f"Education      : "
            f"{result['education']}\n\n"
        )

        file.write("Matched Skills:\n")

        for skill in result["matched_skills"]:
            file.write(f"- {skill}\n")

        file.write("\nMissing Skills:\n")

        for skill in result["missing_skills"]:
            file.write(f"- {skill}\n")

        file.write(
            f"\nFinal Match Score : "
            f"{result['match_score']}/100\n"
        )

        file.write(
            f"Recommendation    : "
            f"{result['recommendation']}\n"
        )

    return report_path