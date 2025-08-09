import os
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import asyncio

# --- Bot Configuration ---
TELEGRAM_BOT_TOKEN = "7990385015:AAGw1Xe03ltLi_aLg7FiOKc_Kl0kHFySeeM"
GEMINI_API_KEY = "AIzaSyDLLUpqxNecGINHCz43Bi7ma1JUP9NmNKE"

# Configure the Gemini API with your key.
genai.configure(api_key=GEMINI_API_KEY)
# FIX: Change the model name from 'gemini-pro' to 'gemini-1.5-flash'.
model = genai.GenerativeModel('gemini-1.5-flash')

# Dictionary to store chat history for each user.
chat_sessions = {}

# --- Command Handlers ---

async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    chat_sessions[user_id] = model.start_chat(history=[])
    
    welcome_message = (
        f'Hello there! I am Lumina AI Lite ✨, a bot powered by Gemini AI. '
        'I am ready to chat with you. How can I help? 😊'
    )
    await update.message.reply_text(welcome_message)

async def new_chat(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    chat_sessions[user_id] = model.start_chat(history=[])
    
    await update.message.reply_text('New chat session started! Let’s begin. 💬')

# --- Improved Message Handler ---

async def handle_message(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text
    
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=telegram.constants.ChatAction.TYPING
    )
    
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    try:
        response = chat_sessions[user_id].send_message(user_message)
        
        ai_response = response.text + '💡'
        
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        await update.message.reply_text("I'm sorry, I'm having a little trouble right now. Please try again in a moment. 🤖")

# --- Main Function ---

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("new_chat", new_chat))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Lumina AI Lite bot is running... 🚀")
    application.run_polling()

if __name__ == '__main__':
    main()