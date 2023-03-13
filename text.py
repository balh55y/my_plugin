with open("User Illust.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()[1:-1]    # 读取文件内容并去除首尾空行
    urls = list(filter(bool, lines))       # 过滤掉空行，并转为list
print(urls)