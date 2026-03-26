from PyPDF2 import PdfReader
import json
import os
from datetime import datetime

RESULT_FILE = "/app/scan_results.json"


def scan_files(file_paths: list[str]) -> list:
    results = [scan_single_file(f) for f in file_paths]

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f)

    print("Saved results to:", RESULT_FILE)

    return results



def scan_single_file(file_path: str) -> dict:
    issues = []
    fixable_issues = []
    total_checks = 3
    passed = 0

    try:
        reader = PdfReader(file_path)

        # Check 1: Metadata
        if reader.metadata and reader.metadata.title:
            passed += 1
        else:
            msg = "Missing document title metadata"
            issues.append(msg)
            fixable_issues.append(msg)  # assuming fixable

        # Check 2: Text layer
        if any(page.extract_text() for page in reader.pages):
            passed += 1
        else:
            msg = "No text layer (scanned PDF)"
            issues.append(msg)
            # not easily fixable → don't add to fixable_issues

        # Check 3: Empty pages
        empty_pages = sum(1 for p in reader.pages if not p.extract_text())
        if empty_pages == 0:
            passed += 1
        else:
            msg = f"{empty_pages} empty pages"
            issues.append(msg)
            fixable_issues.append(msg)  # assuming fixable

    except Exception as e:
        issues.append(f"Error reading file: {str(e)}")

    total_issues = len(issues)
    total_fixable = len(fixable_issues)

    # ✅ Consistency Check
    if total_fixable > total_issues:
        return {
            "file": file_path,
            "error": "Inconsistent counts: totalFixable exceeds totalIssues",
            "totalIssues": total_issues,
            "totalFixable": total_fixable,
            "timestamp": datetime.utcnow().isoformat()
        }

    score = (passed / total_checks) * 100 if total_checks else 0
    # convert issues to structured format
    structured_issues = [
        {
            "description": issue,
            "fix": "Add OCR text layer or ensure selectable text is present for accessibility."
            if "text layer" in issue.lower() or "scanned" in issue.lower()
            else "Review and fix the reported accessibility issue."
        }
        for issue in issues
    ]

    return {
        "file": file_path,
        "score": round(score, 2),
        "issues": structured_issues,
        "totalIssues": total_issues,
        "totalFixable": total_fixable,
        "fixed": False,
        "timestamp": datetime.utcnow().isoformat()
    }