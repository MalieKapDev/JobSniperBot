# JobSniperBot

A Python automation project that scrapes remote-friendly job listings from multiple job boards, stores them in a database, filters duplicates, and sends personalized job applications with tailored CVs and cover letters.

## Features (WIP)

- Multi-site job scraping
- Retries on failed requests for robust scraping
- SQLite database for tracking
- Job data stored and filtered for duplicates to ensure accuracy
- Job match score calculation to filter relevant listings
- Personalized email notifications with job summaries and match scores
- GPT-powered CV/cover letter generation
- Email summary and manual approval before applying
- Logging and error handling for traceability
- Logs stored for troubleshooting
- UI dashboard (planned)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # For Unix-based systems
.\venv\Scripts\activate   # For Windows systems
pip install -r requirements.txt
```
