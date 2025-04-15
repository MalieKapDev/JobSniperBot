import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Email Structure
def send_job_match_email(job):
    body = f"""
    <h2>New Job Match Found!</h2>
    <p><strong>Title:</strong> {job['title']}</p>
    <p><strong>Company:</strong> {job['company']}</p>
    <p><strong>Location:</strong> {job['location']}</p>
    <p><strong>Match Score:</strong> {job['score']}%</p>
    <p><strong>Summary:</strong> {job['summary']}</p>
    <p><a href="{job['url']}">View Job Posting</a></p>
    """
    send_email("🎯 New Job Match Found!", body, html=True)

# Send Email
def send_email(subject, body, recipient=None, html=False):
    try:
        recipient = recipient or EMAIL_USER

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = recipient
        msg['Subject'] = subject

        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())

        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")