import json


def clean_text(text):

    cleaned = text.replace("\n", " ")
    cleaned = cleaned.replace("\t", " ")

    return cleaned.strip()


def normalize_text(text):

    return text.lower().strip()


def remove_special_characters(text):

    special_characters = [
        ",",
        ".",
        ":",
        ";",
        "(",
        ")",
        "[",
        "]"
    ]

    for character in special_characters:
        text = text.replace(character, "")

    return text


def rank_candidates(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            candidates = json.load(file)

    except FileNotFoundError:
        print("Candidate data not found.")
        return

    except json.JSONDecodeError:
        print("Invalid candidate JSON format.")
        return

    sorted_candidates = sorted(
        candidates,
        key=lambda x: x.get("match_score", 0),
        reverse=True
    )

    print("\n================================")
    print(" TOP CANDIDATE RANKINGS")
    print("================================\n")

    for index, candidate in enumerate(sorted_candidates, start=1):
        print(
            f"{index}. {candidate.get('candidate_name', 'Unknown')} - "
            f"{candidate.get('match_score', 0)}"
        )

    print("\n================================\n")
