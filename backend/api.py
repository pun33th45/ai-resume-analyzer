from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.resume_parser import extract_text_from_pdf
from backend.skill_extractor import extract_skills
from backend.scoring import calculate_ats_score, generate_suggestion
from backend.jd_matcher import jd_match_score
from backend.database import save_analysis, get_recent_analyses



app = FastAPI(title="AI Resume Analyzer")

@app.get("/")
def root():
    return {
        "message": "AI Resume Analyzer API is running successfully.",
        "docs": "/docs",
        "analyze_endpoint": "/analyze",
        "history_endpoint": "/history"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...),
    name: str = Form("Anonymous"),
    email: str = Form("unknown@example.com"),
    job_title: str = Form("Not specified")
):
    resume_bytes = await resume.read()
    jd_bytes = await jd.read()

    resume_text = extract_text_from_pdf(resume_bytes)
    jd_text = extract_text_from_pdf(jd_bytes)

    match = jd_match_score(resume_text, jd_text)
    skills = extract_skills(resume_text)
    skill_count = sum(len(v) for v in skills.values())

    ats_score = calculate_ats_score(match, skill_count)
    suggestion = generate_suggestion(match, skills)

    save_analysis(name, email, job_title, ats_score, match)

    return {
        "ats_score": ats_score,
        "jd_match": match,
        "skills_found": skills,
        "suggestion": suggestion
    }

@app.get("/history")
async def history(limit: int = 10):
    rows = get_recent_analyses(limit)
    return [
        {
            "name": r[0],
            "email": r[1],
            "job_title": r[2],
            "ats_score": r[3],
            "jd_match": r[4],
            "created_at": r[5]
        }
        for r in rows
    ]
import os

