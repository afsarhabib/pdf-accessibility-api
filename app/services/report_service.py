import json
import os
from collections import Counter

RESULT_FILE = "/app/scan_results.json"

def generate_report():
    print("Looking for:", RESULT_FILE)

    if not os.path.exists(RESULT_FILE):
        return {"message": "No scans available"}

    with open(RESULT_FILE, "r") as f:
        results = json.load(f)

    if not results:
        return {"message": "No scans available"}

    total_files = len(results)
    total_issues = sum(len(r["issues"]) for r in results)

    avg_score = sum(r["score"] for r in results) / total_files
    worst_file = min(results, key=lambda x: x["score"])["file"]

    status_summary = {"compliant": 0, "partial": 0, "non_compliant": 0}

    for r in results:
        if r["score"] >= 90:
            status_summary["compliant"] += 1
        elif r["score"] >= 60:
            status_summary["partial"] += 1
        else:
            status_summary["non_compliant"] += 1

    # Collect all issues
    all_issues = []
    for r in results:
        all_issues.extend(r["issues"])

    # Count occurrences
    issue_trends = dict(Counter(all_issues))
    total_fixed = sum(1 for r in results if r.get("fixed"))

    return {
        "total_files": total_files,
        "total_issues": total_issues,
        "average_score": round(avg_score, 2),
        "worst_file": worst_file,
        "status_summary": status_summary,
        "issue_trends": issue_trends,
        "total_fixed": total_fixed,
        "files": results
    }