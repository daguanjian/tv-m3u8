import requests
from datetime import datetime

# JSON 地址
JSON_URL = "http://141.164.53.195/live/korea-live.json"
OUTPUT = "korea.m3u8"

def run():
    try:
        r = requests.get(JSON_URL, timeout=20)
        r.encoding = "utf-8"
        data = r.json()
    except Exception as e:
        print(f"{datetime.now()} 获取 JSON 失败: {e}")
        return

    lines = ["#EXTM3U"]
    count = 0

    for item in data:
        name = item.get("name", "").strip()
        uris = item.get("uris", [])

        if not name or not uris:
            continue

        url = uris[0]

        # 按要求格式输出
        lines.append(f"#EXTINF:-1 ,{name}")
        lines.append(url)

        count += 1

    try:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"{datetime.now()} 生成频道数量: {count}")
    except Exception as e:
        print(f"{datetime.now()} 写入文件失败: {e}")

if __name__ == "__main__":
    run()
