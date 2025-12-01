# Prompt：請將單次檢查程式改寫成「可設定規則的 Alert Engine」

你是一位 SRE / 後端工程師，熟悉 log 監控與告警系統 (類似 Prometheus Alertmanager)。  
我有一支 Python 程式 `scheduled_log_alert_manual.py`，目前功能：

- 從 `alert_config.yaml` 讀取一些門檻
- 讀取 log 檔，做硬編碼的 if-else 檢查
- 一次執行完就結束（沒有排程）

【我想提升的目標】

1. 把「異常檢查邏輯」抽成一個通用的 rules engine：
   - 例如：從 YAML 讀取 alert rule list
   - 每個 rule 包含：
     - 名稱 (name)
     - 條件（例如 error_count >= 3）
     - 描述 (description)
   - 檢查後回傳 triggered rules 清單

2. 支援簡單排程：
   - 使用 `schedule` 套件
   - 依照 `alert_config.yaml.schedule`：
     - 若 mode=daily，使用 `schedule.every().day.at(...)`
     - 若 mode=interval，使用 `schedule.every(n).minutes`
   - 提供 `run_scheduler_forever()`，定期呼叫 `run_once()`。

3. 保持教學易讀性：
   - 程式切成幾個清楚的 function：
     - `load_config()`
     - `load_log_lines()`
     - `analyze_log()` 或 `parse_log_entries()`
     - `check_alerts(summary, rules_config)`
     - `build_email_body(summary, triggered_rules)`
     - `run_once()` / `run_scheduler_forever()`
   - 有 docstring 與基本錯誤處理。

【輸出格式】

1. 先用中文簡要解釋你的程式設計。
2. 再給我完整的 Python 程式碼，可以直接覆蓋 `scheduled_log_alert_ai.py` 使用。

接下來我會貼上：
- `scheduled_log_alert_manual.py`
- `alert_config.yaml`