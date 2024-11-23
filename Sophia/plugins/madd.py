from Sophia import HANDLER
from Sophia.__main__ import Sophia
from config import OWNER_ID
from pyrogram import filters
import asyncio
import time
from pyrogram.enums import ChatType

@Sophia.on_message(filters.command("madd", prefixes=HANDLER) & filters.user(OWNER_ID) & filters.group)
async def mass_add(_, message):
    if len(message.command) < 2:
        return await message.reply("Please enter group user name to mass add.")
    time_start = time.time()
    success = 0
    chat_username = message.text.split(None, 1)[1]
    chat_info = await Sophia.get_chat(chat_username)
    if chat_info.type == ChatType.PRIVATE or chat_info.type == ChatType.CHANNEL:
        return await message.reply('Please enter a group id')
    loading_msg = await message.reply("Adding members...")
    async for member in Sophia.get_chat_members(message.chat.id):
        try:
            if not member.user.is_bot == True:
                output = await Sophia.add_chat_members(chat_username, member.user.id)
                if output == True:
                    success += 1
                await asyncio.sleep(2)
        except Exception as e:
            if not str(e) == """Telegram says: [400 CHAT_ADMIN_REQUIRED] - The method requires chat admin privileges (caused by "messages.UpdatePinnedMessage")""" and not str(e).startswith("Telegram says: [420 FLOOD_WAIT_X] - A wait"):
                print(e)
    await loading_msg.delete()
    if success <= 0:
        return await message.reply(f"Failed to add members ❌")
    await message.reply(f"Successfully added {success} members\nTaken time: {int(time.time() - time_start)}")
