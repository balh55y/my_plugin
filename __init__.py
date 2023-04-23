from ast import Try
import datetime
from pathlib import Path
import traceback
from nonebot import on_command, on_fullmatch, on_regex, on_endswith, on_notice
from nonebot.params import CommandArg, EventPlainText, RegexMatched
from nonebot.typing import T_State
from nonebot import require

require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import template_to_pic
from nonebot.matcher import Matcher
from nonebot.utils import run_sync
from nonebot.permission import SUPERUSER
import httpx
import asyncio
import hashlib
import shlex
import re
import json
import random
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
    GroupMessageEvent,
    unescape,
    PokeNotifyEvent,
)
from typing import List, Optional, Type, Tuple, Dict
from nonebot.log import logger
from PIL import Image


from .data_source import yishijie, huoqu, send_forward_msg, current_path


import os


from nonebot.adapters.onebot.v11.helpers import HandleCancellation


with open(Path(current_path) / "User Illust.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()[1:-1]  # 读取文件内容并去除首尾空行
    梦夏urls = list(filter(bool, lines))  # 过滤掉空行，并转为list

壁纸 = on_command("来张壁纸", priority=20)

拼音 = on_regex(r"(^拼音.+)|(.+拼音$)", priority=1)

github_img = on_regex(
    r"github\.com\/[a-zA-Z0-9-]{1,39}\/[a-zA-Z0-9_-]{1,100}", priority=1
)

腿子 = on_command("来张腿子", priority=20)

原神 = on_command("来张原神", priority=20)

梦夏 = on_command("来张梦夏", priority=20)

小作文 = on_command("小作文", priority=20)

send_img = on_command("send-img", priority=20)

call_api = on_command("/api", permission=SUPERUSER)


def _check(event: PokeNotifyEvent):
    return event.target_id == event.self_id


戳一戳 = on_notice(rule=_check)


def _zhiri(event: GroupMessageEvent):
    return event.group_id == 115494820 or event.user_id == 2779375323


值日表 = on_command("值日表", rule=_zhiri, priority=20)
下周值日表 = on_command("下周值日表", rule=_zhiri, priority=20)
上周值日表 = on_command("上周值日表", rule=_zhiri, priority=20)


@值日表.handle()
async def _(bot: Bot, event: GroupMessageEvent , args: Message = CommandArg()):
    # breakpoint()
    text = args.extract_plain_text().strip()
    week_num = week_num_auto()
    if text.isdigit() and int(text) in range(1, 10):
        await week_send(bot, week_num, event,int(text))
    else:
        await week_send(bot, week_num, event)


@下周值日表.handle()
async def _(bot: Bot, event: GroupMessageEvent,args: Message = CommandArg()):
    # breakpoint()
    text = args.extract_plain_text().strip()
    week_num = week_num_auto(1)
    if text.isdigit() and int(text) in range(1, 10):
        await week_send(bot, week_num, event,int(text))
    else:
        await week_send(bot, week_num, event)


@上周值日表.handle()
async def _(bot: Bot, event: GroupMessageEvent,args: Message = CommandArg()):
    # breakpoint()
    text = args.extract_plain_text().strip()
    week_num = week_num_auto(-1)
    if text.isdigit() and int(text) in range(1, 10):
        await week_send(bot, week_num, event,int(text))
    else:
        await week_send(bot, week_num, event)


async def week_send(bot: Bot, week_num: int, event: GroupMessageEvent,num:int=5):
    if num > 7:
        num = 7
    week_ls = ["周一","周二","周三","周四","周五","周六","周日"]
    num_ls = week_ls[:num]
    if is_week_file(week_num):
        await bot.send(
            event,
            MessageSegment.image(Path(currrent_path) / "值日表" / f"week_{week_num}.png"),
        )
        return
    else:
        ls = ["张浩翔", "邓章程", "尹齐河", "王伟宁", "周正南", "赵琳淞", "姜铭洋", "韩怀煜"]
        newls = random.sample(ls, num)
        img = await template_to_pic(
            Path(current_path) / "html",
            "table.html",
            {"week_num": week_num, "names": newls, "num_ls": num_ls},
        )
        with open(Path(current_path) / "值日表" / f"week_{week_num}.png", "wb") as f:
            f.write(img)
        await bot.send(event, MessageSegment.image(img))


def week_num_auto(i: int = 0) -> int:
    today = datetime.date.today()
    feb_27 = datetime.date(2023, 2, 27)
    week_num = (today - feb_27).days // 7 + 1 + i
    return week_num


def is_week_file(周数) -> bool:
    """检查给定路径下是否存在now_week文件"""
    路径 = Path(current_path) / "值日表" / f"week_{周数}.png"
    print(路径)
    if os.path.exists(路径):
        return True
    else:
        return False


# await 值日表.send(''.join(["\n" + '星期' + str(i+1) + "  "+newls[i] for i in range(5)]))


渣男 = on_command("渣男语录", priority=20)

biang = on_command("biang", priority=20)


@biang.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    text = text.replace(" ", "+")
    try:
        await biang.send(str(eval(text) / 1000))
    except Exception as e:
        logger.warning(str(e))


@小作文.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    text_list = text.split()
    try:
        if len(text_list) == 2:
            arg0, arg1 = text_list
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"https://zunslib.cn/api/public/ai?IferAction=article&a={arg0}&b={arg1}"
                )
                res_data = json.loads(resp.text)
                await 小作文.send(res_data["text"])
        else:
            await 小作文.send("小作文需要两个参数~用空格分开")
    except Exception as e:
        logger.warning(str(e))


@send_img.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    text = arg.extract_plain_text().strip()
    pattern = r"https://i\.pximg\.net/img-original/img/\d+/\d+/\d+/\d+/\d+/\d+/"
    pixiv_re = r"^https:\/\/www\.pixiv\.net\/artworks\/(\d+)$"
    if text:
        if re.search(pattern, text):
            new_url = text.replace("i.pximg.net", "pixiv.balh5.workers.dev")
            try:
                await send_forward_msg(
                    bot, event, "学渣", bot.self_id, [MessageSegment.image(file=new_url)]
                )
            except Exception as e:
                logger.warning(e)
        elif pid := re.search(pixiv_re, text).group(1):
            try:
                url_list = await get_pixivimg_url(pid)
                if url_list:
                    await send_forward_msg(
                        bot,
                        event,
                        "学渣",
                        bot.self_id,
                        [
                            MessageSegment.image(
                                file=i.replace("i.pximg.net", "pixiv.balh5.workers.dev")
                            )
                            for i in url_list
                        ],
                    )
            except Exception as e:
                logger.warning(e)
        else:
            try:
                await send_img.send(MessageSegment.image(file=text))
            except Exception as e:
                logger.warning(e)


@call_api.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    try:
        args, kwargs = Command.formatToCommand(str(arg), exe=True)
        result = await bot.call_api(args[0], **kwargs)
        await call_api.send(str(result))
    except BaseException as e:
        await call_api.send(traceback.format_exception(e))


@渣男.handle()
async def _():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://ovooa.com/API/qing/api.php", timeout=5)
        await 渣男.send(resp.text)
    except Exception as e:
        logger.warning("渣男error:" + e)


@壁纸.handle()
async def _(bot: Bot, msg: Message = CommandArg()):
    ls = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    try:
        if msg:
            msg = msg.extract_plain_text().strip()
            if msg in ls:
                url = f"https://ovooa.com/API/bizhi/api.php?type=image&msg={msg}"
                await 壁纸.send(MessageSegment.image(file=url))
        else:
            await 壁纸.send(
                "请在命令后添加正确的参数\n"
                + "1是美女壁纸2是动漫壁纸3是风景壁纸4是游戏壁纸5是文字壁纸6是视觉壁纸7是情感壁纸8是设计壁纸9是明星壁纸10是物语壁纸"
            )
    except Exception as e:
        logger.warning(e)


@原神.handle()
async def _():
    # try:
    #     await 原神.send(MessageSegment.image(file="https://ovooa.com/API/yuan/api?type=image"))
    # except Exception as e:
    #     logger.warning(e)
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://api.xunkong.cc/v1/wallpaper/random")
            js = json.loads(resp.text)
            await 原神.send(
                f"标题:{js['data']['title']}\n作者:{js['data']['author']}\n"
                + MessageSegment.image(file=js["data"]["url"])
            )
    except Exception as e:
        logger.warning(e)


@梦夏.handle()
async def _():
    try:
        await 梦夏.send(MessageSegment.image(file=random.choice(梦夏urls)))
    except Exception as e:
        logger.warning(e)
        await 梦夏.send("出错了:\n" + e)


@腿子.handle()
async def _(bot: Bot):
    try:
        await 腿子.send(
            MessageSegment.image(file="http://ovooa.com/API/meizi/api.php?type=image")
        )
    except Exception as e:
        logger.warning(e)


@github_img.handle()
async def _(bot: Bot, msg: Message = RegexMatched()):
    api = "https://opengraph.githubassets.com"
    id = "xuezha"
    print(api)
    msg = msg.strip()
    print(msg)
    msg = re.search(
        r"github.com\/[a-zA-Z0-9-]{1,39}\/[a-zA-Z0-9_-]{1,100}", msg
    ).group()
    res = msg.split("/")
    user, repo = res[1], res[2]
    imgurl = f"{api}/{id}/{user}/{repo}"
    print(imgurl)
    await github_img.send(MessageSegment.image(file=imgurl))


@拼音.handle()
async def _(bot: Bot, msg: Message = RegexMatched()):
    pinyin = "http://ovooa.com/API/pinyin/api.php?type=text&msg="
    text = msg.strip()
    if text.index("拼音") == 0:
        text = text[2:]
    else:
        text = text[: text.rindex("拼音")]
    print(msg)
    pinyin += text
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(pinyin, timeout=5)
        except Exception as e:
            logger.warning(e)
    await 拼音.finish(resp.text)


@戳一戳.handle()
async def _(bot: Bot, event: PokeNotifyEvent):
    print(event)
    txt_ls = ["功德", "缺德"]
    try:
        if event.group_id:
            print("群聊")
            info = await bot.get_group_member_info(
                group_id=int(event.group_id), user_id=int(event.user_id)
            )
            name = info.get("card", "") or info.get("nickname", "")
            await 戳一戳.send(f"{name}戳了我,{random.choice(txt_ls)}+1")
        else:
            print("私聊")
            info = await bot.get_stranger_info(user_id=int(event.user_id))
            name = info.get("nickname", "")
            msg = f"{name}戳了我,{random.choice(txt_ls)}+1"
            await bot.send_private_msg(user_id=event.user_id, message=msg)
    except Exception as e:
        print("未知错误 %s" % e)


async def get_pixivimg_url(pid: int):
    url = f"https://api.obfs.dev/api/pixiv/illust?id={pid}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        js = json.loads(resp.text)
        if page := js["illust"]["page_count"]:
            if page > 1:
                return [i["image_urls"]["original"] for i in js["illust"]["meta_pages"]]
            elif page == 0:
                return [js["illust"]["meta_single_page"]["original_image_url"]]


class Command:
    @staticmethod
    def get_keywords(old_dict: dict, keywords: dict) -> dict:
        """
        :param keywords:
        :param old_dict:
        :return:

        提取旧字典中设定键合成新字典
        """
        new = dict()
        for key in keywords:
            new[key] = old_dict.get(key, keywords[key])
        return new

    @staticmethod
    def formatToCommand(
        cmd: str, sep: str = " ", kw=True, exe=False
    ) -> Tuple[Tuple, Dict]:
        """
        :param exe: 执行为Python对象，失败则为字符串
        :param kw: 将有等号的词语分出
        :param sep: 分隔符,默认空格
        :param cmd: "arg1 arg2 para1=value1 para2=value2"
        :return:

        命令参数处理
        自动cq去义
        "%20"表示空格
        """
        cmd = Command.escape(cmd, blank=False)
        cmd_list = cmd.strip().split(sep)
        args = []
        keywords = {}
        for arg in cmd_list:
            arg = arg.replace("%20", " ")
            if "=" in arg and kw:
                value = arg.split("=")[1]
                if exe:
                    try:
                        value = eval(value)
                    except:
                        pass
                keywords[arg.split("=")[0]] = value
            else:
                if exe:
                    try:
                        arg = eval(arg)
                    except:
                        pass
                args.append(arg)
        args = tuple(args)
        return args, keywords

    @staticmethod
    def formatToString(*args, **keywords) -> str:

        """
        :param args:
        :param keywords:
        :return:
        escape会将空格转为%20，默认False不转，会将空格转为%20
        """

        string = ""
        for arg in args:
            string += Command.escape(arg) + " "
        kw_item = keywords.items()
        for item in kw_item:
            kw = "%s=%s" % (item[0], item[1])

            string += Command.escape(kw) + " "
        return string[:-1]

    @staticmethod
    def escape(text: str, blank=True) -> str:
        """
        CQ码去义

        :param text:
        :param blank: 转义%20为空格
        :return:
        """
        escape_data = {"&amp;": "&", "&#91;": "[", "&#93;": "]", "&#44;": ","}
        for esd in escape_data.items():
            text = text.replace(esd[0], esd[1])
        return text.replace("%20", " " if blank else "%20")


def is_qq(msg: str):
    return msg.isdigit() and 11 >= len(msg) >= 5


async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise Exception(f"{url} 下载失败！")


async def download_avatar(user_id: str) -> bytes:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    data = await download_url(url)
    if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
        url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100"
        data = await download_url(url)
    return data
