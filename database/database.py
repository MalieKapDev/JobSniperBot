import sqlite3
from datetime import datetime

DB_NAME = "jobsniper.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    c = conn.cursor()

    # Jobs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT,
            location TEXT,
            type TEXT,
            salary TEXT,
            url TEXT UNIQUE,
            source TEXT,
            date_posted TEXT,
            date_scraped TEXT,
            status TEXT DEFAULT 'new',
            match_score REAL
        )
    """)

    # Logs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            level TEXT,
            message TEXT,
            details TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_job(job_details):
    conn = connect_db()
    c = conn.cursor()

    # Check for duplicate based on the URL
    c.execute('SELECT id FROM jobs WHERE url = ?', (job_details[6],))  # url index is 6 now
    existing_job = c.fetchone()

    if existing_job:
        print(f"Job already exists: {job_details[0]} at {job_details[1]}")
    else:
        c.execute('''
            INSERT INTO jobs (
                job_title, company, description, location, type,
                salary, url, source, date_posted, date_scraped,
                status, match_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', job_details)
        print(f"Inserted job: {job_details[0]} at {job_details[1]}")

    conn.commit()
    conn.close()

def get_jobs_by_filter(job_type=None, status="new"):
    conn = connect_db()
    c = conn.cursor()

    query = 'SELECT * FROM jobs WHERE 1=1'
    params = []

    if job_type:
        query += ' AND type = ?'
        params.append(job_type)

    if status:
        query += ' AND status = ?'
        params.append(status)

    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    return results

def get_all_jobs():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM jobs')
    results = c.fetchall()
    conn.close()
    return results

def log_error(level, message, details=""):
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        INSERT INTO logs (level, message, details)
        VALUES (?, ?, ?)
    """, (level, message, details))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created ✅")