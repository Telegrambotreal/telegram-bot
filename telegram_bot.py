from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, CallbackContext, filters
from telegram.error import TelegramError
import os

# Replace this with your bot token from BotFather
BOT_TOKEN = "7743886736:AAEsIRP5Q9yUedoZ0Hmr8AhtpZRQovq1ZW8"

# Replace with your webhook URL (Render or your service's URL)
WEBHOOK_URL = "https://telegram-bot-t8hp.onrender.com/webhook"

# 1. Approve and greet the user personally with advanced customizations
async def approve_and_greet_user(update: Update, context: CallbackContext):
    try:
        user_id = update.chat_join_request.from_user.id
        chat_id = update.chat_join_request.chat.id

        # Approve the user's join request
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)

        # Compose the greeting message
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
        try:
            await context.bot.send_message(chat_id=user.id, text=farewell_message, parse_mode="HTML")
            print(f"Farewell message sent to {user.first_name} personally.")
        except TelegramError as e:
            print(f"Error sending farewell: {e.message}")

# Main function to configure the bot and set up webhook
def main():
    # Create the Application with the bot token
    application = Application.builder().token(BOT_TOKEN).build()

    # Add a handler for chat join requests
    application.add_handler(ChatJoinRequestHandler(approve_and_greet_user))

    # Add a handler for users leaving the group
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, farewell_user))

    # Set up the webhook for your cloud service
    application.bot.set_webhook(url=WEBHOOK_URL)

    # Start the bot (using webhook instead of polling)
    print("Bot is running with webhook...")
    application.run_webhook(listen="0.0.0.0", port=os.environ.get('PORT', 5000), url_path="webhook")

# Entry point for the script
if __name__ == "__main__":
    main()
