import requests
from datetime import datetime

JSON_URL = "http://141.164.53.195/live/korea-live.json"

OUTPUT1 = "korea.m3u8"    # DIYP 影音
OUTPUT2 = "korea2.m3u8"   # 标准 M3U（支持 php）

def extract_m3u8_only(uris):
    """仅提取 .m3u8（用于 OUTPUT1）"""
    def is_m3u8(u):
        return isinstance(u, str) and ("=sbs" in u.lower() or ".m3u8" in u.lower() or u.lower().endswith(".php"))  and "skbcdn-aws-live.cdn.wavve.com" not in u.lower() and "file-1253962976.cos" not in u.lower()

    if isinstance(uris, list):
        for u in uris:
            if is_m3u8(u):
                return u.strip()

    elif isinstance(uris, dict):
        for u in uris.values():
            if is_m3u8(u):
                return u.strip()

    elif isinstance(uris, str):
        if is_m3u8(uris):
            return uris.strip()

    return None


def extract_m3u8_or_php(uris):
    """
    提取 .m3u8 或 .php
    优先 m3u8，其次 php（用于 OUTPUT2）
    """
    urls = []

    def is_valid(u):
        return isinstance(u, str) and ("=sbs" in u.lower() or ".m3u8" in u.lower() or u.lower().endswith(".php"))  and "skbcdn-aws-live.cdn.wavve.com" not in u.lower() and "file-1253962976.cos" not in u.lower()
        

    if isinstance(uris, list):
        urls = [u.strip() for u in uris if is_valid(u)]

    elif isinstance(uris, dict):
        urls = [u.strip() for u in uris.values() if is_valid(u)]

    elif isinstance(uris, str):
        if is_valid(uris):
            urls = [uris.strip()]

    # 优先 m3u8
    for u in urls:
        if ".m3u8" in u.lower():
            return u

    # 其次 php
    if urls:
        return urls[0]

    return None


def run():
    try:
        r = requests.get(JSON_URL, timeout=20)
        r.encoding = "utf-8"
        data = r.json()
    except Exception as e:
        print(f"{datetime.now()} 获取 JSON 失败: {e}")
        return

    lines1 = ["#EXTM3U"]
    lines2 = ["#EXTM3U"]

    count1 = 0
    count2 = 0

    for item in data:
        name = item.get("name", "").strip()
        uris = item.get("uris")

        if not name or not uris:
            continue

        # OUTPUT1：只要 m3u8
        url1 = extract_m3u8_only(uris)
        if url1:
            lines1.append(f"{name},{url1}")
            count1 += 1

        # OUTPUT2：m3u8 或 php
        url2 = extract_m3u8_or_php(uris)
        if url2:
            lines2.append(f"#EXTINF:-1,{name}")
            lines2.append(url2)
            count2 += 1

    with open(OUTPUT1, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines1))

    with open(OUTPUT2, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines2))

    print(f"{datetime.now()} DIYP 频道数量: {count1}")
    print(f"{datetime.now()} 标准 M3U 频道数量: {count2}")
    print(f"{datetime.now()} 已生成文件: {OUTPUT1}, {OUTPUT2}")


if __name__ == "__main__":
    run()
