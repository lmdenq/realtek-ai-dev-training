#!/bin/bash
# 檢查是否為主程式
if [ "$0" = "$BASH_SOURCE" ]; then
    # 主程式
    main
fi

# 定義 greet 函數
greet() {
    local name="$1"
    if [ -z "$name" ]; then
        name="Engineer"
    fi
    echo "Hello, $name from Realtek!"
}

# 定義 validate_name 函數
validate_name() {
    local name="$1"
    if ! [[ "$name" =~ ^[[:alnum:]]+$ ]]; then
        echo "Error: Name must be a string" >&2
        exit 1
    fi
    echo "$name"
}

# 主程式
main() {
    read -p "請輸入你的名字： " name
    name=$(validate_name "$name")
    greet "$name"
}

# 調用主程式
main