"""
scheduled_log_alert_ai.py

在課堂上，你可以：

1. 將 scheduled_log_alert_manual.py 貼給 ChatGPT / OpenWebUI
2. 使用 5_Prompt/01_alert_engine_refactor.md
3. 要求 AI：
   - 將異常檢查邏輯抽成「規則引擎」
   - 從 alert_config.yaml 讀取所有規則與門檻
   - 使用 schedule 套件依照 config 排程執行 main()

下面先留一個最小骨架，讓 AI 產生完整版本後貼上。
"""

# TODO：上課時由 AI 產生，建議包含：
# - load_config()
# - parse_log()
# - build_rules_from_config()
# - check_alerts(entries, rules)
# - run_once() / run_forever_with_schedule()