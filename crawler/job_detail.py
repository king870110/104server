# job_detail.py
import requests
from bs4 import BeautifulSoup


def get_job_details(job_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(job_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.select_one(".job-header__title")
    location = soup.select_one(".job-header__info .job-header__info-item")
    posted_at_tag = soup.select_one(".job-header__publish-date")
    if not title:
        return None
    return {
        "title": title.text.strip() if title else "",
        "location": location.text.strip() if location else "",
        "position": title.text.strip() if title else "",
        "posted_at": posted_at_tag.text.strip() if posted_at_tag else None,
    }
