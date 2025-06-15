# 104 上市櫃職缺爬蟲與同步系統技術文件

## 目的

建立一個自動化 Python 系統，用於:

1. 爭取 104 人力銀行上市正潔公司的職置上架資料
2. 每天限制一次與 Supabase 雲端同步

## 架構規劃

104-sync/
├── sync104_jobs.py ← 主程式，每天跑一次
├── last_sync.json ← 記錄上次同步日期
├── supabase_client.py ← 初始化連線
├── crawler.py ← 負責爬 104 職缺
├── jobs.json ← 暫存職缺資料（可選）
└── requirements.txt

## 系統機制

```
+--------------------+         +-----------------+        +----------------------+
|   crawler.py       |  --->   | jobs.json       |  --->  | supabase_client.py   |
| (爭取職置)       |         | (資料列表) |        | (上傳到 DB)        |
+--------------------+         +-----------------+        +----------------------+
         |
         v
+------------------+
| sync104_jobs.py  | <----> last_sync.json (紀錄是否同步)
+------------------+
```

## 文件說明

### `sync104_jobs.py`

- 主程式
- 根據 `last_sync.json` 判斷是否今天已經同步
- 執行下列流程:

  - 呼叫 `crawler.py` 爭取職置資料
  - 存成 `jobs.json`
  - 讀取 `jobs.json` 中資料帶入 Supabase
  - 更新 `last_sync.json`

### `crawler.py`

- 用 requests + BeautifulSoup 爭取 104 職置列表
- 模擬查詢: 所有上市正潔公司關鍵字 + 加上某些篩選條件
- 抓取資料:

  - jobId
  - title
  - company
  - postedDate
  - url

- 用 list 儲存並写入 `jobs.json`

### `supabase_client.py`

- 使用 `supabase-py` 連線
- 匯出 `upload_jobs(job_list)` function
- 將 job list 定題化後一組一組寫入 Supabase
- 表格: `job_posts`

#### Supabase 表格設計

| 欄位        | 類型      | 說明     |
| ----------- | --------- | -------- |
| job_id      | text (PK) | 職置 ID  |
| company     | text      | 公司名稱 |
| title       | text      | 職置標題 |
| posted_date | date      | 上架日期 |
| url         | text      | 104 URL  |
| updated_at  | timestamp | 自動生成 |

### `last_sync.json`

```json
{
	"lastSync": "2025-06-14"
}
```

- 用來判斷今天是否已同步
- 如果不是今天，則執行爭取 + 更新

## 執行方式

```bash
python sync104_jobs.py
```

- 推薦配合 cronjob 或 GitHub Actions 每日執行

## 未來延伸

- 加入 GUI (Tkinter / Streamlit)
- 配合 Chrome Extension 顯示最新職置日期
- 加入公司排名、職置排行榜

---

如需給用戶使用，可配合 EXE 打包、日記、錯誤影像日誌等功能。
