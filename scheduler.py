# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from handlers import send_daily_checkin
from config import DAILY_CHECKIN_TIME

def start_scheduler(updater):
    """Start the daily check-in scheduler (sync version)"""
    scheduler = BackgroundScheduler()
    hour, minute = DAILY_CHECKIN_TIME.split(':')
    scheduler.add_job(
        send_daily_checkin,
        trigger=CronTrigger(hour=int(hour), minute=int(minute)),
        args=[updater.job_queue._dispatcher.context],
        id='daily_checkin',
        name='Send daily habit check-in to all users',
        replace_existing=True
    )
    scheduler.start()
    print(f"✅ Scheduler started - Daily check-ins scheduled for {DAILY_CHECKIN_TIME}")
    return scheduler

def stop_scheduler(scheduler):
    if scheduler:
        scheduler.shutdown()
        print("🛑 Scheduler stopped") 