import sqlite3
import pytest
from database.database import create_tables, insert_job, get_jobs_by_filter, log_error

@pytest.fixture(scope="function")
def setup_database():
    """Setup and teardown for the database."""
    # Create tables before tests run
    create_tables()
    
    # Yield to allow test functions to run
    yield
    
    # Cleanup: Drop tables after tests run
    try:
        conn = sqlite3.connect("jobsniper.db")
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS jobs")
        c.execute("DROP TABLE IF EXISTS logs")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error during cleanup: {e}")

def test_insert_job(setup_database):
    """Test inserting a job."""
    job_details = (
        "Frontend Developer",           # job_title
        "Company XYZ",                  # company
        "Develop user interfaces",      # description
        "Remote",                       # location
        "Full-time",                    # type
        "Not disclosed",                # salary
        "http://job.link",              # url
        "Indeed",                       # source
        "2025-04-11",                   # date_posted
        "2025-04-11",                   # date_scraped
        "new",                          # status
        0.95                            # match_score
)
    
    # Test insertion of a job
    insert_job(job_details)

    conn = sqlite3.connect("jobsniper.db")
    c = conn.cursor()
    c.execute("SELECT * FROM jobs WHERE url = ?", (job_details[6],))
    job = c.fetchone()
    conn.close()

    assert job is not None, "Job should have been inserted"
    assert job[1] == job_details[0], "Job title mismatch"

def test_get_jobs_by_filter(setup_database):
    """Test retrieving jobs by filter."""
    job_details = (
    "Junior Frontend Developer",  # job_title
    "Company XYZ",                # company
    "Develop user interfaces",    # description
    "USA",                        # location
    "Remote",                     # type
    "$40k",                       # salary
    "http://job.link",            # url
    "Indeed",                     # source
    "2025-04-11",                 # date_posted
    "2025-04-11",                 # date_scraped
    "new",                        # status
    0.9                           # match_score
)
    insert_job(job_details)
    
    # Test filtering by job type (e.g., "Remote")
    jobs = get_jobs_by_filter(job_type="Remote", status="new")
    assert len(jobs) > 0, "No jobs found for the filter"
    assert jobs[0][5] == "Remote", "Job type mismatch"

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