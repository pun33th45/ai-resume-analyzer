# backend/scoring.py

def calculate_ats_score(jd_match: float, skill_count: int) -> float:
    """
    Combines JD match + skills into a final ATS-style score.
    jd_match: 0–100, skill_count: number of relevant skills found
    """
    # 70% weight to JD match, 30% to skill density
    base = jd_match * 0.7
    skill_score = min(skill_count * 4, 30)  # cap at 30
    return round(base + skill_score, 2)

def generate_suggestion(jd_match: float, skills_found: dict) -> str:
    if jd_match < 40:
        return "Your resume does not match this job well. Try adding role-specific keywords and tailoring your summary."
    if jd_match < 70:
        return "Decent match. Add more achievements, measurable impact, and relevant tools mentioned in the job description."
    # high match
    return "Strong match. Consider highlighting 2–3 key projects and quantifying impact to stand out even more."
