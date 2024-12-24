import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, CallbackContext, filters
from telegram.error import TelegramError
import logging

# Replace this with your bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Enable logging for debugging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app (for web service requirements)
app = Flask(__name__)

# 1. Approve and greet the user personally with advanced customizations
async def approve_and_greet_user(update: Update, context: CallbackContext):
    try:
        # Extract user ID and approve their join request
        user_id = update.chat_join_request.from_user.id
        chat_id = update.chat_join_request.chat.id

        # Approve the user's join request
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)

        # Compose the greeting message with HTML, emojis, and design
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

        # Send the message directly to the user with HTML formatting
        await context.bot.send_message(chat_id=user_id, text=greeting_message, parse_mode="HTML")

        print(f"Greeted user {update.chat_join_request.from_user.first_name} personally.")
    except TelegramError as e:
        print(f"Error: {e.message}")

# 2. Send a personal farewell message for users who leave with HTML and emojis
async def farewell_user(update: Update, context: CallbackContext):
    user = update.message.left_chat_member
    if user:
        farewell_message = (
            f"<b><i>👋 Goodbye, {user.first_name}!</i></b>\n"
            "<i>We’ll miss you 😢</i>\n\n"
            "<b>❤️ We hope to see you again soon!</b>\n"
            "<b>✨ <i>Stay awesome, and good luck with everything!</i></b>"
        )
        # Send the farewell message to the user's private chat with HTML formatting
        try:
            await context.bot.send_message(chat_id=user.id, text=farewell_message, parse_mode="HTML")
            print(f"Farewell message sent to {user.first_name} personally.")
        except TelegramError as e:
            print(f"Error sending farewell: {e.message}")

# Flask route (to meet platform port binding requirements)
@app.route('/')
def webhook():
    return "Bot is running"

# Main function
def main():
    # Create the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers for the bot actions
    application.add_handler(ChatJoinRequestHandler(approve_and_greet_user))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, farewell_user))

    # Start the bot using polling (this is the part that gets the updates)
    application.run_polling()

    # Run Flask web server on the platform's provided port (e.g., Render requires this)
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
