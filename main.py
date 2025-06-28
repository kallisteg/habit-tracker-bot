# main.py
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TELEGRAM_TOKEN
from handlers import start_command, handle_habit_input, help_command
from scheduler import start_scheduler, stop_scheduler

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    print("🤖 Starting Habit Tracker Bot...")
    
    # Create updater and dispatcher
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Add command handlers
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    
    # Add message handler for habit input and check-in responses
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_habit_input))
    
    # Start the scheduler
    scheduler = start_scheduler(updater)
    
    try:
        print("🚀 Bot is starting...")
        print("📱 Send /start to begin tracking your habits!")
        print("⏰ Daily check-ins will be sent at 8:00 AM")
        
        # Start the bot
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down bot...")
        stop_scheduler(scheduler)
    except Exception as e:
        print(f"❌ Error: {e}")
        stop_scheduler(scheduler)

if __name__ == "__main__":
    main() 