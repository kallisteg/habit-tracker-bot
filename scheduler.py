# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from handlers import send_daily_checkin
from config import DAILY_CHECKIN_TIME
import pytz

def start_scheduler(updater):
    """Start the daily check-in scheduler (sync version)"""
    scheduler = BackgroundScheduler(timezone=pytz.UTC)
    hour, minute = DAILY_CHECKIN_TIME.split(':')
    
    # Create a wrapper function that gets the bot from the updater
    def send_checkin_job():
        # Create a mock context with the bot
        class MockContext:
            def __init__(self, bot):
                self.bot = bot
        
        context = MockContext(updater.bot)
        send_daily_checkin(context)
    
    scheduler.add_job(
        send_checkin_job,
        trigger=CronTrigger(hour=int(hour), minute=int(minute), timezone=pytz.UTC),
        id='daily_checkin',
        name='Send daily habit check-in to all users',
        replace_existing=True
    )
    scheduler.start()
    print(f"✅ Scheduler started - Daily check-ins scheduled for {DAILY_CHECKIN_TIME} UTC")
    return scheduler

def stop_scheduler(scheduler):
    if scheduler:
        scheduler.shutdown()
        print("🛑 Scheduler stopped") 