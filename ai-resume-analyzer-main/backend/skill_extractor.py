# backend/skill_extractor.py

SKILL_CATEGORIES = {
    "ai": [
        "python", "machine learning", "deep learning", "nlp",
        "tensorflow", "pytorch", "scikit-learn", "neural networks"
    ],
    "web": [
        "html", "css", "javascript", "react", "node", "express",
        "rest api", "typescript", "next.js"
    ],
    "cloud": [
        "aws", "azure", "gcp", "docker", "kubernetes", "lambda",
        "cloud functions", "ec2", "s3"
    ],
    "data": [
        "pandas", "numpy", "sql", "matplotlib", "power bi",
        "excel", "data analysis", "data visualization"
    ]
}

def extract_skills(resume_text: str) -> dict:
    """
    Returns dict: {category: [skills_found]}
    """
    found = {}
    for category, skills in SKILL_CATEGORIES.items():
        hits = [s for s in skills if s in resume_text]
        if hits:
            found[category] = hits
        else:
            found[category] = []
    return found

def count_total_skills(skills_dict: dict) -> int:
    return sum(len(v) for v in skills_dict.values())
