# from src.bot.line_bot import init_line_bot
from src.bot.telegram_bot import init_telegram_bot
from src.model.conversation_model import ConversationHandler as AIConversationHandler

# Initialise AI model
ai_handler = AIConversationHandler("models/llama2/firefly-llama2-13b-chat.Q8_0.gguf")

# Define function to handle AI conversation
def handle_ai_conversation(user_id: str, message: str) -> str:
    response = ai_handler.handle_conversation(user_id, message)
    return response

def main():
    # Initialise bots
    # init_line_bot()
    init_telegram_bot(handle_ai_conversation)

    # Your application code here
    print("Bots are running...")

if __name__ == "__main__":
    main()
