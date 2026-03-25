def get_status(score):
    if score >= 90:
        return "compliant"
    elif score >= 60:
        return "partial"
    return "non-compliant"


def get_health_status(score):
    if score >= 80:
        return "good"
    elif score >= 60:
        return "warning"
    return "critical"