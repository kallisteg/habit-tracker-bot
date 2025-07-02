# 🤖 Telegram Habit Tracker Bot

A Python-based Telegram bot that helps users track their daily habits with motivational quotes and local CSV storage.

## 🎯 Features

- **Daily Habit Check-ins**: Automated reminders at 8:00 AM
- **Motivational Quotes**: Random inspirational quotes with each check-in
- **Flexible Responses**: Support for emojis (✅/❌), text (yes/no), or numbers (1/0)
- **Local Storage**: All data stored in CSV files (no cloud dependencies)
- **GitHub Integration**: Optional GitHub repository sync for Railway deployment
- **Progress Tracking**: Completion rates and daily summaries
- **User-Friendly Interface**: Reply keyboards for easy responses

## 📁 File Structure

```
habit-tracker-bot/
├── habit_list.csv           # Stores user ID + comma-separated habits
├── habit_tracking.csv       # Logs daily check-ins
├── main.py                  # Entrypoint
├── handlers.py              # Telegram logic
├── scheduler.py             # Daily check-in pings
├── csv_handler.py           # CSV read/write logic
├── github_synch.py          # GitHub repository sync
├── quotes.py                # Motivational quotes
├── config.py                # Bot token, constants
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Bot Token

The bot token is already configured in `config.py`. If you need to use your own bot:

1. Create a bot via [@BotFather](https://t.me/botfather) on Telegram
2. Replace the token in `config.py`

### 3. GitHub Integration (Optional - for Railway deployment)

For Railway deployment where local file persistence is not reliable, you can enable GitHub synchronization:

#### Set up GitHub Repository:
1. Create a new GitHub repository
2. Create a `data/` folder in your repository
3. Generate a GitHub Personal Access Token with `repo` permissions

#### Environment Variables:
Set these environment variables in your Railway deployment:

```bash
GITHUB_REPO_OWNER=your_github_username
GITHUB_REPO_NAME=your_repository_name
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_FILE_PATH=data/habit_list.csv
GITHUB_BRANCH=main
```

The bot will automatically:
- Download `habit_list.csv` from GitHub on startup
- Upload changes to GitHub whenever habits are updated
- Create the file in GitHub if it doesn't exist

### 4. Run the Bot

```bash
python main.py
```

## 📱 Usage

### Getting Started

1. **Start the bot**: Send `/start` to begin
2. **Set your habits**: Enter comma-separated habits (e.g., "workout, drink water, read")
3. **Daily check-ins**: Receive automated reminders at 8:00 AM
4. **Track progress**: Reply with ✅/❌ for each habit

### Commands

- `/start` - Set up your habits
- `/help` - Show help information

### Response Formats

The bot accepts multiple response formats:

- **Emojis**: ✅✅❌
- **Text**: yes yes no
- **Numbers**: 1 1 0
- **Mixed**: ✅ yes ❌

## 📊 Data Storage

### habit_list.csv
```csv
user_id,habits
123456,"workout, drink water, code"
```

### habit_tracking.csv
```csv
date,user_id,habit,status
2025-06-28,123456,workout,✅
2025-06-28,123456,drink water,✅
2025-06-28,123456,code,❌
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Check-in time**: Change `DAILY_CHECKIN_TIME` (default: 8:00 AM)
- **Response patterns**: Modify `POSITIVE_RESPONSES` and `NEGATIVE_RESPONSES`
- **File paths**: Update CSV file locations

## 🛠️ Technical Details

### Dependencies

- **python-telegram-bot**: Telegram Bot API wrapper
- **apscheduler**: Task scheduling for daily check-ins
- **pandas**: Data manipulation (optional, for future analytics)
- **requests**: HTTP requests for GitHub API integration

### Architecture

- **Modular Design**: Separate modules for handlers, CSV operations, and scheduling
- **Async/Await**: Non-blocking I/O operations
- **State Management**: Tracks user conversation states
- **Error Handling**: Graceful error handling and logging
- **GitHub Sync**: Optional repository synchronization for cloud deployments

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard:
   - `TELEGRAM_TOKEN`
   - `GITHUB_REPO_OWNER`
   - `GITHUB_REPO_NAME`
   - `GITHUB_TOKEN`
   - `GITHUB_FILE_PATH` (optional, default: `data/habit_list.csv`)
   - `GITHUB_BRANCH` (optional, default: `main`)
3. Deploy and the bot will automatically sync with GitHub

### Production Deployment
1. Set up a server with Python 3.x
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run the bot: `python main.py`
5. Consider using a process manager like `systemd` or `supervisor`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the logs for error messages
2. Verify your bot token is correct
3. Ensure all dependencies are installed
4. Check that CSV files have proper permissions
5. For GitHub sync issues, verify your GitHub token has `repo` permissions

---

**Happy habit tracking! 🎯✨** 