# main.py
from company_list import get_company_list
from job_list import get_job_list_for_company
from job_detail import get_job_details
from supabase_api import upsert_jobs, close_missing_jobs
from telegram_notify import send_notification
import datetime


def main():
    all_jobs = []
    print("[+] 抓取公司列表中...")
    companies = get_company_list()

    for company in companies:
        print(f"[+] 抓取 {company['name']} 的職缺...")
        job_summaries = get_job_list_for_company(company["url"])

        for summary in job_summaries:
            details = get_job_details(summary["url"])
            if details:
                job = {
                    "job_id": summary["job_id"],
                    "company": company["name"],
                    "title": details["title"],
                    "location": details["location"],
                    "position_name": details["position"],
                    "posted_at": details["posted_at"],
                }
                all_jobs.append(job)

    print(f"[+] 上傳 {len(all_jobs)} 筆資料至 Supabase...")
    upsert_jobs(all_jobs)
    close_missing_jobs(all_jobs)
    send_notification(f"✅ 今日更新完成，共同步 {len(all_jobs)} 筆職缺。")


if __name__ == "__main__":
    main()
