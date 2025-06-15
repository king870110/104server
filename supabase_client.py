# supabase_api.py
import os
from dotenv import load_dotenv
import requests
from datetime import datetime
import supabase

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = "jobs"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


def upload_jobs(jobs):
    for job in jobs:
        supabase.table("job_posts").upsert(job, on_conflict=["job_id"]).execute()


def upsert_jobs(jobs):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}"
    for job in jobs:
        job_data = job.copy()
        job_data["created_at"] = datetime.now().isoformat()
        requests.post(url, headers=headers, json=job_data)


def close_missing_jobs(current_jobs):
    # 這邊你可以從 Supabase 撈全部 open 狀態的職缺，比對 current_jobs 不在其中的標記 closed_at
    pass
