"""
這個檔案在上課時，會由 ChatGPT/OpenWebUI 根據 hello_realtek_manual.py 改寫而來。
上課前可以先故意留白或只放註解。
"""

def greet(name: str = "") -> str:
    if name == "":
        name = "Engineer"
    return f"Hello, {name} from Realtek!"

def main():
    """
    主函數，負責接收使用者輸入的名字，並呼叫 greet 函數印出問候語。
    """
    name = input("請輸入你的名字：")
    print(greet(name))

if __name__ == "__main__":
    main()