from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext, ContextTypes
from src.utils.config import TELEGRAM_PARAMS

# Get Telegram token from environment variable
TOKEN = TELEGRAM_PARAMS['telegram_token']

# Initialise message handler
async def message_handler(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Call handle_conversation function from bot_data
    response = context.bot_data['handle_conversation'](str(chat_id), user_message)

    await context.bot.send_message(chat_id=chat_id, text=response)

# Initialise Telegram bot
def init_telegram_bot(handle_conversation):
    application = Application.builder().token(TOKEN).build()

    # Store handle_conversation function in bot_data
    ContextTypes.bot_data['handle_conversation'] = handle_conversation

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    application.run_polling()

# Example usage
if __name__ == '__main__':
    pass
