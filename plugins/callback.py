from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Script import text
from config import ADMIN

@Client.on_callback_query()
async def callback_query_handler(client, query: CallbackQuery):
    if query.data == "start":
        await query.message.edit_caption(
            caption=text.START.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ℹ️ 𝖠𝖻𝗈𝗎𝗍", callback_data="about"),
                 InlineKeyboardButton("📚 𝖧𝖾𝗅𝗉", callback_data="help")],
                [InlineKeyboardButton("📢 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/Indian_MV")]
            ])
        )

    elif query.data == "help":
        await query.message.edit_caption(
            caption=text.HELP,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 𝖴𝗉𝖽𝖺𝗍𝖾𝗌", url="https://t.me/Indian_MV"),
                 InlineKeyboardButton("💬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍", url="https://t.me/Indian_MV_Group")],
                [InlineKeyboardButton("↩️ 𝖡𝖺𝖼𝗄", callback_data="start"),
                 InlineKeyboardButton("❌ 𝖢𝗅𝗈𝗌𝖾", callback_data="close")]
            ])
        )

    elif query.data == "about":
        await query.message.edit_caption(
            caption=text.ABOUT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👨‍💻 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋 👨‍💻", url="https://t.me/Indian_MV_Admin_Bot")],
                [InlineKeyboardButton("↩️ 𝖡𝖺𝖼𝗄", callback_data="start"),
                 InlineKeyboardButton("❌ 𝖢𝗅𝗈𝗌𝖾", callback_data="close")]
            ])
        )

    elif query.data == "close":
        await query.message.delete()

