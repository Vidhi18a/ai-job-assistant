def format_percent(score: float) -> str:
    return f"{round(score * 100)}%"


def match_strength(score: float) -> str:
    if score >= 0.5:
        return "Strong match"
    if score >= 0.2:
        return "Moderate match"
    return "Low match"
