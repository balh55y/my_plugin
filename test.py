import requests
import json

pid = 106232082
url = f"https://api.imjad.cn/pixiv/v2/?type=illust&id={pid}"
resp = requests.get(url)
js = json.loads(resp.text)
re_url = js["response"][0]["urls"]["original"]
print(url)