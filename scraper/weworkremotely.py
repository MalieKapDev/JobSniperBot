import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.matcher import get_match_score, get_job_summary
from utils.emailer import send_email, send_job_match_email
from database.database import create_tables, insert_job

import logging
import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

create_tables()

# Logging
logging.basicConfig(
    filename="logs/scraper_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Config
url = "https://weworkremotely.com/remote-jobs/search?term=front+end+developer"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com"
}

def extract_job_details(post, base_url):
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
        job_link = urljoin(base_url, link_tag['href']) if link_tag else "No link"

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

# Request with retry
def fetch_page(url, retries=3, delay=3):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logging.warning(f"Attempt {i+1}/{retries} failed: {e}")
            time.sleep(delay + random.uniform(1, 3))
    return None

# Scrape logic
saved_jobs = 0
script_status = "success"

response = fetch_page(url)

if response:
    soup = BeautifulSoup(response.text, "html.parser")
    job_sections = soup.find_all("section", class_="jobs")

    if job_sections:
        for section in job_sections:
            job_posts = section.find_all("li", class_=lambda x: x != "view-all")

            for post in job_posts:
                try:
                    job_details = extract_job_details(post, url)
                    if not job_details:
                        continue

                    job_text = f"{job_details[0]} {job_details[3]}"
                    match_score = get_match_score(job_text)
                    summary = get_job_summary(job_text)

                    if match_score >= 60.0:
                        job_data = (
                            job_details[0],  # title
                            job_details[1],  # company
                            job_details[3],  # description
                            job_details[7],  # location
                            job_details[2],  # type
                            job_details[4],  # salary
                            job_details[6],  # url
                            "WeWorkRemotely",  # source
                            job_details[8],  # date_posted
                            None,             # date_scraped
                            "new",            # status
                            match_score,
                            summary
                        )

                        job_email_data = {
                            "title": job_details[0],
                            "company": job_details[1],
                            "location": job_details[7],
                            "score": round(match_score, 2),
                            "summary": summary,
                            "url": job_details[6],
                        }

                        send_job_match_email(job_email_data)
                        insert_job(job_data)
                        saved_jobs += 1
                        logging.info(f"✅ Inserted: {job_details[0]} at {job_details[1]} ({match_score:.1f}%)")

                    else:
                        logging.info(f"❌ Skipped: {job_details[0]} at {job_details[1]} ({match_score:.1f}%)")

                    # Random delay between job posts
                    time.sleep(random.uniform(1, 2.5))

                except Exception as e:
                    logging.error(f"❌ Error processing job post: {e}")
                    script_status = "failed"

    else:
        logging.warning("No job sections found.")
        script_status = "failed"
else:
    logging.error("Final failure: could not retrieve page after retries.")
    script_status = "failed"

# Final status
if script_status == "success":
    send_email(
        '✅ Job Scraping Completed',
        f'Successfully added {saved_jobs} job(s) with match score ≥ 60%.'
    )
else:
    send_email(
        '❌ Job Scraping Failed',
        'There was an error running the scraper. Please check logs.'
    )