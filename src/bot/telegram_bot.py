import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Get Telegram token from environment variable
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Initialise message handler
async def message_handler(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Process message
    response = context.user_data['handle_conversation'](str(chat_id), user_message)
    
    # Send response
    await context.bot.send_message(chat_id=chat_id, text=response)

# Initialise Telegram bot
def init_telegram_bot(handle_conversation):
    application = Application.builder().token(TOKEN).build()
    
    # Set user data
    application.user_data['handle_conversation'] = handle_conversation

    # Set message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Start polling
    application.run_polling()

# Example usage
if __name__ == '__main__':
    pass
