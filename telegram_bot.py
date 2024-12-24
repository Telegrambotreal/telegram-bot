import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, filters, CallbackContext
from telegram.error import TelegramError

# Load the bot token from the environment variable
BOT_TOKEN = "7743886736:AAEsIRP5Q9yUedoZ0Hmr8AhtpZRQovq1ZW8"
if not BOT_TOKEN:
    raise ValueError("Missing BOT_TOKEN environment variable")

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram application
application = Application.builder().token(BOT_TOKEN).build()

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

# Root route for Flask
@app.route('/')
def index():
    return "Hello! The Telegram bot is running.", 200

# Webhook for Telegram updates (optional)
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put(update)
        return "OK", 200

# Main function to start the bot and the Flask app
def main():
    # Add a handler for chat join requests
    application.add_handler(ChatJoinRequestHandler(approve_and_greet_user))

    # Add a handler for users leaving the group
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, farewell_user))

    # Start the bot polling
    print("Bot is running...")
    application.run_polling()

# Entry point for the script
if __name__ == '__main__':
    # Start Flask app in debug mode (use production server in production)
    app.run(host='0.0.0.0', port=10000)
    
    # Optionally run the Telegram bot in polling mode (if not using webhook)
    main()
