import requests
from bs4 import BeautifulSoup
import re

def crawl_jobs():
    url = "https://www.104.com.tw/jobs/search/?ro=0&isnew=30&jobcat=2007001001&area=6001001000&order=11"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    script_data = soup.find_all("script", string=re.compile("window\.INITIAL_STATE"))
    jobs = []

    if not script_data:
        return jobs

    try:
        import json
        raw = re.search(r"window\.INITIAL_STATE=(\{.*\});", script_data[0].string)
        data = json.loads(raw.group(1))
        job_list = data["jobList"]["items"]
        for job in job_list:
            jobs.append({
                "job_id": job["jobId"],
                "title": job["jobName"],
                "company": job["custName"],
                "posted_date": job["appearDate"],
                "url": f"https://www.104.com.tw/job/{job['jobId']}"
            })
    except Exception as e:
        print("解析失敗:", e)
    
    return jobs