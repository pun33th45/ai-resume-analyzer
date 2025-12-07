# backend/jd_matcher.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_vectorizer = TfidfVectorizer(stop_words="english")

def jd_match_score(resume_text: str, jd_text: str) -> float:
    """
    Returns similarity between resume and job description in percentage.
    """
    docs = [resume_text, jd_text]
    tfidf = _vectorizer.fit_transform(docs)
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(sim * 100, 2)
