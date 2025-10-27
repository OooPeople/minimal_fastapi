def normalize_name(name: str) -> str:
    """
    去前後空白、把連續空白壓成 1 格，並保持大小寫不變。
    純函數：不依賴外部狀態，方便測試與重用。
    """
    if not isinstance(name, str):
        raise TypeError("name must be str")
    # 去頭尾空白
    s = name.strip()
    # 把連續空白壓成一格
    parts = s.split()
    return " ".join(parts)
