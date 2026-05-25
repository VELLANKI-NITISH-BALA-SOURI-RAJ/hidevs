import json
import os

OUTPUT_FILE = "candidates.json"


def load_requirements(file_path):

    try:
        with open(file_path, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print("Requirements file not found.")
        return {}

    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return {}


def save_analysis(candidate_result):

    data = []

    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

    unique_candidates = {}
    for existing in data:
        key = existing.get("email") or existing.get("candidate_name")
        if key:
            unique_candidates[key] = existing

    incoming_key = candidate_result.get("email") or candidate_result.get("candidate_name")
    if incoming_key:
        unique_candidates[incoming_key] = candidate_result
    else:
        data.append(candidate_result)

    deduped_data = list(unique_candidates.values())
    if not incoming_key:
        deduped_data = data

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(deduped_data, file, indent=4)
