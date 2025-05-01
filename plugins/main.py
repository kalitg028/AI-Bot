from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from config import *
import google.generativeai as genai
import asyncio

genai.configure(api_key=GOOGLE_API_KEY)

responses_dict = {}

@Client.on_message(filters.private & filters.command("ask"))
async def askcmd(client, message):
    await message.reply_text(
        text="**You don't need to use this command here. Ask me directly.\n\nEx:** `Who Is Lord Shiva?`\n**Ok ?? Let's Try 😏**"
    )

@Client.on_message(filters.command("ask") & filters.group)
async def group_ai_reply(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "⚠️ **Please provide a query after the command.**\n\nExample: `/ask What is AI?`",
            quote=True
        )
    await handle_gemini_mode(client, message)

@Client.on_message(filters.private & filters.text & ~filters.command(["start", "ask"]))
async def handle_ai_query(client, message):
    await handle_gemini_mode(client, message)

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
        model_name="gemini-1.5-pro",
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
            ai_message = await message.reply_text(
                f"**{message.from_user.mention},** {response.text}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ʟᴇᴀʀɴ ᴄᴏᴅɪɴɢ 👨‍💻", url="https://techifybots.blogspot.com")]]
                )
            )

            # Delete the sticker immediately after the bot sends the message
            await s.delete()

            # Wait for 5 minutes before deleting both the user and bot messages
            await asyncio.sleep(300)  # Sleep for 5 minutes (300 seconds)
            await message.delete()  # Delete the user's message
            await ai_message.delete()  # Delete the bot's reply

        else:
            await message.reply_text("⚠️ The AI model couldn't generate a response. Please try again.")
    except Exception as e:
        await message.reply_text("⚠️ An error occurred while processing your query. Please try again.")
        print(f"Error in Gemini Mode: {e}")
