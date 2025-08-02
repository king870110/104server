import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = "jobs"
# print("SUPABASE_URL =", SUPABASE_URL)
# print("SUPABASE_KEY =", SUPABASE_KEY)


headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",  # 告訴 supabase 做 upsert
}


# def upsert_jobs(jobs):
#     url = f"{SUPABASE_URL}/rest/v1/{TABLE}"

#     for job in jobs:
#         job_data = job.copy()

#         if "job_id" not in job_data:
#             print("Error: job data missing 'job_id' key, skip")
#             continue

#         # 如果資料已有 post_at，不要送入 post_at 讓它不被覆寫
#         if "posted_at" not in job_data or not job_data["posted_at"]:
#             job_data["posted_at"] = datetime.now().isoformat()

#         params = {"on_conflict": "job_id"}

#         try:
#             res = requests.post(url, headers=headers, json=job_data, params=params)
#             if res.status_code in (200, 201):
#                 print(f"Upsert job {job_data['job_id']} 成功")
#             else:
#                 print(
#                     f"Upsert job {job_data['job_id']} 失敗: {res.status_code} {res.text}"
#                 )
#         except Exception as e:
#             print(f"Exception when upserting job {job_data['job_id']}: {e}")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upsert_jobs(jobs):
    for job in jobs:
        job_data = job.copy()

        if "job_id" not in job_data:
            print("❌ 缺少 job_id，略過")
            continue

        if not job_data.get("posted_at"):
            job_data["posted_at"] = datetime.now().isoformat()

        try:
            res = supabase.table(TABLE).upsert(job_data, on_conflict="job_id").execute()

            # github
            # if res.status_code in (200, 201):
            #     print(f"✅ Upsert job {job_data['job_id']} 成功")
            # else:
            #     print(
            #         f"⚠️ Upsert job {job_data['job_id']} 失敗: {res.status_code} {res.data}"
            #     )
            try:
                res = (
                    supabase.table(TABLE)
                    .upsert(job_data, on_conflict="job_id")
                    .execute()
                )
                if res.data:
                    print(f"✅ Upsert job {job_data['job_id']} 成功")
                else:
                    print(
                        f"⚠️ Upsert job {job_data['job_id']} 可能失敗，無回傳資料: {res}"
                    )
            except Exception as e:
                print(f"🔥 Exception upserting job {job_data['job_id']}: {e}")

            # local
            # if getattr(res, "error", None):  # v2.x 檢查 error
            #     print(f"⚠️ Upsert job {job_data['job_id']} 失敗: {res.error}")
            # else:
            #     print(f"✅ Upsert job {job_data['job_id']} 成功: {res.data}")

        except Exception as e:
            print(f"🔥 Exception upserting job {job_data['job_id']}: {e}")


def export_json():

    import json

    today = datetime.now()
    start_time = (today - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    print("開始時間:", start_time)

    batch_size = 1000
    start = 0
    all_data = []

    while True:
        response = (
            supabase.table("jobs")
            .select("*")
            .gte("created_at", start_time)
            .range(start, start + batch_size - 1)
            .execute()
        )

        if hasattr(response, "error") and response.error:
            print("查詢錯誤:", response.error)
            break

        batch = response.data
        if not batch:
            break

        all_data.extend(batch)
        print(f"已抓取 {len(all_data)} 筆資料")

        if len(batch) < batch_size:
            # 最後一批，結束迴圈
            break

        start += batch_size

    if all_data:
        os.makedirs("public", exist_ok=True)
        with open("public/jobs.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功匯出 {len(all_data)} 筆資料到 public/jobs.json")
    else:
        print("沒有資料可匯出")
