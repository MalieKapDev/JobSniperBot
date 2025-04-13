import pytest
from utils.gpt_matcher import get_match_score, get_job_summary
from database.database import create_tables, insert_job, get_jobs_by_filter, log_error
from scraper.weworkremotely import extract_job_details

def test_get_match_score_returns_float():
    job_description = "We are looking for a passionate Front-End Developer with experience in React and JavaScript."
    score = get_match_score(job_description)
    
    assert isinstance(score, float), "Match score should be a float"
    assert 0.0 <= score <= 100.0, "Match score should be between 0.0 and 1.0"

def test_get_match_score_empty_prompt():
    prompt = ""
    score = get_match_score(prompt)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0

def test_get_match_score_non_english_prompt():
    prompt = "El candidato ideal tiene experiencia con React y JavaScript."
    score = get_match_score(prompt)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0

def test_get_match_score_long_prompt():
    prompt = "React " * 500  # simulates a very long job description
    score = get_match_score(prompt)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0

def job_description():
    return "We are looking for a Front-End Developer with experience in React and JavaScript."

def expected_summary():
    return "Front-End Developer with React and JavaScript experience."

def test_get_job_summary():
    summary = get_job_summary(job_description())
    assert summary == expected_summary()