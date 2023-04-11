from ast import Try
import datetime
from nonebot import on_command, on_fullmatch, on_regex, on_endswith, on_notice
from nonebot.params import CommandArg, EventPlainText, RegexMatched
from nonebot.typing import T_State
from nonebot import require
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import (
    template_to_pic
)
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
    Bot, Message, MessageEvent, MessageSegment, GroupMessageEvent, unescape, PokeNotifyEvent)
from typing import List, Optional, Type, Tuple, Dict
from nonebot.log import logger
from PIL import Image
# from nonebot.params import Depends
from .data_source import yishijie, huoqu, send_forward_msg, current_path
# from nonebot_plugin_imageutils import (Text2Image, text2image, BuildImage)
import os
# from .utils import UserInfo
from nonebot.adapters.onebot.v11.helpers import HandleCancellation
#from nonebot_plugin_txt2img import Txt2Img

# yishi = on_command(
#     "异世界转生", aliases={"异世界转生"}, priority=5, block=True
# )

# seseysj = on_command(
#     "瑟瑟异世界", aliases={"娘化异世界"}, priority=5, block=True
# )

# chushou = on_command(
#     "异世界触手", aliases={"触手异世界"}, priority=5, block=True
# )

# jin = on_command(
#     "今天是什么少女", aliases={"今天是什么少女"}, priority=5, block=True
# )

# loli = on_command(
#     "今天是什么萝莉", aliases={"我是什么萝莉"}, priority=5, block=True
# )

# zhuren = on_command(
#     "主人的任务", aliases={"今天的任务"}, priority=5, block=True
# )

# meimo = on_command(
#     "今日魅魔", aliases={"魅魔档案"}, priority=5, block=True
# )

# baibei = on_command(
#     "今日败北", aliases={"我的败北"}, priority=5, block=True
# )

# mse = on_command(
#     "m色色", aliases={"抖m色色", "抖m瑟瑟", "m瑟瑟"}, priority=5, block=True
# )

# huahua = on_command(
#     "ai画画", aliases={"aihuahua"}, priority=5, block=True
# )
# mai = on_command(
#    "卖萌", aliases={"卖萌"}, priority=5, block=True
# )

# chou = on_command(
#    "抽老婆", aliases={"抽老婆"}, priority=5, block=True
# )

with open(current_path+"User Illust.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()[1:-1]    # 读取文件内容并去除首尾空行
    梦夏urls = list(filter(bool, lines))       # 过滤掉空行，并转为list

壁纸 = on_command("来张壁纸", priority=20)

拼音 = on_regex(r"(^拼音.+)|(.+拼音$)", priority=1)

github_img = on_regex(
    r"github\.com\/[a-zA-Z0-9-]{1,39}\/[a-zA-Z0-9_-]{1,100}", priority=1)

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
    return event.group_id == 747416482

值日表 = on_fullmatch("值日表",rule=_zhiri,priority=20)

@值日表.handle()
async def _():
    def is_week_file(周数):
        """检查给定路径下是否存在PNG文件"""
        if os.path.exists("current_path"+"值日表"+f"week_{周数}.png"):
            return True
        else:
            return False
    
    today = datetime.date.today()
    feb_27 = datetime.date(2023, 2, 27)
    # breakpoint()
    week_num = (today - feb_27).days // 7 +1
    if is_week_file(week_num):
        await 值日表.send(MessageSegment.image(file=f"{current_path}值日表/"+f"week_{week_num}.png"))
        return
    ls = ["张浩翔","邓长成","尹启河","王伟宁","周正南","赵琳淞","姜明洋","韩怀煜"]
    newls = random.sample(ls, 5)
    template_to_pic(current_path+"html","table.html",{"week_num":week_num,"ls":newls})

    
    # await 值日表.send(''.join(["\n" + '星期' + str(i+1) + "  "+newls[i] for i in range(5)]))


渣男 = on_command("渣男语录", priority=20)

biang = on_command("biang", priority=20)

@biang.handle()
async def _(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    text = args.extract_plain_text().strip()
    text = text.replace(" ","+")
    try:
        await biang.send(str(eval(text)/1000))
    except Exception as e:
        logger.warning(str(e))


@小作文.handle()
async def _(matcher:Matcher,args:Message=CommandArg()):
    text = args.extract_plain_text().strip()
    text_list = text.split()
    try:
        if len(text_list) == 2 :
            arg0,arg1 = text_list
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"https://zunslib.cn/api/public/ai?IferAction=article&a={arg0}&b={arg1}")
                res_data = json.loads(resp.text)
                await 小作文.send(res_data["text"])
        else:
            await 小作文.send("小作文需要两个参数~用空格分开")
    except Exception as e:
        logger.warning(str(e))



@send_img.handle()
async def _(bot: Bot,event: MessageEvent,arg: Message = CommandArg()):
    text = arg.extract_plain_text().strip()
    pattern = r"https://i\.pximg\.net/img-original/img/\d+/\d+/\d+/\d+/\d+/\d+/"
    pixiv_re = r"^https:\/\/www\.pixiv\.net\/artworks\/(\d+)$"
    if text:
        if re.search(pattern, text):
            new_url = text.replace("i.pximg.net", "pixiv.balh5.workers.dev")
            try:
                await send_forward_msg(bot, event, "学渣", bot.self_id, [MessageSegment.image(file=new_url)])
            except Exception as e:
                logger.warning(e)
        elif pid := re.search(pixiv_re, text).group(1):
            try:
                url_list = await get_pixivimg_url(pid)
                if url_list:
                    await send_forward_msg(bot, event, "学渣", bot.self_id, [MessageSegment.image(file=i.replace("i.pximg.net", "pixiv.balh5.workers.dev")) for i in url_list])
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
        logger.warning("渣男error:"+e)

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
            await 壁纸.send("请在命令后添加正确的参数\n"+"1是美女壁纸2是动漫壁纸3是风景壁纸4是游戏壁纸5是文字壁纸6是视觉壁纸7是情感壁纸8是设计壁纸9是明星壁纸10是物语壁纸")
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
            await 原神.send(f"标题:{js['data']['title']}\n作者:{js['data']['author']}\n"+MessageSegment.image(file=js['data']['url']))
    except Exception as e:
        logger.warning(e)

@梦夏.handle()
async def _():
    try:
        await 梦夏.send(MessageSegment.image(file=random.choice(梦夏urls)))
    except Exception as e:
        logger.warning(e)
        await 梦夏.send("出错了:\n"+e)


@腿子.handle()
async def _(bot: Bot):
    try:
        await 腿子.send(MessageSegment.image(file="http://ovooa.com/API/meizi/api.php?type=image"))
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
        r"github.com\/[a-zA-Z0-9-]{1,39}\/[a-zA-Z0-9_-]{1,100}", msg).group()
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
        text = text[:text.rindex("拼音")]
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
    txt_ls=["功德","缺德"]
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
            await bot.send_private_msg(user_id=event.user_id,message=msg)
    except Exception as e:
        print('未知错误 %s' % e)

async def get_pixivimg_url(pid:int):
    url = f"https://api.obfs.dev/api/pixiv/illust?id={pid}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        js = json.loads(resp.text)
        if page := js["illust"]["page_count"]:
            if page > 1:
                return [i["image_urls"]["original"] for i in js["illust"]["meta_pages"]]
            elif page == 0:
                return [js["illust"]["meta_single_page"]["original_image_url"]]



# def userinfo(event: MessageEvent):
#     def _is_at_me_seg(segment: MessageSegment):
#         return segment.type == "at" and str(segment.data.get("qq", "")) == str(
#             event.self_id
#         )

#     msg: Message = event.get_message()

#     if event.to_me:
#         raw_msg = event.original_message
#         i = -1
#         last_msg_seg = raw_msg[i]
#         if (
#             last_msg_seg.type == "text"
#             and not last_msg_seg.data["text"].strip()
#             and len(raw_msg) >= 2
#         ):
#             i -= 1
#             last_msg_seg = raw_msg[i]
#         if _is_at_me_seg(last_msg_seg):
#             msg.append(last_msg_seg)

#     users: List[UserInfo] = []
#     args: List[str] = []

#     if event.reply:
#         for img in event.reply.message["image"]:
#             users.append(UserInfo(img_url=str(img.data.get("url", ""))))

#     for msg_seg in msg:
#         if msg_seg.type == "at":
#             users.append(
#                 UserInfo(
#                     qq=str(msg_seg.data.get("qq", "")),
#                     group=str(event.group_id)
#                     if isinstance(event, GroupMessageEvent)
#                     else "",
#                 )
#             )
#         elif msg_seg.type == "image":
#             users.append(UserInfo(img_url=str(
#                 msg_seg.data.get("url", ""))))
#         elif msg_seg.type == "text":
#             raw_text = str(msg_seg)
#             try:
#                 texts = shlex.split(raw_text)
#             except:
#                 texts = raw_text.split()
#             for text in texts:
#                 if is_qq(text):
#                     users.append(UserInfo(qq=text))
#                 elif text == "自己":
#                     users.append(
#                         UserInfo(
#                             qq=str(event.user_id),
#                             group=str(event.group_id)
#                             if isinstance(event, GroupMessageEvent)
#                             else "",
#                         )
#                     )
#                 else:
#                     text = unescape(text).strip()
#                     if text:
#                         args.append(text)
#     sender = UserInfo(qq=str(event.user_id))
#     return {"sender": sender, "users": users, "args": args}


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
    def formatToCommand(cmd: str, sep: str = " ", kw=True, exe=False) -> Tuple[Tuple, Dict]:
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
        escape_data = {
            "&amp;": "&",
            "&#91;": "[",
            "&#93;": "]",
            "&#44;": ","
        }
        for esd in escape_data.items():
            text = text.replace(esd[0], esd[1])
        return text.replace("%20", " " if blank else "%20")





# ai画画


# @huahua.handle()
# async def _(matcher: Matcher, bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
#     text = msg.extract_plain_text().strip()
#     if text:
#         matcher.set_arg("text", text)
# style_list = ["古风", "油画", "水彩画", "卡通画", "二次元", "浮世绘", "蒸汽波艺术", "low poly",
#               "像素风格", "概念艺术", "未来主义", "赛博朋克", "写实风格", "洛丽塔风格", "巴洛克风格", "超现实主义"]


# @huahua.got(key="text", prompt="请输入描述文本, 格式为: \n图片主体，细节词，修饰词，等若干修饰词\n例子: \n火焰，凤凰，少女，未来感，高清，3d，精致面容，cg感，古风，唯美，毛发细致，上半身立绘")
# @huahua.got(key="style", prompt="请输入作图风格,选择以下其中一种:\n古风,油画,水彩画,卡通画,二次元,浮世绘,蒸汽波艺术,low poly,像素风格,概念艺术,未来主义,赛博朋克,写实风格,洛丽塔风格,巴洛克风格,超现实主义")
# async def _(bot: Bot, event: MessageEvent, matcher: Matcher, cancel=HandleCancellation("已取消")):
#     await huahua.send("预计30秒-5分钟")
#     text = str(matcher.get_arg("text"))
#     style = str(matcher.get_arg("style"))
#     try:
#         access_token = await get_token()
#         taskId = await get_taskId(access_token, text, style)
#         if taskId == None:
#             await huahua.finish(f'主题“{text}”违规，请重新给定任务描述')
#             return
#         await asyncio.sleep(30)
#         msg_list = await get_img(access_token, taskId)
#         if msg_list == None:
#             await huahua.finish(f'无法绘制主题为“{text}”的{style}!')
#             return
#         # msg_list = await aihuahua(text, style)
#         await send_forward_msg(bot, event, "学渣", bot.self_id, msg_list)
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huahua.finish("出错力~")
# 异世界转生


# @yishi.handle()
# async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]
#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))

#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "587874")
#         elif text:
#             result = await yishijie(text, "587874")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "587874")
#         output = txt_to_img(result)
#         await yishi.send(MessageSegment.image(output))
#         # 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO
#         # await yishi.send(msg)
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await yishi.finish("小学渣无法为你转生哦~请重试")

# sese异世界转生


# @seseysj.handle()
# async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]
#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))

#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "635902")
#         elif text:
#             result = await yishijie(text, "635902")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "635902")
#         output = txt_to_img(result)
#         await seseysj.send(MessageSegment.image(output))
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await seseysj.finish("小学渣无法为你转生哦~请重试")


# 触手异世界转生
# @chushou.handle()
# async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]
#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))

#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "638952")
#         elif text:
#             result = await yishijie(text, "638952")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "638952")
#         output = txt_to_img(result)
#         await chushou.send(MessageSegment.image(output))
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await chushou.finish("小学渣无法为你转生哦~请重试")


# def txt_to_img(text: str):
#     img = text2image(text, max_width=1000)
#     output = BytesIO()
#     img.save(output, format="png")
#     return output


# class UserInfo:
#     qq: str = ""
#     group: str = ""
#     name: str = ""
#     img_url: str = ""
#     img: BuildImage = BuildImage.new("RGBA", (640, 640))


def is_qq(msg: str):
    return msg.isdigit() and 11 >= len(msg) >= 5


# 今天是什么少女


# @jin.handle()
# async def _(bot: Bot, event: MessageEvent, state: T_State):
#     try:
#         print(event.sender.nickname)
#         result = await yishijie(event.sender.nickname, "162207")
#         await jin.send(result)
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await jin.finish("小学渣无法为你转生哦~请重试")

# 今天是什么萝莉


# @loli.handle()
# async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]
#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))

#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "1103711")
#         elif text:
#             result = await yishijie(text, "1103711")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "1103711")
#         await loli.send(result)
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await loli.finish("小学渣无法为你转生哦~请重试")


# # 主人的任务
# @zhuren.handle()
# async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]
#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))

#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "1079091")
#         elif text:
#             result = await yishijie(text, "1079091")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "1079091")
#         output = txt_to_img(result)
#         await zhuren.send(MessageSegment.image(output))
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await zhuren.finish("小学渣无法为你转生哦~请重试")


# # 魅魔
# @meimo.handle()
# async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]

#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))

#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "1090381")
#         elif text:
#             result = await yishijie(text, "1090381")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "1090381")
#         output = txt_to_img(result)
#         await meimo.send(MessageSegment.image(output))
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await meimo.finish("小学渣无法为你转生哦~请重试")


# # 败北
# @baibei.handle()
# async def _(bot: Bot,  msg: Message = CommandArg(),  userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]
#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))
#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "870739")
#         elif text:
#             result = await yishijie(text, "870739")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "870739")
#         output = txt_to_img(result)
#         await baibei.send(MessageSegment.image(output))
#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await baibei.finish("小学渣无法为你转生哦~请重试")


# def Users(min_num: int = 1, max_num: int = 1):
#     async def dependency(bot: Bot, state: T_State = State()):
#         users: List[UserInfo] = state[USERS_KEY]
#         if len(users) > max_num or len(users) < min_num:
#             return

#         for user in users:
#             await get_user_info(bot, user)
#             await download_image(user)
#         return users

#     return Depends(dependency)

# def User():
#     async def dependency(users: Optional[List[UserInfo]] = Users()):
#         if users:
#             return users[0]

#     return Depends(dependency)
# 抖m色色

# {'sender': UserInfo(qq='2779375323', group='', name='', gender='unknown', img_url='', img= < nonebot_plugin_imageutils.build_image.BuildImage object at 0x7fdc8315ae30 >), 'users': [UserInfo(qq='782694668', group='747416482', name='', gender='unknown', img_url='', img= < nonebot_plugin_imageutils.build_image.BuildImage object at 0x7fdc8315ae30 > )],
#
#
# 'args': ['m色色']}


# @mse.handle()
# async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
#     text = msg.extract_plain_text().strip()
#     print("txt:"+str(text))
#     try:
#         users: UserInfo = userinfo["users"]

#         args: List[str] = userinfo["args"]
#         sender: UserInfo = userinfo["sender"]
#         print("args:"+str(args))

#         print("sender:"+str(sender))
#         if users:
#             user = await get_user_info(bot, users[0])
#             print("users:"+str(user))
#             result = await yishijie(user.name, "1123926")
#         elif text:
#             result = await yishijie(text, "1123926")
#         else:
#             sender = await get_user_info(bot, sender)
#             result = await yishijie(sender.name, "1123926")
#         output = txt_to_img(result)
#         await mse.send(MessageSegment.image(output))

#     except Exception as r:
#         print('未知错误 %s' % r)
#         await huoqu()
#         await mse.finish("小学渣无法为你转生哦~请重试")


# 卖萌
# @mai.handle()
# async def _(bot: Bot, event: MessageEvent, state: T_State):
#    try:
#        result = await maimeng(event.sender.nickname)
#        await mai.send(result)
#    except Exception:
#        await huoqu()
#        await mai.finish("小真寻卖不了萌呢~")


# 抽老婆
# @chou.handle()
# async def _(bot: Bot, event: MessageEvent, state: T_State):
#    try:
#        x = await laopo(event.sender.nickname)
#        result = x[0]
#        url = x[1]
#        lao = x[2]
#        result += image(url)
#        result += lao
#        await chou.send(result)
#    except Exception:
#        await huoqu()
#        await yishi.finish("小真寻暂时查不到哦~")


# def Sender(sender: UserInfo):
#     async def dependency(bot: Bot):
#         await get_user_info(bot, sender)
#         await download_image(sender)
#         return sender
#     return Depends(dependency)


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


# async def download_image(user: UserInfo):
#     img = None
#     if user.qq:
#         img = await download_avatar(user.qq)
#     elif user.img_url:
#         img = await download_url(user.img_url)

#     if img:
#         user.img = BuildImage.open(BytesIO(img))


# async def get_user_info(bot: Bot, user: UserInfo):
#     if not user.qq:
#         return

#     if user.group:
#         info = await bot.get_group_member_info(
#             group_id=int(user.group), user_id=int(user.qq)
#         )
#         user.name = info.get("card", "") or info.get("nickname", "")
#         user.gender = info.get("sex", "")
#     else:
#         info = await bot.get_stranger_info(user_id=int(user.qq))
#         user.name = info.get("nickname", "")
#         user.gender = info.get("sex", "")
#     return user
