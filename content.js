;(function () {
	// 抓取網址中的 jobId
	const match = window.location.href.match(/job\/(\w+)/)
	if (!match) return

	const jobId = match[1]
	const jobMap = JSON.parse(localStorage.getItem("jobMap") || "{}")
	const job = jobMap[jobId]
	if (!job) return

	// 顯示上架日期
	const titleEl = document.querySelector("h1.job-title") // 假設 104 用這個 class
	if (titleEl) {
		const dateTag = document.createElement("div")
		dateTag.textContent = `📅 上架日期：${job.posted_date}`
		dateTag.style.fontSize = "14px"
		dateTag.style.marginTop = "4px"
		titleEl.appendChild(dateTag)
	}
})()
