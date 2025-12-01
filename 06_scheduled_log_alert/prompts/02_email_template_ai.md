# Prompt：請幫我把 log 分析結果轉成「好讀的告警 Email 內容」

你是一位熟悉 SRE 溝通的工程師。  
我有一個 Python dict，內容是 log 分析後的統計與觸發的規則，例如：

```python
summary = {
  "error_count": 5,
  "http_5xx": 2,
  "gpu_oom": 1,
  "wifi_disconnect": 1,
  "asr_p95": 245,
  "asr_samples": 6,
}
triggered = {
  "error_count": 5,
  "http_5xx": 2,
  "gpu_oom": 1,
  "asr_p95": 245,
}
【請你幫我做到】

生成一段適合當作 Email 內文的中文文字：

開頭簡短說明哪個系統有異常

條列關鍵指標（錯誤次數、5xx 次數、GPU OOM、latency 等）

清楚標出「本次實際觸發的告警條件」

給出 3~5 個建議後續行動

請用純文字格式（不用 HTML），方便直接塞進 send_email()。

【輸出格式】

只要回傳這段文字內容即可，不需要 Python 程式。

我會把 summary 與 triggered 的實際內容貼給你。

