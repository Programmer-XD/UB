from Sophia import HANDLER
from Sophia.__main__ import Sophia
from config import OWNER_ID, Always_Approved_Users_From_Pmblock, BOTS_ALLOWED_TO_WORK_IN_BUSY_COMMANDS
from pyrogram import filters
import asyncio
import os
from Restart import restart_program
from pyrogram import enums
from Sophia.Database.pmguard import *

warning_count = {}

async def denied_users(filter, client: Client, message: Message): # Thanks To KoraXD 
    if not await GET_PM_GUARD():
        return False
    if message.chat.id in (await GET_APPROVED_USERS()):
        return False
    else:
        return True

@Sophia.on_message(filters.command(["pmblock", "pmguard"], prefixes=HANDLER) & filters.user(OWNER_ID))
async def set_pm_guard(_, message):
    is_pm_block_enabled = await GET_PM_GUARD()
    if is_pm_block_enabled:
        await UNSET_PM_GUARD()
        await message.reply("**➲ I have Disabled PmGuard Successfully ✅**")
        return
    else:
        if len(message.command) < 2:
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
    is_pm_block_enabled = await GET_PM_GUARD()
    if is_pm_block_enabled:
        valueotazuki = "value57"
    else:
        restart_program()
    user_id = message.chat.id
    maximum_message_count = await GET_WARNING_COUNT()
    if BOTS_ALLOWED_TO_WORK_IN_BUSY_COMMANDS == False:
        if message.chat.type == enums.ChatType.BOT:
            return
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
            
                    

@Sophia.on_message(filters.command(['a', 'approve'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def Approve_user(_, message):
    global approved_users
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        try:
            if user_id in approved_users:
                await message.reply('**➲ This User is Already Approved ✨ 🥀**')
                return
            approved_users.append(user_id)
            await message.reply("➲ Successfully Approved 🥀⚡")
        except Exception as e:
            await message.reply(f"Sorry, i got a error while approving this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')


@Sophia.on_message(filters.command(['ua', 'unapprove'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def Unapprove_user(_, message):
    global approved_users
    if is_pm_block_enabled:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            await message.reply("➲ This Command Only Works On Private Chats ❌.")
            return
        user_id = message.chat.id
        try:
            approved_users.remove(user_id)
            await message.reply("➲ Successfully Unapproved ✨🗿.")
        except Exception as e:
            if str(e) == "list.remove(x): x not in list":
                await message.reply("**➲ This user is Not Approved yet ❌.**")
                return
            await message.reply(f"Sorry, i got a error while unapproving this user\n\n{e}")
    else:
        if message.chat.type == enums.ChatType.SUPERGROUP:
            return
        await message.reply('**➲ PmGuard Not Enabled ❌.**')
            

        
@Sophia.on_message(filters.command(['cw', 'clearwarns'], prefixes=HANDLER) & filters.user(OWNER_ID))
async def Clear_User_Warns(_, message):
    global warning_count
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
                

# END
