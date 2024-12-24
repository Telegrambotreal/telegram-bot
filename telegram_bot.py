import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.ext import MessageHandler, filters
from telegram.ext import Updater

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the command handler function
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm your bot. How can I assist you today?")

# Define the main function to set up the bot and webhook
async def main():
    # Create an application with your bot's token
    application = Application.builder().token("7743886736:AAEsIRP5Q9yUedoZ0Hmr8AhtpZRQovq1ZW8").build()

    # Add handlers (you can add more commands or message handlers here)
    application.add_handler(CommandHandler("start", start))

    # Set the webhook URL (use your actual webhook URL here)
    WEBHOOK_URL = os.getenv("https://telegram-bot-ylm5.onrender.com")  # Ensure the webhook URL is correctly set in your environment variables
    if WEBHOOK_URL is None:
        raise ValueError("WEBHOOK_URL environment variable is not set!")

    # Set webhook using the async set_webhook method
    await application.bot.set_webhook(url=WEBHOOK_URL)

    # Start the webhook listener (listening on port 5000 or the port specified in environment)
    application.run_webhook(listen="0.0.0.0", port=os.environ.get('PORT', 5000), url_path="webhook")

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())
