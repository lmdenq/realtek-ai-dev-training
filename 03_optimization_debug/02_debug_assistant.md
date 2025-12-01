# Prompt：請協助 Debug 並加上完整錯誤處理與 log 分析

你是一位熟悉維運與 log 分析的 SRE / DevOps 工程師。  
我有一支程式只能逐行讀 log，沒有分析功能。

【希望你幫我做到】
1. 分析 log 格式（INFO / WARN / ERROR）
2. 實作分類器：統計各類數量
3. 若 ERROR 過多，請給出「建議措施」
4. 加入 try/except，避免檔案不存在等錯誤
5. 將結果輸出成結構化報表（JSON 或表格）

【原始程式碼如下】：
```python
(貼 log_analyzer_manual.py)
```