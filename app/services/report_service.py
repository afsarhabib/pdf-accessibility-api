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

    # Compliance breakdown
    compliant = sum(1 for r in results if r["complianceStatus"] == "compliant")
    non_compliant = total_files - compliant

    compliance_breakdown = {
        "compliant": compliant,
        "nonCompliant": non_compliant
    }

    # Worst file
    worst = max(results, key=lambda x: x.get("nonCompliancePercent", 0))

    worst_file = {
        "fileName": worst.get("fileName"),
        "nonCompliancePercent": worst.get("nonCompliancePercent")
    }

    # Collect issue types
    issue_counter = Counter()

    for r in results:
        for issue in r["issues"]:
            key = issue.get("description")
            issue_counter[key] += 1

    top_issue_types = [
        {"issue": k, "count": v}
        for k, v in issue_counter.items()
    ]

    # Standard violation frequency
    standard_counter = Counter()

    for r in results:
        for issue in r["issues"]:
            standard = issue.get("standard")
            standard_counter[standard] += 1

    standard_violation_frequency = dict(standard_counter)

    return {
        "totalFiles": total_files,
        "totalIssues": total_issues,
        "complianceBreakdown": compliance_breakdown,
        "topIssueTypes": top_issue_types,
        "standardViolationFrequency": standard_violation_frequency,
        "worstFile": worst_file,
        "files": results
    }