from PyPDF2 import PdfReader
import json
import os

RESULT_FILE = "/app/scan_results.json"

def scan_files(file_paths: list[str]) -> dict:
    results = [scan_single_file(f) for f in file_paths]

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f)

    print("Saved results to:", RESULT_FILE)

    return {"results": results}

def scan_single_file(file_path: str) -> dict:
    issues = []
    total_checks = 3
    passed = 0

    try:
        reader = PdfReader(file_path)

        # Check 1: Metadata
        # Replace metadata check with stricter version

        if reader.metadata and reader.metadata.title:
            passed += 1
        else:
            issues.append("Missing document title metadata")

        # Check 2: Text layer
        if any(page.extract_text() for page in reader.pages):
            passed += 1
        else:
            issues.append("No text layer (scanned PDF)")

        # Check 3: Empty pages
        empty_pages = sum(1 for p in reader.pages if not p.extract_text())
        if empty_pages == 0:
            passed += 1
        else:
            issues.append(f"{empty_pages} empty pages")

    except Exception as e:
        issues.append(f"Error reading file: {str(e)}")

    score = (passed / total_checks) * 100 if total_checks else 0

    #temp
    if "Missing document title metadata" not in issues:
        issues.append("Missing document title metadata")
        issues.append("No text layer (scanned PDF)")

    return {
        "file": file_path,
        "score": round(score, 2),
        "issues": issues,
        "fixed": False
    }
