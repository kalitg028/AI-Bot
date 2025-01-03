from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from info import *  # Ensure PROMPT and LOG_CHANNEL are defined
from database.fsub import get_fsub  # Ensure get_fsub is defined
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)

responses_dict = {}
user_modes = {}  # Key: (user_id, chat_id), Value: Mode
DEFAULT_MODE = "chatgpt"

@Client.on_message(filters.private & filters.command("ask"))
async def askcmd(client, message):
    await message.reply_text(
        text="**You don't need to use this command here. Ask me directly.\n\nEx:** `Who Is Lord Shiva?`\n**Ok ?? Let's Try 😏**"
    )

@Client.on_message(filters.command("ask") & filters.group)
async def group_ai_reply(client, message):
    # Check if the command has a query
    if len(message.command) == 1:
        return await message.reply_text(
            "⚠️ **Please provide a query after the command.**\n\nExample: `/ask What is AI?`",
            quote=True
        )

    user_id = message.from_user.id
    chat_id = message.chat.id
    mode = user_modes.get((user_id, chat_id), DEFAULT_MODE)  # Default to "chatgpt" mode if not set

    if mode == "chatgpt":
        await handle_chatgpt_mode(client, message)
    elif mode == "gemini":
        await handle_gemini_mode(client, message)

# Command to set AI mode
@Client.on_message(filters.command("mode"))
async def set_mode(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_mode = user_modes.get((user_id, chat_id), DEFAULT_MODE)

    # Generate buttons for mode selection
    buttons = [
        [
            InlineKeyboardButton("• ᴄʜᴀᴛɢᴘᴛ •", callback_data=f"set_mode_chatgpt_{chat_id}"),
            InlineKeyboardButton("• ɢᴇᴍɪɴɪ •", callback_data=f"set_mode_gemini_{chat_id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_text(
        f"Your current mode in this chat is `{current_mode}`.\n\nChoose a mode:",
        reply_markup=reply_markup
    )

# Handle button clicks for mode selection
@Client.on_callback_query(filters.regex(r"set_mode_"))
async def mode_callback(client, callback_query):
    data = callback_query.data.split("_")
    selected_mode = data[2]
    chat_id = int(data[3])  # Extract chat_id from callback data
    user_id = callback_query.from_user.id

    current_mode = user_modes.get((user_id, chat_id), DEFAULT_MODE)

    if selected_mode == current_mode:
        await callback_query.answer("This mode is already in use!", show_alert=True)
    else:
        user_modes[(user_id, chat_id)] = selected_mode
        await callback_query.answer(f"Mode changed to {selected_mode.capitalize()}!", show_alert=True)
        await callback_query.edit_message_text(
            f"Your AI mode in this chat has been set to `{selected_mode}`."
        )

# Handle AI queries based on the selected mode
@Client.on_message(filters.private & filters.text & ~filters.command(["start", "mode", "ask", "search"]))
async def handle_ai_query(client, message):
    if FSUB and not await get_fsub(client, message):
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    mode = user_modes.get((user_id, chat_id), DEFAULT_MODE)

    if mode == "chatgpt":
        await handle_chatgpt_mode(client, message)
    elif mode == "gemini":
        await handle_gemini_mode(client, message)

# Mode 1: ChatGPT API
async def handle_chatgpt_mode(client, message):
    input_text = message.text.strip()
    searching_message = await message.reply_text("🔍 Processing your query...")
    query = f"{PROMPT}, so my question is ({input_text})"
    url = f"https://darkness.ashlynn.workers.dev/chat/?prompt={query}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("successful") == "success" and data.get("status") == 200:
            response_text = data.get("response")
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=f"👤 {message.from_user.mention} (`{message.from_user.id}`)\n\n"
                     f"**Query:** `{input_text}`\n\n**AI Generated Response (ChatGPT):**\n{response_text}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton('Close', callback_data='close')]]
                )
            )
            await searching_message.edit_text(
                f"**{message.from_user.mention},** {response_text}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ʟᴇᴀʀɴ ᴄᴏᴅɪɴɢ 👨‍💻", url="https://techifybots.blogspot.com")]]
                )
            )
        else:
            await searching_message.edit_text("⚠️ Could not fetch a valid response. Please try again later.")
    except Exception as e:
        await searching_message.edit_text("⚠️ An error occurred while processing your query. Please try again later.")
        print(f"Error in ChatGPT Mode: {e}")

# Mode 2: Gemini AI
async def handle_gemini_mode(client, message):
    user_input = message.text.strip()
    s = await message.reply_sticker("CAACAgQAAxkBAAIFqGc04PwJshM42NKq2lOFn-q5lQtqAAJuDwAC4eqxUNoxB5joJxGiHgQ")

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    try:
        prompt_parts = [user_input]
        response = model.generate_content(prompt_parts)

        if hasattr(response, 'text') and response.text:
            await client.send_message(
                LOG_CHANNEL,
                text=f"👤 {message.from_user.mention} (`{message.from_user.id}`)\n\n"
                     f"**Query:** `{user_input}`\n\n**AI Generated Response (Gemini):**\n{response.text}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton('Close', callback_data='close')]]
                )
            )
            await message.reply_text(
                f"**{message.from_user.mention},** {response.text}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ʟᴇᴀʀɴ ᴄᴏᴅɪɴɢ 👨‍💻", url="https://techifybots.blogspot.com")]]
                )
            )
        else:
            await message.reply_text("⚠️ The AI model couldn't generate a response. Please try again.")
    except Exception as e:
        await message.reply_text("⚠️ An error occurred while processing your query. Please try again.")
        print(f"Error in Gemini Mode: {e}")
    finally:
        await s.delete()
