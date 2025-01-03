import asyncio
import time
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from info import *  # Ensure OWNER_ID is defined here
from database.users import db  # Ensure db methods are defined here

lock = asyncio.Lock()  # Define a lock for broadcast

class temp(object):
    ME = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False
    U_NAME = None
    B_NAME = None
    B_LINK = None
    SETTINGS = {}
    FILES_ID = {}
    BANNED_USERS = []
    BANNED_CHATS = []
    USERS_CANCEL = False
    GROUPS_CANCEL = False    
    CHAT = {}

@Client.on_message(filters.command("users") & filters.user(OWNER_ID))
async def users(client, message):
    total_users = await db.total_users_count()
    text = f"**Total Users: {total_users}**"
    await message.reply_text(
        text=text,
        quote=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close')]]),
        disable_web_page_preview=True
    )


async def broadcast_messages(user_id, message, pin):
    try:
        m = await message.copy(chat_id=user_id)
        if pin:
            await m.pin(both_sides=True)
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, pin)
    except Exception as e:
        await db.delete_user(int(user_id))
        return "Error"


def get_readable_time(seconds):
    periods = [('days', 86400), ('hours', 3600), ('minutes', 60), ('seconds', 1)]
    result = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result.append(f'{int(period_value)} {period_name}')
    return ' '.join(result)


@Client.on_message(filters.command(["broadcast", "pin_broadcast"]) & filters.user(OWNER_ID) & filters.reply)
async def users_broadcast(client, message):
    if lock.locked():
        return await message.reply('Currently processing a broadcast. Please wait for it to complete.')
    
    # Determine if the message should be pinned
    pin = message.command[0] == 'pin_broadcast'

    users = await db.get_all_users()  # Get all users from the database
    b_msg = message.reply_to_message
    b_sts = await message.reply_text(text='Broadcasting messages to users...')
    start_time = time.time()
    total_users = await db.total_users_count()
    done, failed, success = 0, 0, 0

    async with lock:
        async for user in users:
            time_taken = get_readable_time(time.time() - start_time)
            if temp.USERS_CANCEL:  # Cancel if the broadcast is interrupted
                temp.USERS_CANCEL = False
                await b_sts.edit(
                    f"Broadcast Cancelled!\nCompleted in {time_taken}\n\n"
                    f"Total Users: <code>{total_users}</code>\n"
                    f"Completed: <code>{done} / {total_users}</code>\n"
                    f"Success: <code>{success}</code>"
                )
                return

            sts = await broadcast_messages(int(user['id']), b_msg, pin)
            if sts == "Success":
                success += 1
            elif sts == "Error":
                failed += 1
            done += 1

            # Update progress every 20 users
            if done % 20 == 0:
                btn = [[InlineKeyboardButton('CANCEL', callback_data='broadcast_cancel#users')]]
                await b_sts.edit(
                    f"Broadcast in progress...\n\n"
                    f"Total Users: <code>{total_users}</code>\n"
                    f"Completed: <code>{done} / {total_users}</code>\n"
                    f"Success: <code>{success}</code>",
                    reply_markup=InlineKeyboardMarkup(btn)
                )

        # Final status message
        time_taken = get_readable_time(time.time() - start_time)
        await b_sts.edit(
            f"Broadcast completed.\nCompleted in {time_taken}\n\n"
            f"Total Users: <code>{total_users}</code>\n"
            f"Completed: <code>{done} / {total_users}</code>\n"
            f"Success: <code>{success}</code>"
        )
