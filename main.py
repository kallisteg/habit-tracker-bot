# main.py
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TELEGRAM_TOKEN
from handlers import start_command, handle_habit_input, help_command, send_daily_checkin, stats_command, sync_command
from csv_handler import init_github_sync
from datetime import time
import pytz

if not TELEGRAM_TOKEN: #if token is missing
    raise ValueError("TELEGRAM_TOKEN environment variable is missing.") # raise in python triggers exceptions.
# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    print("🤖 Starting Habit Tracker Bot...")
    
    # Initialize GitHub synchronization
    init_github_sync()
    
    # Create updater and dispatcher
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Add command handlers
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("stats", stats_command))
    dp.add_handler(CommandHandler("sync", sync_command))
    
    # Add message handler for habit input and check-in responses
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_habit_input))
    
    # Schedule daily check-in using JobQueue
    tz = pytz.timezone("America/Toronto")
    updater.job_queue.run_daily(
        send_daily_checkin,
        time=time(hour=8, minute=0, tzinfo=tz),
        name="Send daily habit check-in to all users",
        context=updater.bot,
    )
    
    try:
        print("🚀 Bot is starting...")
        print("📱 Send /start to begin tracking your habits!")
        print("⏰ Daily check-ins will be sent at 8:00 AM Toronto time")

        # Start the bot
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down bot...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 