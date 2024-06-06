def main():
    try:
        task1()
        task2()
    except Exception as e:
        print(f"An error occurred: {e}")
        # 這裡可以執行清理操作或其他必要的步驟
        # 比如記錄錯誤日誌、釋放資源等
        # 如果需要，還可以使用 `raise` 將錯誤重新拋出
        # raise


def task1():
    try:
        microtask1()
        microtask2()
    except Exception as e:
        print(f"Task1 failed: {e}")
        raise


def task2():
    try:
        # task2的實際工作
        pass
    except Exception as e:
        print(f"Task2 failed: {e}")
        raise


def microtask1():
    # 模擬一個會引發異常的任務
    raise ValueError("Microtask1 encountered an error")


def microtask2():
    # 其他子任務
    pass


if __name__ == "__main__":
    main()
