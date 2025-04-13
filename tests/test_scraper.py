import sqlite3
import pytest
from database.database import create_tables, insert_job, get_jobs_by_filter, log_error
from scraper.weworkremotely import extract_job_details
from utils.gpt_matcher import get_match_score

@pytest.fixture(scope="function")
def setup_database():
    """Setup and teardown for the database."""
    create_tables()
    yield
    try:
        conn = sqlite3.connect("jobsniper.db")
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS jobs")
        c.execute("DROP TABLE IF EXISTS logs")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error during cleanup: {e}")

@pytest.fixture(scope="function")
def db_connection():
    """Setup and teardown for the database connection."""
    conn = sqlite3.connect("jobsniper.db")
    yield conn
    conn.close()

def test_insert_job(db_connection):
    """Test inserting a job."""
    job_details = (
        "Frontend Developer",  # job_title
        "Company XYZ",         # company
        "Develop user interfaces",  # description
        "Remote",              # location
        "Full-time",           # type
        "Not disclosed",       # salary
        "http://job.link",     # url
        "Indeed",              # source
        "2025-04-11",          # date_posted
        "2025-04-11",          # date_scraped
        "new",                 # status
        95.0,                  # match_score
        "Front-End Developer with React experience."  # summary
    )

    insert_job(job_details)
    
    c = db_connection.cursor()
    c.execute("SELECT * FROM jobs WHERE url = ?", (job_details[6],))
    job = c.fetchone()
    
    assert job is not None, "Job should have been inserted"
    assert job[1] == job_details[0], "Job title mismatch"
    c.close()

def test_extract_job_details_summary():
    """Test job summary extraction from job details."""
    job_description = "We are looking for a Senior React Developer to join our growing team. You will be responsible for developing and maintaining user-facing features."
    summary = extract_job_details(job_description)
    assert summary == "Senior React Developer responsible for user-facing features.", "Summary extraction mismatch"

def test_log_error(setup_database):
    """Test logging an error."""
    log_error("ERROR", "Test error message", "Test details")
    
    conn = sqlite3.connect("jobsniper.db")
    c = conn.cursor()
    c.execute("SELECT * FROM logs WHERE message = ?", ("Test error message",))
    log = c.fetchone()
    conn.close()

    assert log is not None, "Log entry should exist"
    assert log[3] == "Test error message", "Log message mismatch"
    assert log[4] == "Test details", "Log details mismatch"

def test_job_with_low_match_score(setup_database):
    """Test job insertion with a low match score."""
    job_details = (
        "Junior Frontend Developer",  # job_title
        "Company XYZ",                # company
        "Basic frontend tasks",       # description
        "USA",                        # location
        "Remote",                     # type
        "$40k",                       # salary
        "http://lowmatch.job",        # url
        "Indeed",                     # source
        "2025-04-11",                 # date_posted
        "2025-04-11",                 # date_scraped
        "new",                        # status
        50.0,                         # match_score
        "Basic Front-End Developer position."  # summary
    )
    
    insert_job(job_details)

    conn = sqlite3.connect("jobsniper.db")
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE url = ?", (job_details[6],))
    job = c.fetchone()
    conn.close()

    assert job is None, "Job with low match score should not be inserted"