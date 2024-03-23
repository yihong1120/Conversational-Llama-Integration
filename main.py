from src.bot.line_bot import init_line_bot
from src.bot.telegram_bot import init_telegram_bot

def main():
    # Initialise bots
    init_line_bot()
    init_telegram_bot()

    # Your application code here
    print("Bots are running...")

if __name__ == "__main__":
    main()
