import pytest
from unittest.mock import patch, MagicMock
from utils.emailer import send_email, send_job_match_email

def test_send_email_success():
    with patch('smtplib.SMTP') as mock_smtp:
        instance = mock_smtp.return_value.__enter__.return_value

        send_email("Test Subject", "Test Body", recipient="test@example.com")

        instance.starttls.assert_called_once()
        instance.login.assert_called_once()
        instance.sendmail.assert_called_once()

def test_send_job_match_email():
    mock_job = {
        "title": "Front-End Developer",
        "company": "Awesome Devs Inc.",
        "location": "Remote",
        "score": 88.5,
        "summary": "Looking for a React dev to build cool UIs.",
        "url": "https://example.com/job-posting"
    }

    with patch('smtplib.SMTP') as mock_smtp:
        send_job_match_email(mock_job)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.sendmail.assert_called_once()