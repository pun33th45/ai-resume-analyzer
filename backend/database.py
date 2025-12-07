# backend/database.py

import sqlite3
from datetime import datetime

conn = sqlite3.connect("resume_analyzer.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    job_title TEXT,
    ats_score REAL,
    jd_match REAL,
    created_at TEXT
)
""")
conn.commit()

def save_analysis(name: str, email: str, job_title: str,
                  ats_score: float, jd_match: float):
    cur.execute("""
        INSERT INTO analyses (name, email, job_title, ats_score, jd_match, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, email, job_title, ats_score, jd_match,
          datetime.utcnow().isoformat()))
    conn.commit()

def get_recent_analyses(limit: int = 10):
    cur.execute("""
        SELECT name, email, job_title, ats_score, jd_match, created_at
        FROM analyses ORDER BY id DESC LIMIT ?
    """, (limit,))
    return cur.fetchall()
