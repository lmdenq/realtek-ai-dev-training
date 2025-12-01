# Prompt：請幫我設計結構化的 log parser（含 dataclass）

你是一位熟悉 log 觀測與資料工程的資深工程師。  
我有一份 Mobile + NetService + AIInference 的應用 log，以及一支很陽春的 parser。

【log 特徵】
- 每行格式大致如下：
  `timestamp level source key=value key=value ...`
- 一些欄位是 key=value（user_id, model, latency_ms, event, path, ...）
- 有 INFO / WARN / ERROR / DEBUG
- source 例如：MobileApp / NetService / AIInference

【我目前的程式】
- `mobile_log_basic_manual.py` 只會：
  - 用 split 切出 timestamp / level / source
  - 剩下的全部當成 message 字串

【請你幫我做到】
1. 設計一個 `LogEntry` 資料結構（可以用 Python dataclass）：
   - timestamp（字串即可）
   - level
   - source
   - fields: dict[str, str] 來放所有 key=value
   - raw_message

2. 實作一個 parser：
   - 能把 key=value 解析進 fields
   - 沒有 key=value 的部分，保留在 raw_message
   - 不要在 fields 中硬編死 field 名稱（不同 source 可有不同欄位）

3. 實作一個 `parse_file(path) -> list[LogEntry]`：
   - 讀整個檔案
   - 回傳 LogEntry 清單
   - 可選：提供一個函式把結果輸出成 JSON lines

4. 配合教學用途：
   - 程式碼要有清楚的 docstring 與註解
   - 切成適合講解的幾個 function，而不是擠在 main 裡

【輸出格式】
1. 先用中文簡要說明你設計這個資料結構與 parser 的理由。
2. 再給我完整 Python 程式碼（可以直接覆蓋 `mobile_log_basic_ai.py`）。

【附件】
- 我會先貼上 `mobile_log_basic_manual.py`
- 再貼上部分 log 範例