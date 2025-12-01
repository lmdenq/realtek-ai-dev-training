#!/usr/bin/env bash
# 模擬效率很差的 shell 版本（大量 for 迴圈）
# 用來示範為何 AI 會建議不要用 shell 做這種事 XD

echo "[INFO] generating list..."
seq 1 50000 > a.txt
seq 20000 70000 > b.txt

echo "[INFO] find duplicates..."
dups=()

for i in $(cat a.txt); do
    for j in $(cat b.txt); do
        if [ "$i" -eq "$j" ]; then
            dups+=("$i")
        fi
    done
done

echo "[INFO] duplicates count: ${#dups[@]}"