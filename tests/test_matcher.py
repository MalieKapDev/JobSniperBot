import pytest
import sqlite3
from utils.matcher import get_match_score, get_job_summary
from database.database import insert_job
from scraper.weworkremotely import extract_job_details

# Mock HTML content simulating a scraped job posting
mock_html_job_data = """
<div class="job-posting">
    <h1>Front-End Developer</h1>
    <div class="listing-container">
        <p>We are looking for a Front-End Developer with experience in React and JavaScript. 
        You will build UI components, collaborate with designers, and write clean code.</p>
    </div>
</div>
"""

def test_get_match_score_returns_float():
    """Test that score is float and in range"""
    job_description = "We are looking for a passionate Front-End Developer with experience in React and JavaScript."
    score = get_match_score(job_description)
    
    assert isinstance(score, float), "Match score should be a float"
    assert 0.0 <= score <= 1.0, "Match score should be between 0.0 and 100.0"

def test_get_match_score_empty_prompt():
    score = get_match_score("")
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

def test_get_match_score_non_english_prompt():
    prompt = "El candidato ideal tiene experiencia con React y JavaScript."
    score = get_match_score(prompt)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

def test_get_match_score_long_prompt():
    prompt = "React " * 500  # Very long description
    score = get_match_score(prompt)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

def test_get_job_summary_returns_summary():
    job_desc = (
        "We are looking for a Front-End Developer with experience in React and JavaScript. "
        "Responsibilities include building UI components, collaborating with designers, and writing clean code."
    )
    summary = get_job_summary(job_desc)

    assert summary is not None, "get_job_summary returned None"
    assert isinstance(summary, str), "Summary should be a string"
    assert 10 <= len(summary) <= 300, f"Summary length is off: {len(summary)}"
    assert any(word in summary for word in ["React", "JavaScript", "Developer"]), "Key job terms missing"

def test_extract_job_details_summary():
    job_description = (
        "We are looking for a Junior Frontend Developer to join our growing team. "
        "You will assist in developing and maintaining user interfaces. "
        "This is a remote-first role with growth potential."
    )
    expected = (
        "We are looking for a Junior Frontend Developer to join our growing team. "
        "You will assist in developing and maintaining user interfaces."
    )
    summary = get_job_summary(job_description)
    assert summary == expected, f"Expected: {expected}\nGot: {summary}"