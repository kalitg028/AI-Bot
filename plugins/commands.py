from pyrogram import Client, filters
from pyrogram.errors import *
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import *
import asyncio
from Script import text
from .db import data
from .fsub import get_fsub

@Client.on_message(filters.command("start"))
async def start_cmd(client, message):
    if await data.get_user(message.from_user.id) is None:
        await data.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text.LOG.format(message.from_user.mention, message.from_user.id)
        )
    if IS_FSUB and not await get_fsub(client, message):return
    await message.reply_text(
        text.START.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'), InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help')],
            [InlineKeyboardButton('♻ ᴅᴇᴠᴇʟᴏᴘᴇʀ ♻', url='https://telegram.me/TechifyRahul')]
        ]),
        disable_web_page_preview=True
    )

@Client.on_message(filters.command("users") & filters.user(ADMIN))
async def total_users(client: Client, message: Message):
    try:
        total = await data.users.count_documents({})
        await message.reply_text(f"📊 **Total Users:** `{total}`")
    except Exception as e:
        print(f"Error in /users command: {e}")
        await message.reply_text("⚠️ An error occurred while fetching user count.")

@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(ADMIN))
async def broadcasting_func(client: Client, message: Message):
    try:
        msg = await message.reply_text("Wait a second!")
        if not message.reply_to_message:
            return await msg.edit("<b>Please reply to a message to broadcast.</b>")
        await msg.edit("Processing ...")
        completed = 0
        failed = 0
        to_copy_msg = message.reply_to_message
        users_list = await data.get_all_users()
        
        for i, userDoc in enumerate(users_list):
            if i % 20 == 0:
                await msg.edit(f"Total: {i}\nCompleted: {completed}\nFailed: {failed}")
            user_id = userDoc.get("user_id")
            if not user_id:
                continue
            try:
                await to_copy_msg.copy(int(user_id))
                completed += 1
                await asyncio.sleep(0.1)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await to_copy_msg.copy(int(user_id))
                    completed += 1
                except Exception:
                    failed += 1
            except Exception as e:
                print(f"Error in broadcasting to {user_id}: {e}")
                failed += 1
                
        await msg.edit(f"Successfully Broadcasted\nTotal: {len(users_list)}\nCompleted: {completed}\nFailed: {failed}")
    except Exception as e:
        print(f"Error in broadcast: {e}")
        await message.reply_text("An error occurred while broadcasting.")
