from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from telegram.error import TimedOut, NetworkError, BadRequest
from src.utils.config import TELEGRAM_PARAMS, PROMPT_PARAMS

# Telegram bot token
TOKEN = TELEGRAM_PARAMS['telegram_token']

# Define the message handler
async def message_handler(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id

    # if user sends /start, send welcome message
    if user_message == "/start":
        welcome_message = PROMPT_PARAMS["welcome_message"]
        await context.bot.send_message(chat_id=chat_id, text=welcome_message)
        return
    
    # if user sends /help, send help message
    elif user_message == "/help":
        help_message = PROMPT_PARAMS["help_message"]
        await context.bot.send_message(chat_id=chat_id, text=help_message)
        return
    
    # if user sends /goodbye, send goodbye message
    elif user_message == "/goodbye":
        goodbye_message = PROMPT_PARAMS["goodbye_message"]
        await context.bot.send_message(chat_id=chat_id, text=goodbye_message)
        return
    
    # Process the user message
    try:
        # Call the handle_conversation function to generate a response
        response = context.bot_data['handle_conversation'](str(chat_id), user_message)
        # Send the response to the user
        await context.bot.send_message(chat_id=chat_id, text=response)

    # Handle timeout exceptions
    except TimedOut:
        # Send a message if the request times out
        await context.bot.send_message(chat_id=chat_id, text="請求超時，請稍後再試。")

    # Handle network exceptions
    except NetworkError:
        # Send a message if there is a network error
        await context.bot.send_message(chat_id=chat_id, text="網絡錯誤，請稍後再試。")

    # Handle bad request exceptions
    except BadRequest:
        # Send a message if there is a bad request
        await context.bot.send_message(chat_id=chat_id, text="請求錯誤，請稍後再試。")

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
