import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = "jobs"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",  # 告訴 supabase 做 upsert
}


def upsert_jobs(jobs):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}"

    for job in jobs:
        job_data = job.copy()

        if "job_id" not in job_data:
            print("Error: job data missing 'job_id' key, skip")
            continue

        # 如果資料已有 post_at，不要送入 post_at 讓它不被覆寫
        if "posted_at" not in job_data or not job_data["posted_at"]:
            job_data["posted_at"] = datetime.now().isoformat()

        params = {"on_conflict": "job_id"}

        try:
            res = requests.post(url, headers=headers, json=job_data, params=params)
            if res.status_code in (200, 201):
                print(f"Upsert job {job_data['job_id']} 成功")
            else:
                print(
                    f"Upsert job {job_data['job_id']} 失敗: {res.status_code} {res.text}"
                )
        except Exception as e:
            print(f"Exception when upserting job {job_data['job_id']}: {e}")
