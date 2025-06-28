# handlers.py
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from csv_handler import save_user_habits, get_user_habits, append_checkin, has_checkin_today
from quotes import get_random_quote
from config import POSITIVE_RESPONSES, NEGATIVE_RESPONSES
from datetime import datetime
import re

# Store user states
user_states = {}

def start_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    welcome_message = f"Hello {user_name}! 👋\n\nI'm your Habit Tracker Bot! 🎯\n\n"
    welcome_message += "I'll help you track your daily habits and send you motivational reminders.\n\n"
    welcome_message += "Please send me your habits separated by commas.\n"
    welcome_message += "For example: workout, drink water, read 30 minutes, meditate"
    
    update.message.reply_text(welcome_message)
    user_states[user_id] = "waiting_for_habits"

def handle_habit_input(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_text = update.message.text.strip()
    
    if user_id not in user_states or user_states[user_id] != "waiting_for_habits":
        handle_checkin_response(update, context)
        return
    
    habits = [habit.strip() for habit in user_text.split(',') if habit.strip()]
    if not habits:
        update.message.reply_text("Please provide at least one habit. Try again:")
        return
    habits_str = ', '.join(habits)
    save_user_habits(user_id, habits_str)
    del user_states[user_id]
    confirm_message = f"Perfect! I've saved your {len(habits)} habit(s):\n\n"
    for i, habit in enumerate(habits, 1):
        confirm_message += f"{i}. {habit}\n"
    confirm_message += "\nI'll send you daily check-ins at 8:00 AM with motivational quotes! 🌅\n"
    confirm_message += "You can reply with ✅/❌ or yes/no for each habit."
    update.message.reply_text(confirm_message)

def send_daily_checkin(context: CallbackContext):
    from csv_handler import get_all_users
    user_ids = get_all_users()
    today = datetime.now().strftime("%Y-%m-%d")
    for user_id in user_ids:
        if has_checkin_today(user_id, today):
            continue
        habits = get_user_habits(user_id)
        if not habits:
            continue
        quote = get_random_quote()
        message = f"🌅 Good morning! Time for your daily habit check-in!\n\n"
        message += f"💭 {quote}\n\n"
        message += "📋 Your habits for today:\n"
        for i, habit in enumerate(habits, 1):
            message += f"{i}. {habit}\n"
        message += "\nReply with your status for each habit:\n"
        message += "✅ = Completed\n❌ = Missed\n\n"
        message += "Example: ✅✅❌ (for 3 habits)"
        keyboard = [
            ["✅✅✅", "✅✅❌", "✅❌✅", "✅❌❌"],
            ["❌✅✅", "❌✅❌", "❌❌✅", "❌❌❌"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        try:
            context.bot.send_message(
                chat_id=user_id,
                text=message,
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")

def handle_checkin_response(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_text = update.message.text.strip()
    today = datetime.now().strftime("%Y-%m-%d")
    habits = get_user_habits(user_id)
    if not habits:
        update.message.reply_text("You haven't set up your habits yet. Use /start to begin!")
        return
    if has_checkin_today(user_id, today):
        update.message.reply_text("You've already checked in today! See you tomorrow! 😊")
        return
    response_chars = list(user_text.lower())
    status_emojis = []
    for char in response_chars:
        if char in ['✅', 'y', '1', 't'] or 'yes' in char:
            status_emojis.append('✅')
        elif char in ['❌', 'n', '0', 'f'] or 'no' in char:
            status_emojis.append('❌')
    if len(status_emojis) != len(habits):
        update.message.reply_text(
            f"Please provide status for all {len(habits)} habits.\n"
            f"Example: {'✅' * len(habits)} or {'❌' * len(habits)}"
        )
        return
    for habit, status in zip(habits, status_emojis):
        append_checkin(today, user_id, habit, status)
    completed = status_emojis.count('✅')
    total = len(habits)
    completion_rate = (completed / total) * 100
    confirmation = f"📊 Daily Check-in Complete!\n\n"
    for i, (habit, status) in enumerate(zip(habits, status_emojis), 1):
        confirmation += f"{i}. {habit}: {status}\n"
    confirmation += f"\n🎯 Completion Rate: {completed}/{total} ({completion_rate:.1f}%)\n\n"
    if completion_rate == 100:
        confirmation += "🎉 Perfect! You completed all your habits today!"
    elif completion_rate >= 80:
        confirmation += "🌟 Great job! You're doing amazing!"
    elif completion_rate >= 60:
        confirmation += "👍 Good progress! Keep it up!"
    else:
        confirmation += "💪 Tomorrow is a new day! Don't give up!"
    update.message.reply_text(
        confirmation,
        reply_markup=ReplyKeyboardRemove()
    )

def help_command(update: Update, context: CallbackContext):
    help_text = """
🤖 Habit Tracker Bot Commands:

/start - Set up your habits
/help - Show this help message

📋 How it works:
1. Use /start to set your habits
2. Receive daily check-ins at 8:00 AM
3. Reply with ✅/❌ for each habit
4. Track your progress over time

💡 Tips:
- You can reply with emojis: ✅✅❌
- Or use text: yes yes no
- Or use numbers: 1 1 0

📊 Your data is stored locally in CSV files.
"""
    update.message.reply_text(help_text) 