import httpx
import re
import requests
import asyncio
from pathlib import Path
from typing import List
from nonebot.adapters.onebot.v11 import (
    Bot, Message, MessageEvent, MessageSegment, GroupMessageEvent, unescape, PokeNotifyEvent)
# from .depends import *

url = 'https://shindanmaker.com/'

dir_path = Path(__file__).parent
current_path = str(dir_path.absolute()) + "/"
TEXT_TOO_LONG = "文字太长了哦，改短点再试吧~"
NAME_TOO_LONG = "名字太长了哦，改短点再试吧~"
REQUIRE_NAME = "找不到名字，加上名字再试吧~"
REQUIRE_ARG = "该表情至少需要一个参数"

# 获取token和cookie


async def huoqu():
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
    }
    session = requests.get('https://shindanmaker.com/587874',
                           headers=header, timeout=9)
    # 获取token
    token = re.compile(
        r'<input type="hidden" name="_token" value="(.*?)">\s+<div>\s+<input id="shindanInput"').findall(session.text)[0]
    a = str(session.cookies)
    x = re.compile(r'XSRF-TOKEN=(.*?) for .shindanmaker.com').findall(a)[0]
    y = re.compile(r'_session=(.*?) for .shindanmaker.com').findall(a)[0]
    cookie = '_session=' + y + ';' + 'name=' + x
    # 写入token
    filename = current_path + 'token.txt'
    COOKIE = current_path + "COOKIE.txt"
    with open(filename, 'w') as file_object:
        file_object.write(token)
        file_object.close()
    # 写入cookie
    with open(COOKIE, 'w') as u:
        u.write(cookie)
        u.close()


# 异世界转生
async def yishijie(id, net):
    tr = open(current_path + "token.txt", 'r')
    fr = open(current_path + "COOKIE.txt", 'r')

    cookie = fr.read()
    # print(cookie)
    token = tr.read()
    # print(token)
    tr.close()
    fr.close()
    params = ({
        '_token': token,
        'shindanName': id,
        'hiddenName': '名無しのY'
    })
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
    }
    urls = url + net
    r = requests.post(urls, headers=header, params=params, timeout=9)
    e = str(re.compile(
        r'<span class="shindanResult_name">(.*?)</span>\s+</span>\s+</span>').findall(r.text)[0])
    x = re.sub(r'<br />', "\n", e)
    y = re.sub(r"</span>|amp;", "", x)
    return y


# 今天是什么少女
async def jintian(id):  #
    tr = open(current_path + "token.txt", 'r')
    fr = open(current_path + "COOKIE.txt", 'r')
    cookie = fr.read()
    token = tr.read()
    tr.close()
    fr.close()
    params = ({
        '_token': token,
        'shindanName': id,
        'hiddenName': '名無しのY'
    })
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
    }
    urls = url + "162207"
    r = requests.post(urls, headers=header, params=params)
    e = str(re.compile(
        r'textarea" id="copy-textarea-140" rows="5">(.*?)&#10;#shindanmaker&#10;').findall(r.text)[0])
    return e


# 卖萌
async def maimeng(id):
    tr = open(current_path + "token.txt", 'r')
    fr = open(current_path + "COOKIE.txt", 'r')
    cookie = fr.read()
    token = tr.read()
    tr.close()
    fr.close()
    params = ({
        '_token': token,
        'shindanName': id,
        'hiddenName': '名無しのY'
    })
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
    }
    urls = url + "360578"
    r = httpx.post(urls, headers=header, params=params)
    e = str(re.compile(
        r'id="copy-textarea-140" rows="5">(.*?)&#10;#shindanmaker&ensp;').findall(r.text)[0])
    x = re.sub(r'&ensp;', " ", e)
    return x


# 抽老婆
async def laopo(id):
    tr = open(current_path + "token.txt", 'r')
    fr = open(current_path + "COOKIE.txt", 'r')
    cookie = fr.read()
    token = tr.read()
    tr.close()
    fr.close()
    params = ({
        '_token': token,
        'shindanName': id,
        'hiddenName': '名無しのY'
    })
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'
    }
    urls = url + "1075116"
    r = httpx.post(urls, headers=header, params=params)
    text = str(re.compile(
        r'" id="copy-textarea-140" rows="5">(.*?)、https').findall(r.text)[0])
    img = str(re.compile(
        r'、https://shindanmaker.com/1075116/pic/(.*?)_wct『').findall(r.text)[0])
    lur = "https://d22xqp4igu9v8d.cloudfront.net/s/1075116/" + img + '.jpg'
    lao = "『" + \
        str(re.compile(
            r'_wct『(.*?)&#10;#shindanmaker&ensp').findall(r.text)[0])
    return text, lur, lao


# 获取绘画的结果
async def get_img(access_token, taskId):
    url = "https://wenxin.baidu.com/younger/portal/api/rest/1.0/ernievilg/v1/getImg?from=baicai"
    payload = {
        'access_token': access_token,
        'taskId': taskId
    }  # 请求参数，taskId是绘画的任务id
    async with httpx.AsyncClient(verify=False, timeout=None) as client:
        resp = await client.post(url, data=payload)
        data = resp.json()
        print(data)
        if data['code'] == 0:  # 请求成功
            if data['data']['status'] == 1:  # status为1，表明绘画完成
                return [MessageSegment.image(file=imgurl["image"]) for imgurl in data['data']['imgUrls']]
            else:
                # 5s后再次请求
                await asyncio.sleep(5)
                return await get_img(access_token, taskId)

        print(f'绘画任务失败,返回msg: {data["msg"]}')  # 请求失败的消息提示
        return None


async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    name: str,
    uin: str,
    msgs: List[Message],
) -> dict:
    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )