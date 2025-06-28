# 🤖 Telegram Habit Tracker Bot

A Python-based Telegram bot that helps users track their daily habits with motivational quotes and local CSV storage.

## 🎯 Features

- **Daily Habit Check-ins**: Automated reminders at 8:00 AM
- **Motivational Quotes**: Random inspirational quotes with each check-in
- **Flexible Responses**: Support for emojis (✅/❌), text (yes/no), or numbers (1/0)
- **Local Storage**: All data stored in CSV files (no cloud dependencies)
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

### 3. Run the Bot

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

### Architecture

- **Modular Design**: Separate modules for handlers, CSV operations, and scheduling
- **Async/Await**: Non-blocking I/O operations
- **State Management**: Tracks user conversation states
- **Error Handling**: Graceful error handling and logging

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
1. Set up a server with Python 3.x
2. Install dependencies: `pip install -r requirements.txt`
3. Run the bot: `python main.py`
4. Consider using a process manager like `systemd` or `supervisor`

### GitHub Actions (Optional)
The bot can be deployed using GitHub Actions for continuous operation.

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

---

**Happy habit tracking! 🎯✨** 