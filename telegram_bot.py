import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, CallbackContext, filters
from telegram.error import TelegramError
import logging

# Replace this with your bot token from BotFather
BOT_TOKEN = "7743886736:AAEsIRP5Q9yUedoZ0Hmr8AhtpZRQovq1ZW8"

# Enable logging for debugging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app (for web service requirements)
app = Flask(__name__)

# Function to approve and greet the user
async def approve_and_greet_user(update: Update, context: CallbackContext):
    try:
        user_id = update.chat_join_request.from_user.id
        chat_id = update.chat_join_request.chat.id
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
        
        greeting_message = (
            "<b><i>🎉 <u>Hey Official</u>, Welcome To The Bot!</i></b>\n\n"
            "<b>🌟 You’re Just One Step Away From Unlocking Awesome Rewards!</b>\n\n"
            "👇 Must Join All Channels To Get Your Free Rewards 👇\n\n"
            "💸 <b>🔥 Free Paytm Cash 💵 is waiting for you!</b>\n\n"
            "✅ <a href='https://t.me/+7d9wtMM_z2ZiY2Jl'><b>Join Channel 1</b></a>\n"
            "✅ <a href='https://t.me/+pw4k7DWYQUNhNTY9'><b>Join Channel 2</b></a>\n"
            "✅️ <a href='https://t.me/+7NZs15XeGPEyYmRl'><b>Join Channel 3</b></a>\n"
            "✅️ <a href='https://t.me/+e2dzSK3Keto4Yzdl'><b>Join Channel 4</b></a>\n"
            "✅️ <a href='https://t.me/+NU95RnXUCipiNGE9'><b>Join Channel 5</b></a>\n"
            "✅️ <a href='https://t.me/+i0LNH4IWMKw1NDdl'><b>Join Channel 6</b></a>\n\n"
            "<b>💖 <i>With ❤️ by <a href='https://t.me/Dmdsofficial'>@DmdsOfficial</a></i></b>\n\n"
            "<b><i>✨ Stay connected and enjoy the best deals! ✨</i></b>"
        )
        
        await context.bot.send_message(chat_id=user_id, text=greeting_message, parse_mode="HTML")
    except TelegramError as e:
        logger.error(f"Error: {e.message}")

# Function for farewell message
async def farewell_user(update: Update, context: CallbackContext):
    user = update.message.left_chat_member
    if user:
        farewell_message = (
            f"<b><i>👋 Goodbye, {user.first_name}!</i></b>\n"
            "<i>We’ll miss you 😢</i>\n\n"
            "<b>❤️ We hope to see you again soon!</b>\n"
            "<b>✨ <i>Stay awesome, and good luck with everything!</i></b>"
        )
        try:
            await context.bot.send_message(chat_id=user.id, text=farewell_message, parse_mode="HTML")
        except TelegramError as e:
            logger.error(f"Error sending farewell: {e.message}")

# Flask route (to meet platform port binding requirements)
@app.route('/')
def webhook():
    return "Bot is running"

# Main function
def main():
    # Create the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for bot actions
    application.add_handler(ChatJoinRequestHandler(approve_and_greet_user))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, farewell_user))

    # Start the bot using polling in the background
    application.run_polling()

    # Run the Flask web server (for handling the platform's port requirements)
    port = int(os.getenv("PORT", 5000))  # Render provides the PORT environment variable
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
