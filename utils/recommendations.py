def get_recommendation(issue):
    issue = issue.lower()

    if "alt" in issue:
        return "Add descriptive alt text to images"
    elif "contrast" in issue:
        return "Improve color contrast (WCAG)"
    elif "heading" in issue:
        return "Fix heading hierarchy (H1 → H2 → H3)"
    elif "table" in issue:
        return "Add table headers and scope"
    elif "form" in issue:
        return "Ensure all form fields have labels"
    else:
        return "Review WCAG accessibility guidelines"