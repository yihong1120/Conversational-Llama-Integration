from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext, ContextTypes, Updater
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
def init_telegram_bot(handle_ai_conversation):
    # 使用 builder 方法初始化 Application 并设置 token
    application = Application.builder().token(TOKEN).build()

    # 在 Application 的 bot_data 中存储 handle_ai_conversation 函数
    application.bot_data['handle_conversation'] = handle_ai_conversation

    # 将消息处理函数添加到 Application
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # 开始轮询
    application.run_polling()

# Example usage
if __name__ == '__main__':
    pass
