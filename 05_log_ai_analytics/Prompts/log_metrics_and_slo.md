# Prompt：請從這份 log 中萃取關鍵指標（metrics）與 SLO 觀點

你是一位專門維運「行動 App + AI 後端」的 SRE。  
我們有一份經過初步解析的結構化 log（或你也可以直接從原始 log 解析），
希望你協助我們設計「可以直接用來監控與報表的指標程式」。

【系統包含】
- MobileApp：user 行為、battery、螢幕、video 播放…
- NetService：HTTP 狀態碼、wifi / cell 網路品質、重試、504/503 事件…
- AIInference：asr-small-v1, llm-chat-v2, recommend-v1, vision-objdet-v1

【請你幫我做到】
1. 幫我設計一組實務上有用的 metrics：
   - 每個 AI model 的 latency_ms：平均值、P95
   - 每位 user (alice/bob/carol) 的 login 成功 / 失敗次數
   - NetService HTTP status：2xx / 4xx / 5xx 次數
   - 網路異常事件：wifi_disconnected、tcp_reset、http_504、http_503 的次數

2. 實作一支 Python 程式：
   - 從 `mobile_log_basic_ai.py` 的 parser 或原始 log 取得資料
   - 計算並印出上述指標，格式清楚、適合貼進報表
   - 可選：將結果輸出為 JSON / CSV（方便之後丟到 Grafana / BI）

3. 從 SLO 角度提出建議：
   - 例如：asr 模型 latency SLO 應該怎麼訂？
   - http_5xx 的比例大概多少需要告警？
   - GPU OOM、circuit_breaker 應該配哪些監控？

【輸出格式】
1. 先用中文條列說明你選的 metrics 與 SLO 想法。
2. 再給我完整 Python 程式碼（可直接存為 `mobile_log_metrics_ai.py`）。