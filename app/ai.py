import json

def load_jobs():
    with open('data/silver/clean_jobs.json') as f:
        return json.load(f)

def find_jobs_by_skill(skill):
    jobs = load_jobs()
    result = []

    for job in jobs:
        if skill.lower() in job["skills"]:
            result.append(job["title"])

    return result