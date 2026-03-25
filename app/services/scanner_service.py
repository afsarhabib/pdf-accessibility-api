from PyPDF2 import PdfReader
import json
import os
from datetime import datetime

RESULT_FILE = "/app/scan_results.json"


def scan_files(file_paths: list[str]) -> list:
    raw_results = [scan_single_file(f) for f in file_paths]

    formatted_results = []

    for r in raw_results:
        issues = r.get("issues", [])

        non_compliance = 0 if len(issues) == 0 else min(100, len(issues) * 25)

        formatted_results.append({
            "fileName": os.path.basename(r.get("file")),
            "nonCompliancePercent": non_compliance,
            "complianceStatus": "compliant" if non_compliance == 0 else "non-compliant",
            "issues": issues
        })

    with open(RESULT_FILE, "w") as f:
        json.dump(formatted_results, f)

    print("Saved results to:", RESULT_FILE)

    return formatted_results


def scan_single_file(file_path: str) -> dict:
    issues = []
    total_checks = 3
    passed = 0

    try:
        reader = PdfReader(file_path)

        # Check 1: Metadata
        if reader.metadata and reader.metadata.title:
            passed += 1
        else:
            issues.append({
                "description": "Missing document title metadata",
                "category": "Metadata",
                "standard": "WCAG 2.1 - Document Title"
            })

        # Check 2: Text layer
        if any(page.extract_text() for page in reader.pages):
            passed += 1
        else:
            issues.append({
                "description": "No text layer (scanned PDF)",
                "category": "Accessibility",
                "standard": "WCAG 2.1 SC 1.4"
            })

        # Check 3: Empty pages
        empty_pages = sum(1 for p in reader.pages if not p.extract_text())
        if empty_pages == 0:
            passed += 1
        else:
            issues.append({
                "description": f"{empty_pages} empty pages detected",
                "category": "Content",
                "standard": "Document Structure"
            })

    except Exception as e:
        issues.append({
            "description": f"Error reading file: {str(e)}",
            "category": "Processing",
            "standard": "System"
        })

    return {
        "file": file_path,
        "issues": issues
    }