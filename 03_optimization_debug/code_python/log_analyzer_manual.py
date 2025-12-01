"""
最初版本：僅能逐行讀 log，無任何分析功能

* 讓 AI 重構成 log 分析器（分類、統計、告警）
"""

LOG_FILE = "./datasets/example_mobile_ai.log"

def main():
    print(f"[INFO] reading {LOG_FILE}")
    try:
        f = open(LOG_FILE, "r", encoding="utf-8")
    except:
        print(
            f"[ERROR] cannot open log file: {LOG_FILE}. Please check the path."
        )
    for line in f:
        print(line.strip())

    f.close()
    print("[INFO] done.")

if __name__ == "__main__":
    main()