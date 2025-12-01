# 模組 05：AI 驅動的 Log 分析實作（Mobile × Network × AI Inference） 
最佳化 / 維護 :「AI 協助觀測與事件分析」延伸實作。

---
## 單元目標
1. 從「只會 grep + 目視」進化到「用 Python 做基本結構化分析」  
2. 理解如何用 **AI 來設計 log schema、寫 parser、產出 SLO/SLA 指標**  
3. 透過 AI 自動生成：
   - 結構化 JSON/CSV
   - 指標統計（例如：模型延遲、錯誤率、用戶行為）
   - 事件故事線（incident timeline）
---

## 課程分段流程

### Part A：先示範傳統作法（grep / Python 手寫 parser）

- 說明 log 內容包含：
  - MobileApp 事件（alice / bob / carol）
  - NetService 網路事件（http_200 / 4xx / 5xx / wifi_disconnect）
  - AIInference AI 模型事件（asr / llm / recommend / vision）
- 使用 Shell：`grep`, `awk` 粗略篩選：
  - 找出所有 `ERROR` 行
  - 找出 `AIInference` 的 `latency_ms`
  - 找出 `MobileApp` 的 `login_failed`
- 使用 `mobile_log_basic_manual.py`：
  - 單純逐行 split
  - 把 severity（INFO/WARN/ERROR）、component、message 印出
  - 還沒有正式的 schema / class

重點：先讓學員看到 **手寫版的繁瑣、脆弱**。

---
### Part B：用 AI 幫忙設計「結構化 parser」

- 在 VSCode 打開 `mobile_log_basic_manual.py`  
- 將程式與 log 範例一起貼到 ChatGPT / OpenWebUI  
- 使用 Prompt：`Prompts/log_structured_parser.md`  

請 AI 幫忙：

1. 根據 log 格式設計資料結構，如：
   - `LogEntry` dataclass（timestamp / level / source / kv fields）
2. 撰寫 robust 的 parser：
   - 能處理 `key=value` pairs
   - 沒有 key=value 的段落，也要妥善放進 `message`
3. 讀檔後輸出 JSON 列表或寫入 CSV

把 AI 產生的版本貼回 `mobile_log_basic_ai.py`，在 VSCode 執行，確認能正確 parse。

---
### Part C：用 AI 生成「指標分析程式」

- 在 VSCode 打開 `mobile_log_metrics_manual.py`  
- 手寫版只會做非常簡單的統計，例如：
  - 計算總共幾筆 ERROR / WARN
  - 計算 asr-small-v1 的平均 latency
- 然後用 Prompt：`Prompts/log_metrics_and_slo.md`  
  要求 AI：

1. 從結構化結果中算出：
   - 各模型 latency 平均值 / P95
   - MobileApp login 成功 / 失敗率（alice / bob / carol）
   - NetService HTTP status 分佈（2xx / 4xx / 5xx）
   - 重大事件：例如 GPU OOM、wifi_disconnected、http_504
2. 把結果整理成：
   - 終端機文字報表
   - 可以導出 CSV / JSON 的格式（方便之後丟到 Grafana / BI）

把 AI 結果貼回 `mobile_log_metrics_ai.py`，執行給學員看。

---

### Part D：用 AI 寫「事故故事線 & 報告摘要」

- 訓練學員如何用 AI 生成 incident report：
  - 從解析後的 JSON（或原始 log 範例）中
  - 使用 `Prompts/log_incident_storytelling.md`
- 讓 AI 自動寫出：
  - 時間線（timeline）
  - 原因推測（例如：高載 → GPU OOM → batch size reduce → 恢復）
  - 對 Product / SRE 該看什麼指標的建議

---

## VSCode / AI 工具切換說明

- VSCode：
  - 負責撰寫 / 執行 `mobile_log_basic_manual.py`、`mobile_log_metrics_manual.py`
  - 負責貼回 AI 生成的程式碼並執行測試
- ChatGPT / OpenWebUI：
  - 協助設計 data model / parser / 指標
  - 協助補完效能最佳化與錯誤處理
  - 協助撰寫報表文字與 incident 故事線

---