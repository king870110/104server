# company_list.py
import requests
from bs4 import BeautifulSoup

def get_company_list():
    companies = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, 3):  # 你可以換成更大的範圍
        url = f"https://www.104.com.tw/company/search/?jobsource=index_cmp_3&sw=2&page={page}"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for tag in soup.select(".company-item-info a"):
            name = tag.text.strip()
            href = tag["href"]
            if name and href:
                companies.append({"name": name, "url": f"https:{href}"})
    return companies