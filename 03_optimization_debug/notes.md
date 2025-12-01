# 模組 03：程式碼最佳化、Debug、維護與版本管理

課程時間：4 小時  
結構：4 個單元  

整體主軸：  
- 使用 AI 輔助找效能瓶頸  
- 使用 AI 進行 Debug（錯誤追蹤、例外處理補強）  
- 使用 AI 做模組化重構  
- 使用 AI 協助撰寫維護文件與 Git commit message  

---

## 單元 9 效能瓶頸分析：從 O(n²) 到 O(n)

### 目標
- 認識 Python 性能問題的常見原因  
- 用 AI 找出慢程式的瓶頸（loop / IO / 資料結構）  
- 用 AI 協助最佳化（list comprehension、generator、dict 快速查詢）

### 使用檔案
- `code_Python/slow_script_manual.py`
- `Prompts/refactor_performance.md`
- `code_Python/slow_script_ai.py`

### 步驟
1. VSCode 執行 slow_script_manual.py  
2. 學員體驗「等超久」  
3. 將程式碼貼給 ChatGPT/OpenWebUI  
4. AI 找瓶頸 → 重構版本貼入 slow_script_ai.py  
5. 展示不同版本執行時間差異

---

## 單元 10 AI Debug：自動找錯、重建錯誤處理機制

### 目標
- 讓 AI 協助依 log trace 出錯位置  
- 自動補上 try/except  
- 自動產生錯誤訊息分類器（方便維運）

### 使用檔案
- `log_analyzer_manual.py`
- `datasets/example.log`
- `Prompts/debug_assistant.md`
- `log_analyzer_ai.py`

### 步驟
1. 用手寫版本分析 log（功能不完整、錯誤一大堆）  
2. 丟給 AI → 要求：
   - 錯誤分類  
   - 統計 ERROR/WARN/INFO  
   - 提供「建議改善方案」  
3. VSCode 執行 AI 版本分析 log  

---

## 單元 11 AI 輔助程式碼重構 × 模組化 × 文件化

###  學到：
- 模組化（拆 function / class）
- 建立共用工具（utils / helpers）
- 自動產生技術文件（docstring / README / 設計說明）

### 使用檔案
- 第一次上課內容 任意 AI 程式（教師示範）
- 搭配 prompt：`refactor_performance.md`

流程：  
- 將 AI 寫的 batch_rename / cleanup 維運腳本再請 AI 重構  
- 產生 utils.py  
- 產生 docstring + README.md 自動化說明  

---

## 單元 12 AI 輔助 Git 版本管理：commit 訊息 × 變更說明書

### 目標
- 使用 AI 自動產生 Git commit message  
- 使用 AI 自動產生 CHANGELOG  
- 使用 AI 自動產生維護手冊（Release Notes）

### 使用檔案
- `git_commit_ai_example.txt`
- `Prompts/git_commit_message.md`

流程：  
1. 產生一個錯誤訊息很糟糕的 commit message  
2. 丟給 AI：→ 幫我轉成 conventional commit  
3. AI 自動產出三份：
   - commit message  
   - CHANGELOG snippet  
   - Release note  

---