import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(SUPABASE_KEY)
print(SUPABASE_URL)


def fetch_jobs():
    print("[+] 正在抓取 104 職缺資料")
    url = "https://www.104.com.tw/company/search/?jobsource=index_cmp_3&sw=2&zone=16"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    # TODO: 根據實際 HTML 結構擷取資料
    jobs = []

    # ⛔ 範例假資料
    jobs.append(
        {
            "company": "鴻海科技集團",
            "job_title": "後端工程師",
            "location": "台北市內湖區",
            "position": "全職",
            "posted_date": datetime.now().isoformat(),
        }
    )

    return jobs


def upload_to_supabase(jobs):
    print(f"[+] 上傳 {len(jobs)} 筆資料至 Supabase")
    for job in jobs:
        res = requests.post(
            f"{SUPABASE_URL}/rest/v1/jobs",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
            },
            json=job,
        )
        if res.status_code != 201:
            print(f"[!] 上傳失敗: {res.text}")


def notify_telegram(message):
    print("[+] 發送 Telegram 通知")
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
    )


if __name__ == "__main__":
    jobs = fetch_jobs()
    if jobs:
        upload_to_supabase(jobs)
        notify_telegram(f"✅ 已更新 {len(jobs)} 筆職缺資料至 Supabase！")
    else:
        notify_telegram("⚠️ 今日無職缺更新。")
