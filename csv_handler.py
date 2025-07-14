# csv_handler.py
import csv
import os
from datetime import datetime
from config import HABIT_LIST_FILE, HABIT_TRACKING_FILE
from github_synch import create_github_sync, GitHubCSVSync

# Global GitHub sync instances
github_sync_habits = None
github_sync_tracking = None

def init_github_sync():
    """Initialize GitHub synchronization for both CSV files if environment variables are set."""
    global github_sync_habits, github_sync_tracking
    
    # Get GitHub configuration
    from github_synch import get_github_config
    config = get_github_config()
    
    if not all([config["repo_owner"], config["repo_name"], config["github_token"]]):
        print("📁 Using local file storage only")
        return
    
    # Create sync instance for habit_list.csv
    github_sync_habits = GitHubCSVSync(
        repo_owner=config["repo_owner"],
        repo_name=config["repo_name"],
        file_path=config["file_path"],
        github_token=config["github_token"],
        branch=config["branch"]
    )
    
    # Create sync instance for habit_tracking.csv
    tracking_file_path = os.getenv("GITHUB_FILE_PATH_TRACKING", "data/habit_tracking.csv")
    github_sync_tracking = GitHubCSVSync(
        repo_owner=config["repo_owner"],
        repo_name=config["repo_name"],
        file_path=tracking_file_path,
        github_token=config["github_token"],
        branch=config["branch"]
    )
    
    print("🔗 GitHub synchronization enabled for both CSV files")
    
    # Sync both files from GitHub on startup
    github_sync_habits.sync_from_github(HABIT_LIST_FILE)
    github_sync_tracking.sync_from_github(HABIT_TRACKING_FILE)

def save_user_habits(user_id, habits):
    """Save user's habits to habit_list.csv"""
    # Create file with headers if it doesn't exist
    if not os.path.exists(HABIT_LIST_FILE):
        with open(HABIT_LIST_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'habit'])
    
    # Read existing data
    existing_data = []
    if os.path.exists(HABIT_LIST_FILE):
        with open(HABIT_LIST_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
    
    # Remove existing habits for this user
    existing_data = [row for row in existing_data if row['user_id'] != str(user_id)]
    
    # Add new habits for this user
    for habit in habits:
        existing_data.append({'user_id': str(user_id), 'habit': habit})
    
    # Write back to file
    with open(HABIT_LIST_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['user_id', 'habit'])
        writer.writeheader()
        writer.writerows(existing_data)
    
    # Sync to GitHub if enabled
    if github_sync_habits:
        github_sync_habits.sync_to_github(HABIT_LIST_FILE)

def get_user_habits(user_id):
    """Get user's habits from habit_list.csv"""
    if not os.path.exists(HABIT_LIST_FILE):
        return []
    
    habits = []
    with open(HABIT_LIST_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] == str(user_id):
                habits.append(row['habit'])
    
    return habits

def append_checkin(date, user_id, habit, status):
    """Append a habit check-in to habit_tracking.csv"""
    # Create file with headers if it doesn't exist
    if not os.path.exists(HABIT_TRACKING_FILE):
        with open(HABIT_TRACKING_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'user_id', 'habit', 'status'])
    
    # Read existing data to check for duplicates
    existing_data = []
    if os.path.exists(HABIT_TRACKING_FILE):
        with open(HABIT_TRACKING_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
    
    # Check if this check-in already exists
    user_id_str = str(user_id)
    for row in existing_data:
        if (row['date'] == date and 
            row['user_id'] == user_id_str and 
            row['habit'] == habit):
            # Update existing check-in
            row['status'] = status
            break
    else:
        # Add new check-in
        existing_data.append({
            'date': date,
            'user_id': user_id_str,
            'habit': habit,
            'status': status
        })
    
    # Write back to file
    with open(HABIT_TRACKING_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'user_id', 'habit', 'status'])
        writer.writeheader()
        writer.writerows(existing_data)
    
    # Sync to GitHub if enabled
    if github_sync_tracking:
        github_sync_tracking.sync_to_github(HABIT_TRACKING_FILE)

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

def sync_habits_from_github():
    """Sync habit_list.csv from GitHub repository."""
    if github_sync_habits:
        return github_sync_habits.sync_from_github(HABIT_LIST_FILE)
    return False

def sync_habits_to_github():
    """Sync habit_list.csv to GitHub repository."""
    if github_sync_habits:
        return github_sync_habits.sync_to_github(HABIT_LIST_FILE)
    return False

def sync_tracking_from_github():
    """Sync habit_tracking.csv from GitHub repository."""
    if github_sync_tracking:
        return github_sync_tracking.sync_from_github(HABIT_TRACKING_FILE)
    return False

def sync_tracking_to_github():
    """Sync habit_tracking.csv to GitHub repository."""
    if github_sync_tracking:
        return github_sync_tracking.sync_to_github(HABIT_TRACKING_FILE)
    return False

def sync_all_from_github():
    """Sync both CSV files from GitHub repository."""
    habits_success = sync_habits_from_github()
    tracking_success = sync_tracking_from_github()
    return habits_success and tracking_success

def sync_all_to_github():
    """Sync both CSV files to GitHub repository."""
    habits_success = sync_habits_to_github()
    tracking_success = sync_tracking_to_github()
    return habits_success and tracking_success

def get_user_stats(user_id):
    """Get statistics for a user's habits"""
    if not os.path.exists(HABIT_TRACKING_FILE):
        return {}
    
    stats = {}
    with open(HABIT_TRACKING_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] == str(user_id):
                habit = row['habit']
                status = row['status']
                
                if habit not in stats:
                    stats[habit] = {'total': 0, 'completed': 0}
                
                stats[habit]['total'] += 1
                if status == '✅':
                    stats[habit]['completed'] += 1
    
    return stats 