"""
快程式範例：O(n) 版本
- 用 set 追蹤已見與重複數字
- 運算時間遠低於 O(n²) 版本
"""
import time

def find_duplicates_slow(numbers):
    """原始 O(n²) 版本（示範用）"""
    duplicates = []
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j and numbers[i] == numbers[j]:
                if numbers[i] not in duplicates:
                    duplicates.append(numbers[i])
    return duplicates

def find_duplicates_fast(numbers):
    """O(n) 版本（實際使用）"""
    seen = set()
    duplicates = set()
    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    return list(duplicates)

def main():
    print("[INFO] generating large list...")
    data = list(range(5000)) + list(range(2000, 7000))  # 製造重複值

    # ----------------- O(n²) 測試 -----------------
    print("[INFO] running O(n²) duplicate finder...")
    start = time.perf_counter()
    dups_slow = find_duplicates_slow(data)
    end = time.perf_counter()
    print(f"[INFO] found {len(dups_slow)} duplicates (O(n²))")
    print(f"[INFO] time used = {end - start:.4f} sec")

    # ----------------- O(n) 測試 -----------------
    print("\n[INFO] running O(n) duplicate finder...")
    start = time.perf_counter()
    dups_fast = find_duplicates_fast(data)
    end = time.perf_counter()
    print(f"[INFO] found {len(dups_fast)} duplicates (O(n))")
    print(f"[INFO] time used = {end - start:.4f} sec")

    # ----------------- 結果一致性 -----------------
    assert sorted(dups_slow) == sorted(dups_fast), "結果不一致！"

if __name__ == "__main__":
    main()
