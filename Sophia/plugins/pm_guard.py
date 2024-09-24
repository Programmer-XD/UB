from Sophia import HANDLER
from Sophia.__main__ import Sophia
from config import OWNER_ID, BOTS_ALLOWED_TO_WORK_IN_BUSY_COMMANDS
from pyrogram import filters
import asyncio
import os
from Restart import restart_program
from pyrogram import enums
from Sophia.Database.backup_msg import *
from Sophia.Database.pmguard import *

warning_count = {}

async def denied_users(_, client, update):
    if not await GET_PM_GUARD():
        return False
    if update.chat.id not in (await GET_APPROVED_USERS()):
        return True
    else:
        return False
        
@Sophia.on_message(filters.command(["pmblock", "pmguard"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def set_pm_guard(_, message):
    is_pm_block_enabled = await GET_PM_GUARD()
    if is_pm_block_enabled:
        await UNSET_PM_GUARD()
        await message.reply("**➲ I have Disabled PmGuard Successfully ✅**")
        return
    else:
        if len(message.command) < 2:
            RESULT = await GET_DEFAULT_MESSAGE_LIMIT()
            RESULT2 = str(RESULT)
            if RESULT2.isdigit():
                await SET_PM_GUARD(RESULT)
                return await message.reply('**➲ I have enabled PmGuard successfully with Default Warning limit 🥀 ✨**')
            else:
                return await message.reply_text("➲ Master, Please enter the maximum message warning limit.")
        count = " ".join(message.command[1:])
        intCount = int(count)
        if intCount == 1:
            await message.reply("➲ Master, Count must be atleast 2.")
            return
        if intCount <= 0:
            await message.reply("➲ Master, Count must be positive Integers.")
            return
        if intCount > 20:
            await message.reply("➲ Maximum Applable warning count is 20.")
            return
        await SET_PM_GUARD(intCount)
        await message.reply('**➲ I have enabled PmGuard successfully 🥀 ✨**')
    

@Sophia.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
            )
async def warn_users(_, message):
    global warning_count
    user_id = message.chat.id
    maximum_message_count = await GET_WARNING_COUNT()
    if user_id not in warning_count:
        warning_count[user_id] = 0
    warning_count[user_id] += 1
    if warning_count[user_id] < maximum_message_count:
        await message.reply(f"**⚠️ WARNING**\n\nSorry, my master has enabled the PmGuard feature. You can't send messages until my master approves you or disabling this feature. If you Spam Here or the warning exceeds the limits I will Block You.\n\n**➲ Warning Counts** `{warning_count[user_id]}/{maximum_message_count}`")
    elif warning_count[user_id] >= maximum_message_count:
        try:
            await message.reply("➲ You have exceeded your limits, so I have blocked you!")
            await Sophia.block_user(user_id)
        except Exception as e:
            print(e)
            await Sophia.send_message(OWNER_ID, e)
    if await GET_BACKUP():
        backup_chat = await GET_BACKUP_CHANNEL_ID(message.chat.id)
        try:
            await Sophia.forward_messages(backup_chat, message.chat.id, message.id)
        except Exception as e:
            if str(e) == """Telegram says: [400 CHANNEL_INVALID] - The channel parameter is invalid (caused by "channels.GetChannels")""":
                chat = await Sophia.create_channel(f"{message.chat.first_name} BACKUP", "~ @Hyper_Speed0")
                await ADD_BACKUP_CHAT(message.chat.id)
                await SET_BACKUP_CHANNEL_ID(message.chat.id, chat.id)
                await Sophia.forward_messages(chat.id, message.chat.id, message.id)
                return await Sophia.archive_chats(chat.id)
            else:
                print(f"Error on pm_guard.py when backuping message {message.chat.id}: {str(e)}")
            
                    

@Sophia.on_message(filters.command(['a', 'approve', 'allow'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def approve_user(_, message):
    is_pm_block_enabled = await GET_PM_GUARD()
    approved_users = await GET_APPROVED_USERS()
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        try:
            if user_id in approved_users:
                await message.reply('**➲ This User is already approved ✨ 🥀**')
                return
            await ADD_APPROVED_USER(user_id)
            await message.reply("➲ Successfully Approved 🥀⚡")
        except Exception as e:
            await message.reply(f"Sorry, i got a error while approving this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')


@Sophia.on_message(filters.command(['ua', 'unapprove', 'deny', 'd'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def Unapprove_user(_, message):
    is_pm_block_enabled = await GET_PM_GUARD()
    approved_users = await GET_APPROVED_USERS()
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        if user_id not in approved_users:
            await message.reply("**➲ This user is Not Approved yet ❌.**")
            return
        try:
            await REMOVE_APPROVED_USER(user_id)
            await message.reply("➲ Successfully Unapproved ✨🗿.")
        except Exception as e:
            await message.reply(f"Sorry, i got a error while unapproving this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')
            

        
@Sophia.on_message(filters.command(['cw', 'clearwarns'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def clear_warn(_, message):
    global warning_count
    is_pm_block_enabled = await GET_PM_GUARD()
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        try:
            user_id = message.chat.id
            warning_count[user_id] = 0
            await message.reply("➲ Successfully Cleared All Warnings 🗿🔥.")
        except Exception as e:
            await message.reply(f"Sorry, i got a error while Clearing Warns for this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')
                
@Sophia.on_message(filters.command(['setmsglimit', 'setpmlimit'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def set_limit(_, message):
    if len(message.command) < 2:
        return await message.reply_text("➲ Please enter the maximum message warning limit.")
    count = " ".join(message.command[1:])
    intCount = int(count)
    if intCount == 1:
        await message.reply("➲ Count must be atleast 2.")
        return
    if intCount <= 0:
        await message.reply("➲ Count must be positive Integers.")
        return
    if intCount > 20:
        await message.reply("➲ Maximum Applable warning count is 20.")
        return
    await SET_DEFAULT_MESSAGE_LIMIT(intCount)
    await message.reply(f"**➲ Successfuly set default Warning limit! 🥀 ✨**")

@Sophia.on_message(filters.command(["ausers", "achats"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def get_approved_users(_, message):
    MSG = await message.reply("`Processing...`")
    NAMES = []
    FORMATTED_NAMES = ""
    async for dialog in Sophia.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            if dialog.chat.id in await GET_APPROVED_USERS():
                GET_CHAT = await Sophia.get_chat(dialog.chat.id)
                First_name = GET_CHAT.first_name
                NAMES.append(First_name)
    for name in NAMES:
        FORMATTED_NAMES += f"-» `{name}`\n"
    await MSG.edit(f"**Results:**\n{FORMATTED_NAMES}")
# END
