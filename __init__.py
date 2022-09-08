from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.typing import T_State
import httpx
import asyncio
import hashlib
import shlex
from nonebot.adapters.onebot.v11 import (
    Bot, Message, MessageEvent, MessageSegment, GroupMessageEvent, unescape)
from typing import List, Optional
from nonebot.log import logger
from nonebot.params import State, Depends
from .data_source import yishijie, huoqu
from nonebot_plugin_imageutils import (Text2Image, text2image, BuildImage)
from io import BytesIO
from .utils import UserInfo
#from nonebot_plugin_txt2img import Txt2Img

__zx_plugin_name__ = "shindan"
__plugin_usage__ = """
usage：
    来测测你是什么样的人
    指令:
        今天是什么少女[@xxx]
        异世界转生[@xxx]
        卖萌[@xxx]
        抽老婆[@xxx]
""".strip()
__plugin_des__ = "基于 https://shindanmaker.com 的测定小功能"
__plugin_cmd__ = ["今天是什么少女", "异世界转生", "卖萌", "抽老婆"]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.1
__plugin_author__ = "ZeroBot-Plugin"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["今天是什么少女", "异世界转生", "卖萌", "抽老婆"],
}

yishi = on_command(
    "异世界转生", aliases={"异世界转生"}, priority=5, block=True
)

seseysj = on_command(
    "瑟瑟异世界", aliases={"娘化异世界"}, priority=5, block=True
)

chushou = on_command(
    "异世界触手", aliases={"触手异世界"}, priority=5, block=True
)

jin = on_command(
    "今天是什么少女", aliases={"今天是什么少女"}, priority=5, block=True
)

loli = on_command(
    "今天是什么萝莉", aliases={"我是什么萝莉"}, priority=5, block=True
)

zhuren = on_command(
    "主人的任务", aliases={"今天的任务"}, priority=5, block=True
)

meimo = on_command(
    "今日魅魔", aliases={"魅魔档案"}, priority=5, block=True
)

baibei = on_command(
    "今日败北", aliases={"我的败北"}, priority=5, block=True
)

mse = on_command(
    "m色色", aliases={"抖m色色", "抖m瑟瑟", "m瑟瑟"}, priority=5, block=True
)
# mai = on_command(
#    "卖萌", aliases={"卖萌"}, priority=5, block=True
# )

# chou = on_command(
#    "抽老婆", aliases={"抽老婆"}, priority=5, block=True
# )


def userinfo(event: MessageEvent):
    def _is_at_me_seg(segment: MessageSegment):
        return segment.type == "at" and str(segment.data.get("qq", "")) == str(
            event.self_id
        )

    msg: Message = event.get_message()

    if event.to_me:
        raw_msg = event.original_message
        i = -1
        last_msg_seg = raw_msg[i]
        if (
            last_msg_seg.type == "text"
            and not last_msg_seg.data["text"].strip()
            and len(raw_msg) >= 2
        ):
            i -= 1
            last_msg_seg = raw_msg[i]
        if _is_at_me_seg(last_msg_seg):
            msg.append(last_msg_seg)

    users: List[UserInfo] = []
    args: List[str] = []

    if event.reply:
        for img in event.reply.message["image"]:
            users.append(UserInfo(img_url=str(img.data.get("url", ""))))

    for msg_seg in msg:
        if msg_seg.type == "at":
            users.append(
                UserInfo(
                    qq=str(msg_seg.data.get("qq", "")),
                    group=str(event.group_id)
                    if isinstance(event, GroupMessageEvent)
                    else "",
                )
            )
        elif msg_seg.type == "image":
            users.append(UserInfo(img_url=str(
                msg_seg.data.get("url", ""))))
        elif msg_seg.type == "text":
            raw_text = str(msg_seg)
            try:
                texts = shlex.split(raw_text)
            except:
                texts = raw_text.split()
            for text in texts:
                if is_qq(text):
                    users.append(UserInfo(qq=text))
                elif text == "自己":
                    users.append(
                        UserInfo(
                            qq=str(event.user_id),
                            group=str(event.group_id)
                            if isinstance(event, GroupMessageEvent)
                            else "",
                        )
                    )
                else:
                    text = unescape(text).strip()
                    if text:
                        args.append(text)
    sender = UserInfo(qq=str(event.user_id))
    return {"sender": sender, "users": users, "args": args}


# 异世界转生


@yishi.handle()
async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]
        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))

        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "587874")
        elif text:
            result = await yishijie(text, "587874")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "587874")
        output = txt_to_img(result)
        await yishi.send(MessageSegment.image(output))
        # 以上结果为 PIL 的 Image 格式，若要直接 MessageSegment 发送，可以转为 BytesIO
        # await yishi.send(msg)
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await yishi.finish("小学渣无法为你转生哦~请重试")

# sese异世界转生


@seseysj.handle()
async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]
        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))

        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "635902")
        elif text:
            result = await yishijie(text, "635902")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "635902")
        output = txt_to_img(result)
        await seseysj.send(MessageSegment.image(output))
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await seseysj.finish("小学渣无法为你转生哦~请重试")


# 触手异世界转生
@chushou.handle()
async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]
        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))

        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "638952")
        elif text:
            result = await yishijie(text, "638952")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "638952")
        output = txt_to_img(result)
        await chushou.send(MessageSegment.image(output))
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await chushou.finish("小学渣无法为你转生哦~请重试")


def txt_to_img(text: str):
    img = text2image(text, max_width=1000)
    output = BytesIO()
    img.save(output, format="png")
    return output


# class UserInfo:
#     qq: str = ""
#     group: str = ""
#     name: str = ""
#     img_url: str = ""
#     img: BuildImage = BuildImage.new("RGBA", (640, 640))


def is_qq(msg: str):
    return msg.isdigit() and 11 >= len(msg) >= 5


# 今天是什么少女


@jin.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    try:
        print(event.sender.nickname)
        result = await yishijie(event.sender.nickname, "162207")
        await jin.send(result)
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await jin.finish("小学渣无法为你转生哦~请重试")

# 今天是什么萝莉


@loli.handle()
async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]
        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))

        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "1103711")
        elif text:
            result = await yishijie(text, "1103711")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "1103711")
        await loli.send(result)
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await loli.finish("小学渣无法为你转生哦~请重试")


# 主人的任务
@zhuren.handle()
async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]
        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))

        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "1079091")
        elif text:
            result = await yishijie(text, "1079091")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "1079091")
        output = txt_to_img(result)
        await zhuren.send(MessageSegment.image(output))
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await zhuren.finish("小学渣无法为你转生哦~请重试")


# 魅魔
@meimo.handle()
async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]

        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))

        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "1090381")
        elif text:
            result = await yishijie(text, "1090381")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "1090381")
        output = txt_to_img(result)
        await meimo.send(MessageSegment.image(output))
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await meimo.finish("小学渣无法为你转生哦~请重试")


# 败北
@baibei.handle()
async def _(bot: Bot,  msg: Message = CommandArg(),  userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]
        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))
        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "870739")
        elif text:
            result = await yishijie(text, "870739")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "870739")
        output = txt_to_img(result)
        await baibei.send(MessageSegment.image(output))
    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await baibei.finish("小学渣无法为你转生哦~请重试")


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


@mse.handle()
async def _(bot: Bot, msg: Message = CommandArg(), userinfo: dict = Depends(userinfo)):
    text = msg.extract_plain_text().strip()
    print("txt:"+str(text))
    try:
        users: UserInfo = userinfo["users"]

        args: List[str] = userinfo["args"]
        sender: UserInfo = userinfo["sender"]
        print("args:"+str(args))

        print("sender:"+str(sender))
        if users:
            user = await get_user_info(bot, users[0])
            print("users:"+str(user))
            result = await yishijie(user.name, "1123926")
        elif text:
            result = await yishijie(text, "1123926")
        else:
            sender = await get_user_info(bot, sender)
            result = await yishijie(sender.name, "1123926")
        output = txt_to_img(result)
        await mse.send(MessageSegment.image(output))

    except Exception as r:
        print('未知错误 %s' % r)
        await huoqu()
        await mse.finish("小学渣无法为你转生哦~请重试")


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
def Sender(sender: UserInfo):
    async def dependency(bot: Bot):
        await get_user_info(bot, sender)
        await download_image(sender)
        return sender
    return Depends(dependency)


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


async def download_image(user: UserInfo):
    img = None
    if user.qq:
        img = await download_avatar(user.qq)
    elif user.img_url:
        img = await download_url(user.img_url)

    if img:
        user.img = BuildImage.open(BytesIO(img))


async def get_user_info(bot: Bot, user: UserInfo):
    if not user.qq:
        return

    if user.group:
        info = await bot.get_group_member_info(
            group_id=int(user.group), user_id=int(user.qq)
        )
        user.name = info.get("card", "") or info.get("nickname", "")
        user.gender = info.get("sex", "")
    else:
        info = await bot.get_stranger_info(user_id=int(user.qq))
        user.name = info.get("nickname", "")
        user.gender = info.get("sex", "")
    return user
