# 每日排程 log 分析與自動 Email 告警
---

## 學習目標
1. 了解「排程 log 分析」在真實維運場景中的角色（每天固定時間做健康檢查）。
2. 會寫一支簡單的 Python 腳本：
   - 讀取 `example_mobile_ai.log`
   - 偵測多種「異常狀況」
   - 發現異常時寄出 Email 告警。
3. 學會把設定抽離成 `alert_config.yaml`：
   - 每天固定分析時間（例如 09:05）
   - 要監控的異常條件與門檻
   - Email 帳號、收件人清單等（敏感資訊不進 Git）。
4. 會用 AI 把「最出版 if-else 偵測邏輯」重構成「規則化、可調整」的 Alert Engine。

---

## 情境描述

- 每天早上 09:05，自動檢查前 5 分鐘內的服務狀況：
  - AIInference 是否發生 GPU OOM？
  - http_5xx 是否出現？
  - asr-small-v1 的 latency p95 是否超過 200ms？
  - NetService 是否有 wifi_disconnected / tcp_reset？
- 如果任一項超標，系統會自動寄一封 Email 給：
  - SRE / 維運人員
  - 產品經理（PM）
- 告警內容包含：
  - 簡短標題：[Log Alert] 瑞昱行動 AI 服務異常告警
  - 指標摘要（錯誤次數 / 5xx 次數 / 模型延遲）
  - 建議下一步要看的 log / dashboard。

---

## 教學流程建議

### Part A：說明排程與設定檔

1. 打開 `alert_config.yaml`：
   - 解釋每天固定時間 `09:05`
   - 解釋 `alerts:` 區段中各種異常條件
   - 解釋 email 設定只放帳號，不放密碼（密碼用環境變數）。
2. 說明兩種排程方式：
   - 教學中用 `schedule` 套件跑 demo（適合課堂）
   - 實務可用 cron / systemd timer（用 `4_Shell_與排程範例/cron_install_example.sh` 示範）

### Part B：最初版：一次性分析 + 寄信

1. 在 VSCode 打開 `scheduled_log_alert_manual.py`。
2. 解釋程式只做三件事：
   - 讀 log → 粗略統計異常指標（error 行數、http_5xx、GPU OOM…）
   - 若任一指標超過門檻 → 呼叫 `email_utils.send_email()`
   - 只跑一次（還沒有真正排程）。
3. 學員跟著一起執行一次，模擬「每天清晨由 cron 叫起來跑一次」。

### Part C：AI 重構成「排程 ＋ 規則化 Alert Engine」

1. 開啟 `scheduled_log_alert_ai.py` 與 `5_Prompt/01_alert_engine_refactor.md`。
2. 老師示範：
   - 把 manual 版本程式貼給 ChatGPT/OpenWebUI
   - 要求 AI：
     - 從 `alert_config.yaml` 讀取規則與門檻
     - 實作 `check_alerts(entries, rules)` 這種結構
     - 用 `schedule` 套件每 X 分鐘或每天固定時間跑一次
3. 把結果貼回 `scheduled_log_alert_ai.py`，讓學員直接執行。

### Part D：AI 協助生成告警 Email 內容

1. 開啟 `5_Prompt/02_email_template_ai.md`。
2. 示範：
   - 將分析出的 summary dict（例如：錯誤數量、latency 等）貼給 AI
   - 讓 AI 回傳一段 HTML / Markdown 風格的「告警報告」文字
3. 把這段文字當作 email body 傳給 `send_email()`，寄到自己信箱給學員看看實際效果。

---

## 本單元用到的檔案一覽

- `datasets/example_mobile_ai.log`：Mobile / Net / AIInference 綜合 log
- `06_scheduled_log_alert/3_Python 程式檔案/email_utils.py`
- `06_scheduled_log_alert/3_Python 程式檔案/scheduled_log_alert_manual.py`
- `06_scheduled_log_alert/3_Python 程式檔案/scheduled_log_alert_ai.py`
- `06_scheduled_log_alert/3_Python 程式檔案/alert_config.yaml`
- `06_scheduled_log_alert/4_Shell_與排程範例/cron_install_example.sh`
- `06_scheduled_log_alert/5_Prompt 檔案/*.md`

---