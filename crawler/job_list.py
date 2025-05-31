# job_list.py
import requests
from bs4 import BeautifulSoup
import re


def get_job_list_for_company(company_url):
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(company_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    for tag in soup.select("a.js-job-link"):
        title = tag.text.strip()
        href = tag["href"]
        match = re.search(r"job/(\d+)", href)
        job_id = match.group(1) if match else href
        jobs.append({"job_id": job_id, "title": title, "url": f"https:{href}"})
    return jobs
