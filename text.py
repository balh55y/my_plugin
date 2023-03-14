import re
# 定义正则表达式
pattern = r"https://i\.pximg\.net/img-original/img/\d+/\d+/\d+/\d+/\d+/\d+/"
# 测试网址
url = "https://i.pximg.net/img-original/img/2023/02/06/00/57/48/105126080_p10.jpg"
# 进行正则匹配
match = re.search(pattern, url)
if match:
    # 进行替换
    new_url = url.replace("i.pximg.net", "pixiv.balh5.workers.dev")
    # new_url = re.sub(pattern, "https://pixiv.balh5.workers.dev/img-original/img/", url)
    print(new_url)
else:
    print("网址不符合规则")