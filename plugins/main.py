from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import *
from database.fsub import get_fsub
from database.users import db

@Client.on_message(filters.private & filters.command("start"))
async def startcmd(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(
            chat_id=LOG_CHANNEL, 
            text=f"**#NewUser\n\n👤 {message.from_user.mention}** (`{message.from_user.id}`)"
        )

    if FSUB and not await get_fsub(client, message):
        return

    welcome_message = (
        f"**{message.from_user.mention},\n\n"
        "Welcome to AI Neura Bot – your advanced AI chatbot.\n\n"
        "I’m here to help you with anything you need.\n\n"
        "__Click on 'Help' for more details and discover what I can do for you!__**"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="about"),
         InlineKeyboardButton("• ʜᴇʟᴘ •", callback_data="help")],
        [InlineKeyboardButton("♻ ᴅᴇᴠᴇʟᴏᴘᴇʀ ♻", url="https://telegram.me/TechifyRahul")]
    ])

    await client.send_photo(
        chat_id=message.chat.id, 
        photo="https://envs.sh/5e1.jpg", 
        caption=welcome_message, 
        reply_markup=keyboard
    )

@Client.on_callback_query()
async def handle_button_click(client, callback_query):
    data = callback_query.data

    if data == "help":
        help_message = (
            "**✨ --ᴜsᴇs ᴏꜰ ᴄᴏᴍᴍᴀɴᴅs--\n\n• /ask - ɪꜰ ʏᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ ɪɴ ɢʀᴏᴜᴘ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴀsᴋ ᴀɴʏᴛʜɪɴɢ\n\nᴇx: `/ask what is AI?`\n\nɴᴏᴛᴇ : ɪɴ ᴘʀɪᴠᴀᴛᴇ ʏᴏᴜ ᴅᴏɴ'ᴛ ɴᴇᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs\n\n• /mode - ᴄʜᴏᴏsᴇ ʏᴏᴜʀ ᴄᴏɴᴠᴇʀsᴀᴛɪᴏɴ sᴛʏʟᴇ**"
        )
        help_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻  ʀᴇᴘᴏ", url="https://github.com/TechifyBots"),
             InlineKeyboardButton("💥  ᴅᴏɴᴀᴛᴇ", callback_data="donate")],
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="start")]
        ])
        await edit_message(client, callback_query, help_message, help_keyboard)

    elif data == "start":
        welcome_message = (
            f"**{callback_query.from_user.mention},\n\n"
            "Welcome to AI Neura Bot – your advanced AI chatbot.\n\n"
            "I’m here to help you with anything you need.\n\n"
            "__Click on 'Help' for more details and discover what I can do for you!__**"
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="about"),
             InlineKeyboardButton("• ʜᴇʟᴘ •", callback_data="help")],
            [InlineKeyboardButton("♻ ᴅᴇᴠᴇʟᴏᴘᴇʀ ♻", url="https://telegram.me/TechifyRahul")]
        ])

        await edit_message(client, callback_query, welcome_message, keyboard)

    elif data == "donate":
        donate_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="help"),
             InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        donate_message = (
            ">❤️‍🔥 𝐓𝐡𝐚𝐧𝐤𝐬 𝐟𝐨𝐫 𝐬𝐡𝐨𝐰𝐢𝐧𝐠 𝐢𝐧𝐭𝐞𝐫𝐞𝐬𝐭 𝐢𝐧 𝐃𝐨𝐧𝐚𝐭𝐢𝐨𝐧\n\n**__💞  ɪꜰ ʏᴏᴜ ʟɪᴋᴇ ᴏᴜʀ ʙᴏᴛ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴅᴏɴᴀᴛᴇ ᴀɴʏ ᴀᴍᴏᴜɴᴛ ₹𝟷𝟶, ₹𝟸𝟶, ₹𝟻𝟶, ₹𝟷𝟶𝟶, ᴇᴛᴄ.__**\n\n❣️ 𝐷𝑜𝑛𝑎𝑡𝑖𝑜𝑛𝑠 𝑎𝑟𝑒 𝑟𝑒𝑎𝑙𝑙𝑦 𝑎𝑝𝑝𝑟𝑒𝑐𝑖𝑎𝑡𝑒𝑑 𝑖𝑡 ℎ𝑒𝑙𝑝𝑠 𝑖𝑛 𝑏𝑜𝑡 𝑑𝑒𝑣𝑒𝑙𝑜𝑝𝑚𝑒𝑛𝑡\n\n💖 𝐔𝐏𝐈 𝐈𝐃 : `TechifyBots@UPI`\n\n💗 𝐐𝐑 𝐂𝐨𝐝𝐞 : **<a href='https://TechifyBots.github.io/Donate'>𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾</a>**"
        )
        await edit_message(client, callback_query, donate_message, donate_keyboard)

    elif data == "close":
        await callback_query.message.delete()

    elif data == "about":
        about_message = (
            "**ᴍʏ ɴᴀᴍᴇ : [ᴀɪ ɴᴇᴜʀᴀ ʙᴏᴛ](https://telegram.me/AINeuraBot)\n"
            "ʜᴏsᴛᴇᴅ ᴏɴ : ᴋᴏʏᴇʙ\n"
            "ᴅᴀᴛᴀʙᴀsᴇ : ᴍᴏɴɢᴏᴅʙ\n"
            "ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ 𝟹\n"
            "ᴍʏ ᴄʀᴇᴀᴛᴏʀ : [ʀᴀʜᴜʟ](https://telegram.me/callownerbot)**"
        )
        about_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data="start"),
             InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        await edit_message(client, callback_query, about_message, about_keyboard)

async def edit_message(client, callback_query, caption, reply_markup):
    try:
        await callback_query.message.edit_caption(caption=caption, reply_markup=reply_markup)
    except Exception as e:
        print("Error editing message caption:", e)

    await client.answer_callback_query(callback_query.id)

@Client.on_message(filters.group & filters.command("start"))
async def techifybots(client, message):
    await message.reply_text(text="Hy,\n\nHow can I assist you?")
