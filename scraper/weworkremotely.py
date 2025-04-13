from utils.gpt_matcher import get_match_score, get_job_summary

from database.database import create_tables, insert_job
create_tables()

import logging
import os
import smtplib
import requests
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(filename="scraper_log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from .env file
load_dotenv()

# Access the variables
email = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email, email_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())

        logging.info("Notification email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

script_status = "success"

def extract_job_details(post):
    try:
        title_tag = post.find("h4", class_="new-listing__header__title")
        job_title = title_tag.text.strip() if title_tag else "Not Listed"

        company_tag = post.find("p", class_="new-listing__company-name")
        company_name = company_tag.text.strip() if company_tag else "Not Listed"

        description_tag = post.find("p", class_="new-listing__company-headquarters")
        job_description = description_tag.text.strip() if description_tag else "Not Listed"

        if "remote" in job_description.lower():
            job_type = "Remote"
        elif "hybrid" in job_description.lower():
            job_type = "Hybrid"
        else:
            job_type = "On-Site"

        link_tag = post.find("a", href=True)
        job_link = urljoin(url, link_tag['href']) if link_tag else "No link"

        salary_tag = post.find("span", class_="salary")
        salary = salary_tag.text.strip() if salary_tag else "Not Listed"

        date_tag = post.find("p", class_="new-listing__header__icons__date")
        date_added = date_tag.text.strip() if date_tag else "Not Listed"

        location_tag = post.find("p", class_="new-listing__company-headquarters")
        location = location_tag.text.strip() if location_tag else "Not Listed"

        return [job_title, company_name, job_type, job_description, salary, "Not Applied", job_link, location, date_added]

    except Exception as e:
        logging.error(f"Error extracting job details: {e}")
        return None

url = "https://weworkremotely.com/remote-jobs/search?term=front+end+developer"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

saved_jobs = 0

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    logging.info("Request successful.")

    soup = BeautifulSoup(response.text, "html.parser")
    job_sections = soup.find_all("section", class_="jobs")

    if job_sections:
        for section in job_sections:
            job_posts = section.find_all("li", class_=lambda x: x != "view-all")

            for post in job_posts:
                job_details = extract_job_details(post)

                if job_details:
                    try:
                        job_description = job_details[3]  # index 3 = description
                        match_score = get_match_score(job_description)
                        summary = get_job_summary(job_description)

                        if match_score >= 60.0:
                            # Prepare job tuple to match insert_job() structure
                            job_data = (
                                job_details[0],  # title
                                job_details[1],  # company
                                job_details[3],  # description
                                job_details[7],  # location
                                job_details[2],  # job_type
                                job_details[4],  # salary
                                job_details[6],  # url
                                "WeWorkRemotely",  # source
                                job_details[8],  # date_posted
                                None,            # date_scraped (optional)
                                "new",           # application_status
                                match_score,      # match score
                                summary
                            )

                            insert_job(job_data)
                            saved_jobs += 1
                            logging.info(f"✅ Added job: {job_data[0]} at {job_data[1]} (Match: {match_score}%)")
                        else:
                            logging.info(f"❌ Skipped job: {job_details[0]} at {job_details[1]} (Match: {match_score}%)")

                    except Exception as e:
                        logging.error(f"Error inserting job into database: {e}")
                        script_status = "failed"
    else:
        logging.warning("No job sections found on the page.")
        script_status = "failed"

except requests.exceptions.RequestException as e:
    logging.error(f"Request error: {e}")
    script_status = "failed"     

except requests.exceptions.RequestException as e:
    logging.error(f"Request error: {e}")
    script_status = "failed"

except Exception as e:
    logging.error(f"General error: {e}")
    script_status = "failed"

if script_status == "success":
    send_email('Job Scraping Completed Successfully',
        f'The job scraping script has completed successfully and added {saved_jobs} job(s) with a match score ≥ 60% to the SQLite database.')
else:
    send_email('Job Scraping Script Failed',
        'There was an error while running the job scraping script. Check the logs for more details.')