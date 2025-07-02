# csv_handler.py
import csv
import os
from datetime import datetime
from config import HABIT_LIST_FILE, HABIT_TRACKING_FILE
from github_synch import create_github_sync

# Global GitHub sync instance
github_sync = None

def init_github_sync():
    """Initialize GitHub synchronization if environment variables are set."""
    global github_sync
    github_sync = create_github_sync()
    if github_sync:
        print("🔗 GitHub synchronization enabled")
        # Sync from GitHub on startup
        github_sync.sync_from_github(HABIT_LIST_FILE)
    else:
        print("📁 Using local file storage only")

def save_user_habits(user_id, habits):
    """Save user's habits to habit_list.csv"""
    # Create file with headers if it doesn't exist
    if not os.path.exists(HABIT_LIST_FILE):
        with open(HABIT_LIST_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'habits'])
    
    # Read existing data
    existing_data = []
    if os.path.exists(HABIT_LIST_FILE):
        with open(HABIT_LIST_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
    
    # Update or add user habits
    user_found = False
    for row in existing_data:
        if row['user_id'] == str(user_id):
            row['habits'] = habits
            user_found = True
            break
    
    if not user_found:
        existing_data.append({'user_id': str(user_id), 'habits': habits})
    
    # Write back to file
    with open(HABIT_LIST_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['user_id', 'habits'])
        writer.writeheader()
        writer.writerows(existing_data)
    
    # Sync to GitHub if enabled
    if github_sync:
        github_sync.sync_to_github(HABIT_LIST_FILE)

def get_user_habits(user_id):
    """Get user's habits from habit_list.csv"""
    if not os.path.exists(HABIT_LIST_FILE):
        return []
    
    with open(HABIT_LIST_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] == str(user_id):
                habits_str = row['habits']
                return [habit.strip() for habit in habits_str.split(',') if habit.strip()]
    
    return []

def append_checkin(date, user_id, habit, status):
    """Append a habit check-in to habit_tracking.csv"""
    # Create file with headers if it doesn't exist
    if not os.path.exists(HABIT_TRACKING_FILE):
        with open(HABIT_TRACKING_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'user_id', 'habit', 'status'])
    
    # Append the check-in
    with open(HABIT_TRACKING_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, user_id, habit, status])

def get_all_users():
    """Get all user IDs from habit_list.csv"""
    if not os.path.exists(HABIT_LIST_FILE):
        return []
    
    user_ids = []
    with open(HABIT_LIST_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_ids.append(int(row['user_id']))
    
    return user_ids

def has_checkin_today(user_id, date):
    """Check if user has already checked in today"""
    if not os.path.exists(HABIT_TRACKING_FILE):
        return False
    
    with open(HABIT_TRACKING_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] == str(user_id) and row['date'] == date:
                return True
    
    return False

def sync_from_github():
    """Sync habit_list.csv from GitHub repository."""
    if github_sync:
        return github_sync.sync_from_github(HABIT_LIST_FILE)
    return False

def sync_to_github():
    """Sync habit_list.csv to GitHub repository."""
    if github_sync:
        return github_sync.sync_to_github(HABIT_LIST_FILE)
    return False 