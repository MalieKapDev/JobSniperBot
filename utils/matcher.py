import re
from utils.config import get_clean_resume_text
from nltk.tokenize import word_tokenize

resume_text = get_clean_resume_text()

def get_match_score(job_text: str) -> float:
    """
    Calculates match score between resume and job description.
    Score is based on the number of overlapping words (excluding stopwords, lemmatized).
    """
    job_text = job_text.lower()
    job_text = re.sub(r'[^a-z\s]', '', job_text)
    job_tokens = set(word_tokenize(job_text))

    resume_tokens = set(word_tokenize(resume_text))

    overlap = resume_tokens.intersection(job_tokens)

    if not job_tokens:
        return 0.0

    score = len(overlap) / len(job_tokens)
    return round(score, 2)  # Score between 0.0 and 1.0

def get_job_summary(job_description):
    """
    Return the first two sentences of the job description as a summary.
    """
    sentences = re.split(r'\.|\n', job_description)
    summary_sentences = [s.strip() for s in sentences if s.strip()][:2]
    return '. '.join(summary_sentences) + '.' if summary_sentences else ""