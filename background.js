// background.js

// 每天觸發一次同步
chrome.runtime.onInstalled.addListener(() => {
    chrome.alarms.create("dailySync", {
      when: Date.now(),
      periodInMinutes: 60 * 24 // 每24小時
    });
  });
  
  chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === "dailySync") {
      fetch("http://localhost:8080/api/jobs")
        .then((res) => res.json())
        .then((jobs) => {
          const map = {};
          for (const job of jobs) {
            map[job.job_id] = job;
          }
          localStorage.setItem("jobMap", JSON.stringify(map));
        })
        .catch((err) => console.error("同步錯誤", err));
    }
  });
  