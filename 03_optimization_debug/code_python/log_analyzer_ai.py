#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
log_analyzer.py

一個簡易的 log 分析器：
1. 讀取 log 檔，解析每行的等級 (INFO/WARN/ERROR)
2. 統計各等級數量
3. 若 ERROR 占比過高，給出建議措施
4. 所有流程都包在 try/except 裡，避免因檔案不存在等問題崩潰
5. 將結果輸出成結構化 JSON 報表，並在終端顯示簡易表格

Author:   <Your Name>
Date:     2025-11-24
"""

import json
import logging
import re
from collections import Counter
from pathlib import Path
from datetime import datetime

# ===================== 設定 ===================== #
LOG_FILE = Path("./datasets/example_mobile_ai.log")  # 需要分析的 log 檔
REPORT_FILE = Path("./report.json")       # 產生的報表
ERROR_THRESHOLD = 0.10                    # ERROR 佔比 10% 時給出建議

# ===================== Logger ===================== #
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        # 如需寫入檔案，可再加一個 FileHandler
    ]
)

# ===================== 正規表達式 ===================== #
# 例子： [2025-11-24 10:15:01] [ERROR] 失敗，無法連線
LOG_PATTERN = re.compile(
    r"""
    ^\s*                               # 行首空白
    (?P<datetime>\d{4}-\d{2}-\d{2}\s+   # 日期
    \d{2}:\d{2}:\d{2})\s+
    \[(?P<level>INFO|WARN|ERROR)\]     # 等級
    \s+(?P<message>.+)$                # 其餘訊息
    """,
    re.VERBOSE
)

def parse_line(line: str):
    """把一行 log 轉成 dict。若無法解析，level 會回傳 'UNKNOWN'。"""
    m = LOG_PATTERN.match(line)
    if m:
        return {
            "datetime": m.group("datetime"),
            "level": m.group("level"),
            "message": m.group("message").strip()
        }
    else:
        # 這裡可自行擴充其他格式的解析
        return {
            "datetime": None,
            "level": "UNKNOWN",
            "message": line.strip()
        }

def analyze_log(file_path: Path) -> dict:
    """讀檔並統計 log 等級。"""
    counts = Counter()
    parsed_lines = []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                parsed = parse_line(line)
                parsed_lines.append(parsed)
                counts[parsed["level"]] += 1

    except FileNotFoundError:
        logging.error(f"檔案不存在：{file_path}")
        raise
    except Exception as e:
        logging.exception(f"讀檔時發生錯誤：{e}")
        raise

    total = sum(counts.values())
    error_ratio = counts["ERROR"] / total if total else 0

    report = {
        "file": str(file_path),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_lines": total,
        "counts": dict(counts),
        "error_ratio": round(error_ratio, 4),
    }

    # 若 ERROR 佔比超過門檻，加入建議
    if error_ratio > ERROR_THRESHOLD:
        report["recommendations"] = [
            "檢查最近 30 分鐘內的系統日誌，確認是否有連線失敗或資源耗盡的跡象。",
            "如果是第三方 API，先確認其狀態頁面是否有異常。",
            "將 ERROR 訊息加到監控平台（如 Prometheus + Alertmanager）以即時通知。",
            "若持續高併發，考慮實行排隊或限流機制。"
        ]

    # 也可以把每行原始資料寫進 report 以備追蹤（但注意大小）
    # report["lines"] = parsed_lines

    return report

def print_table(report: dict):
    """在終端顯示簡易表格，方便快速閱讀。"""
    print("\n=== Log 統計報表 ===")
    print(f"檔案: {report['file']}")
    print(f"總行數: {report['total_lines']}")
    print(f"ERROR 占比: {report['error_ratio']*100:.2f}%")
    print("\n等級統計:")
    for level in ["INFO", "WARN", "ERROR", "UNKNOWN"]:
        print(f"  {level:6}: {report['counts'].get(level, 0)}")
    if "recommendations" in report:
        print("\n⚠️  建議措施:")
        for idx, rec in enumerate(report["recommendations"], 1):
            print(f"  {idx}. {rec}")

def main():
    logging.info(f"開始分析 log：{LOG_FILE}")

    try:
        report = analyze_log(LOG_FILE)
    except Exception:
        logging.error("分析失敗，程式結束。")
        return

    # 輸出 JSON 報表
    try:
        with REPORT_FILE.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        logging.info(f"報表已寫入：{REPORT_FILE}")
    except Exception as e:
        logging.exception(f"寫入報表失敗：{e}")
        # 仍然在終端顯示
    # 端末簡易表格
    print_table(report)

    logging.info("分析完成。")

if __name__ == "__main__":
    main()