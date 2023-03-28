from telethon import TelegramClient, Button, events
from telethon.utils import get_peer_id
from aioredis import Redis
from settings import *
from .dbf import Dbf
import asyncio, os

############## Client Setup ###############

dB = Redis(
    username=REDISUSER,
    host=REDISHOST,
    port=REDISPORT,
    password=REDISPASSWORD,
    decode_responses=True,
)
db = Dbf(dB)

client = TelegramClient(None, 6, "eb06d4abfb49dc3eeb1aeb98ae0f581e")
loop = asyncio.get_event_loop()


async def start_bot(token: str) -> None:
    await client.start(bot_token=token)
    client.me = await client.get_me()
    print(client.me.username, "is Online Now.")

loop.run_until_complete(start_bot(BOT_TOKEN))

HELP = """
/addch - **Add The Channel**

/remch - **Remove The Channel**

/listch - **List All Channels**
"""

############## Funcs ###############

@client.on(events.NewMessage(incoming=True, pattern="^/start$"))
async def strt(e):
    await e.reply("Hi")

@client.on(events.NewMessage(incoming=True, pattern="^/help$"))
async def hlp(e):
    e.reply(HELP)

@client.on(events.NewMessage(incoming=True, pattern="^/addch"))
async def adch(event):
    if event.sender_id not in ADMINS:
        return
    try:
        async with client.conversation(event.sender_id, timeout=2000) as conv:
            await conv.send_message(
                "Send Channel Username or Id\n__make sure bot is admin there__"
            )
            res = await conv.get_response()
            try:
                chat = int(res.text)
            except BaseException:
                chat = res.text.strip().split("/")[-1]
            try:
                chat = await client.get_entity(chat) 
            except BaseException:
                return await conv.send_message("Wrong Username/id")
            await conv.send_message(
                "Send Time Interval of Deleting Msgs In Seconds.\nEx - `120`"
            )
            res_2 = await conv.get_response()
            try:
                sec = int(res_2.text)
            except BaseException:
                return await conv.send_message("Invalid Input")
            await db.set_chat_list(chat.id, sec)
            return await conv.send_message("Added Successfully.")
    except TimeoutError:
        pass

@client.on(events.NewMessage(incoming=True, pattern="^/remch"))
async def rch(event):
    if event.sender_id not in ADMINS:
        return
    chats = await db.get_chat_list()
    if not chats:
        return await event.reply("No Chat List Found")
    try:
        async with client.conversation(event.sender_id, timeout=2000) as conv:
            await conv.send_message("Give Channel Username or Id To remove from List.")
            res = await conv.get_response()
            try:
                chat = int(res.text)
            except BaseException:
                chat = res.text.strip().split("/")[-1]
            try:
                chat = await client.get_entity(chat)
                await db.rem_chat_list(chat.id)
                return await conv.send_message("Removed Successfully.")
            except BaseException:
                return await conv.send_message("Wrong Username/id")
    except TimeoutError:
        pass

@client.on(events.NewMessage(incoming=True, pattern="^/listch"))
async def lstch(event):
    if event.sender_id not in ADMINS:
        return
    chats = await db.get_chat_list()
    txt = ""
    if chats:
        await event.answer("Processing...")
        txt += "Channel List\n\n"
        for chat in chats.keys():
            try:
                ent = await client.get_entity(chat)
                txt += f"__{ent.title}__\n`{chats[chat]}s`\n\n"
            except BaseException:
                pass
    else:
        return await event.answer("No Chat List Found")

@client.on(events.NewMessage(incoming=True))
async def deleter(e):
    x = await db.get_chat_list()
    th = await e.get_chat()
    id = get_peer_id(th)
    if id not in x:
        return
    try:
        await asyncio.sleep(int(x[id]))
        await e.delete()
    except Exception as ex:
        print(str(ex))

client.run_until_disconnected()
