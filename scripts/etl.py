import json
# minor ETL update
# Load raw data
with open('data/bronze/jobs.json') as f:
    jobs = json.load(f)

clean_jobs = []

for job in jobs:
    clean_jobs.append({
        "title": job["title"].lower(),
        "skills": job["description"].lower().split(", ")
    })

# Save cleaned data
with open('data/silver/clean_jobs.json', 'w') as f:
    json.dump(clean_jobs, f, indent=2)

print("ETL completed!")