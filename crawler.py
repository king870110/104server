from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime


def crawl_jobs(zone="16", indcat="1,2", max_pages=150):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )

    options.add_argument("--headless")  # 啟動無頭模式，不顯示瀏覽器

    driver = webdriver.Chrome(options=options)
    jobs = []

    for page in range(1, max_pages + 1):
        url = f"https://www.104.com.tw/jobs/search/?page={page}&searchJobs=1&jobsource=joblist_search&zone={zone}&indcat={indcat}"
        driver.get(url)

        print(f"第 {page} 頁，URL: {url}")

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".vue-recycle-scroller__item-view")
                )
            )
        except:
            print(f"第 {page} 頁職缺卡片等待逾時，停止")
            break

        # cards = driver.find_elements(By.CSS_SELECTOR, "article.b-block--top-bord")
        cards = driver.find_elements(
            By.CSS_SELECTOR,
            "div.vue-recycle-scroller__item-view.recycle-scroller--item",
        )

        if not cards:
            print(f"第 {page} 頁沒有職缺，停止。")
            break

        last_seen_at = datetime.now().isoformat()

        for card in cards:
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, ".info-job__text")
                company_elem = card.find_element(By.CSS_SELECTOR, ".info-company__text")
                location_elem = card.find_element(By.CSS_SELECTOR, ".info-tags__text a")

                date_elem = card.find_element(
                    By.CSS_SELECTOR, ".date-container"
                ).text.strip()

                job = {
                    "job_id": title_elem.get_attribute("href")
                    .split("/")[-1]
                    .split("?")[0],
                    "job_title": title_elem.text.strip(),
                    "company": company_elem.text.strip(),
                    "url": title_elem.get_attribute("href"),
                    "posted_at": parse_date(date_elem),
                    "location": location_elem.text.strip(),
                    "last_seen_at": last_seen_at,
                }
                jobs.append(job)
            except Exception as e:
                print("擷取職缺時出錯:", e)
                continue

        print(f"第 {page} 頁抓取到 {len(cards)} 筆職缺")
        time.sleep(2)  # 頁間休息

    driver.quit()
    print(f"總共抓取 {len(jobs)} 筆職缺")
    return jobs


def parse_date(date_str):
    year = datetime.now().year
    # print(date_str)
    try:
        # 假設 date_str 是 "6/15"
        if "/" in date_str and len(date_str.split("/")) == 2:
            dt = datetime.strptime(f"{year}/{date_str}", "%Y/%m/%d")
            return dt.isoformat()
        # 如果已經有完整年月日格式，自己再加判斷
        elif "/" in date_str and len(date_str.split("/")) == 3:
            dt = datetime.strptime(date_str, "%Y/%m/%d")
            return dt.isoformat()
        else:
            print(f"日期格式不支援: {date_str}")
            return None
    except Exception as e:
        print(f"日期解析錯誤: {date_str} -> {e}")
        return None
