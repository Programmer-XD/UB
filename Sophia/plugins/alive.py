from Sophia import HANDLER
from Sophia import MY_VERSION as Root_version
from Sophia.__main__ import Sophia
from config import OWNER_ID as OWN
from pyrogram import filters
from pyrogram import __version__ as ver_pyro
import asyncio
import os
from subprocess import getoutput as run

bot_start_time = datetime.now()

@Sophia.on_message(filters.command("alive", prefixes=HANDLER) & filters.user(OWN))
async def Sophia_Alive(_, message):
    await message.edit("`◖⁠⚆⁠ᴥ⁠⚆⁠◗ Loading...`")
    await asyncio.sleep(0.8)
    bot_inf = await Sophia.get_me()
    Name_of_ubot1 = bot_inf.first_name
    Name_of_ubot2 = bot_inf.last_name
    start_time = bot_start_time
    end_time = datetime.now()
    ping_time = (end_time - start_time).total_seconds() * 1000
    uptime = (end_time - bot_start_time).total_seconds()
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    if Name_of_ubot2 == None:
        Name_of_ubot = Name_of_ubot1
    else:
        Name_of_ubot = f"{Name_of_ubot1} {Name_of_ubot2}"
    try:
        py_ver = run("python --version")
    except Exception as e:
        print(e)
        py_ver = "Error"
    TEXT = f""" **~  𝑺𝒐𝒑𝒉𝒊𝒂 𝑺𝒚𝒔𝒕𝒆𝒎:**
━━━━━━━━━━━━━━━━━━━

❥ **Owner**: {Name_of_ubot}
❥ **My Version**: `{Root_version}`
❥ **Python Version**: `{py_ver}`
❥ **Pyrogram Version:** `{ver_pyro}`
❥ **Uptime:** `{int(hours)}h {int(minutes)}m {int(seconds)}s`

━━━━━━━━━━━━━━━━━━━
**Join @FutureCity005 & @Hyper_Speed0 ✨🥀**
"""
    await message.delete()
    await Sophia.send_photo(message.chat.id, photo="https://telegra.ph/file/c74ff3e597f9598ca7cbb.jpg", caption=TEXT)
