# Prompt：請根據 log 產生一份「事故故事線與摘要報告」

你是一位 SRE / 事件指揮官（incident commander）。  
我有一份系統 log，包含使用者操作、網路品質、AI 模型負載與錯誤。

【請你幫我做到】
1. 幫我整理出一條「時間線」：
   - 挑出重要事件（ERROR / WARN，或會影響體驗的 INFO）
   - 用自然語言描述發生了什麼事（例如：bob 登入失敗多次、asr GPU OOM、網路中斷又恢復…）

2. 幫我寫一段「事故摘要」：
   - 用 3~5 句話說明這 2 分鐘內系統重點狀況
   - 說明對使用者體驗的影響
   - 說明系統自我恢復機制（例如：auto_batch_size_reduce、reconnect_success、http_retry）

3. 幫我列出「後續改善建議」：
   - 可以從哪些 metrics / log 再加強？
   - 需要新增哪幾種告警規則？
   - 哪些地方適合加入自動化防護（例如 circuit breaker 調整門檻）

【輸出格式】
1. 先給一份 Markdown 格式的時間線（Timeline）
2. 再給事故摘要（Incident Summary）
3. 最後列出改善建議（Action Items）

我會提供：
- 部分或全部原始 log 內容（或解析後的 JSON）
請依我提供的內容做出合理推斷，不要隨意虛構不存在的事件。