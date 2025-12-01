# Prompt：請根據新的 alert_config.yaml 更新程式碼


你是一位 Python 後端工程師。  

我們已經有一支能夠：



- 讀取 `alert_config.yaml`

- 解析 log

- 根據設定進行告警



但是當我們調整 `alert_config.yaml` 結構時，需要你幫我們同步更新程式碼。



【請你幫我做到】



1. 檢查我貼給你的最新 `alert_config.yaml`，確認欄位名稱與結構。

2. 檢查既有程式（例如 `scheduled_log_alert_ai.py`）中：

   - 讀 config 的部分

   - 使用 config 的部分（例如 alerts / schedule / email）。

3. 自動修改程式碼：

   - 確保所有欄位名稱與 config 一致

   - 若新增了新的 alert rule，請示範如何擴充 rule engine



【輸出格式】



1. 簡要說明你修改了哪些地方。

2. 給出完整更新後的 Python 程式碼。



我會貼上：

- 最新版 `alert_config.yaml`

- 目前的 `scheduled_log_alert_ai.py`

