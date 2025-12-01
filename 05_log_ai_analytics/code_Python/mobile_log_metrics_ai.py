#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
mobile_log_metrics.py

計算手機 AI 服務日誌中的關鍵度量指標與 SLO 觸發情況。
用法:
    python mobile_log_metrics.py <path_to_jsonl_log> [--out-json=out.json] [--out-csv=out.csv]

日誌格式:
    每行一條 JSON，包含
        - timestamp
        - source   (MobileApp / NetService / AIInference)
        - fields   (字典)
"""

import json
import argparse
import statistics
import sys
from pathlib import Path
from collections import defaultdict, Counter

def parse_int(value, default=0):
    """嘗試把字串轉為 int，失敗則回傳 default。"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def compute_p95(values):
    """計算 95% 分位。若數量 < 2，回傳 0。"""
    if not values:
        return 0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * 0.95) - 1
    idx = max(0, idx)  # 確保索引合法
    return sorted_vals[idx]

def main(log_path, out_json=None, out_csv=None):
    # =====================
    # 初始化統計容器
    # =====================
    model_latencies = defaultdict(list)          # model -> list[latency]
    user_login_success = Counter()                # user -> count
    user_login_failure = Counter()                # user -> count
    http_status_counts = Counter()                # '2xx', '4xx', '5xx'
    anomaly_counts = Counter()                    # wifi_disconnected, tcp_reset, http_504, http_503

    # =====================
    # 讀取日誌
    # =====================
    log_file = Path(log_path)
    if not log_file.is_file():
        print(f"❌ 無法找到日誌文件: {log_path}", file=sys.stderr)
        sys.exit(1)

    with log_file.open(encoding='utf-8') as f:
        for line_no, raw in enumerate(f, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"⚠️ 第 {line_no} 行解析失敗: {e}", file=sys.stderr)
                continue

            source = entry.get('source')
            fields = entry.get('fields', {})
            # ---------- AIInference ----------
            if source == 'AIInference':
                model = fields.get('model')
                if not model:
                    continue
                # 延遲
                if 'latency_ms' in fields:
                    latency = parse_int(fields['latency_ms'])
                    model_latencies[model].append(latency)
                # 有時會直接寫入 slo 檢查
                if fields.get('event') == 'health_check' and 'avg_latency_ms' in fields:
                    # 可視作一次延遲樣本
                    latency = parse_int(fields['avg_latency_ms'])
                    model_latencies[model].append(latency)

            # ---------- MobileApp ----------
            elif source == 'MobileApp':
                user = fields.get('user_id') or fields.get('user_id') or fields.get('user')
                if not user:
                    # 某些日誌用 user_id
                    user = fields.get('user_id')
                if not user:
                    continue
                action = fields.get('action')
                if action == 'login_success':
                    user_login_success[user] += 1
                elif action == 'login_failure' or action == 'login':
                    user_login_failure[user] += 1
                elif action == 'login':
                    # 某些日誌中 login 只表示請求，成功/失敗由後續 event
                    pass

            # ---------- NetService ----------
            elif source == 'NetService':
                event = fields.get('event')
                # HTTP 狀態統計
                if event and event.startswith('http_'):
                    code = event.split('_')[1]
                    if code.isdigit():
                        code_int = int(code)
                        if 200 <= code_int < 300:
                            http_status_counts['2xx'] += 1
                        elif 400 <= code_int < 500:
                            http_status_counts['4xx'] += 1
                        elif 500 <= code_int < 600:
                            http_status_counts['5xx'] += 1
                    # 特殊 504 / 503 異常
                    if event in ('http_504', 'http_503'):
                        anomaly_counts[event] += 1

                # 其他網路異常
                if event == 'wifi_disconnected':
                    anomaly_counts['wifi_disconnected'] += 1
                if event == 'tcp_reset':
                    anomaly_counts['tcp_reset'] += 1

    # =====================
    # 結果計算
    # =====================
    # AI 模型延遲統計
    model_stats = {}
    for model, lats in model_latencies.items():
        if lats:
            avg = statistics.mean(lats)
            p95 = compute_p95(lats)
            model_stats[model] = {
                'avg_ms': round(avg, 2),
                'p95_ms': p95
            }

    # 用戶登錄統計
    user_stats = {}
    for user in set(user_login_success) | set(user_login_failure):
        user_stats[user] = {
            'login_success': user_login_success.get(user, 0),
            'login_failure': user_login_failure.get(user, 0)
        }

    # =====================
    # 輸出格式化
    # =====================
    print("\n=== AI 模型延遲統計 ===")
    for model, stats in sorted(model_stats.items()):
        print(f"- {model}: 平均延遲 = {stats['avg_ms']:.2f} ms, 95% 分位 = {stats['p95_ms']} ms")

    print("\n=== 用戶登錄成功/失敗統計 ===")
    for user, stats in sorted(user_stats.items()):
        print(f"- {user}: 成功 = {stats['login_success']}, 失敗 = {stats['login_failure']}")

    print("\n=== NetService HTTP 狀態統計 ===")
    for status, count in sorted(http_status_counts.items()):
        print(f"- {status} = {count}")

    print("\n=== 網路異常統計 ===")
    for anomaly, count in sorted(anomaly_counts.items()):
        print(f"- {anomaly} = {count}")

    # =====================
    # 可選 JSON / CSV 輸出
    # =====================
    if out_json:
        out_data = {
            'model_stats': model_stats,
            'user_stats': user_stats,
            'http_status_counts': dict(http_status_counts),
            'anomaly_counts': dict(anomaly_counts)
        }
        Path(out_json).write_text(json.dumps(out_data, ensure_ascii=False, indent=2))
        print(f"\n✅ JSON 結果已寫入: {out_json}")

    if out_csv:
        # CSV 只寫 AI 模型延遲統計（平均、P95）
        import csv
        with Path(out_csv).open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['model', 'avg_ms', 'p95_ms'])
            for model, stats in sorted(model_stats.items()):
                writer.writerow([model, f"{stats['avg_ms']:.2f}", stats['p95_ms']])
        print(f"\n✅ CSV 結果已寫入: {out_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="計算手機 AI 服務日誌中的關鍵度量指標。"
    )
    parser.add_argument('logfile', help='JSONL 日誌文件路徑')
    parser.add_argument('--out-json', help='輸出 JSON 結果文件')
    parser.add_argument('--out-csv', help='輸出 CSV 結果文件（僅 AI 延遲統計）')
    args = parser.parse_args()

    main(args.logfile, out_json=args.out_json, out_csv=args.out_csv)