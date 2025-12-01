# VSCode + Git + AI Commit 實作步驟
1. 在 VSCode 開啟專案資料夾。
2. 修改程式後，點左側「Source Control」圖示。
3. 在 CHANGES 清單中點選檔案，檢視差異（diff）。
4. 使用滑鼠右鍵或 Terminal 的 `git diff` 取得這次修改的 diff 文字。
5. 將 diff 貼到 ChatGPT / OpenWebUI。
6. 依需求選擇對應的 Prompt：
   - `basic_commit_message.md`
   - `conventional_commit.md`
   - `enterprise_commit_history.md`
7. 把 AI 產生的 commit message 貼回 VSCode 的訊息欄位。
8. 按下 Commit（必要時再 Push 到遠端 repo）。