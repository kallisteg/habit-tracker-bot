# quotes.py
import random

MOTIVATIONAL_QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "The future depends on what you do today. - Mahatma Gandhi",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "It always seems impossible until it's done. - Nelson Mandela",
    "The way to get started is to quit talking and begin doing. - Walt Disney",
    "Success is walking from failure to failure with no loss of enthusiasm. - Winston Churchill",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs",
    "The greatest glory in living lies not in never falling, but in rising every time we fall. - Nelson Mandela",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The only person you are destined to become is the person you decide to be. - Ralph Waldo Emerson",
    "What you get by achieving your goals is not as important as what you become by achieving your goals. - Zig Ziglar",
    "The mind is everything. What you think you become. - Buddha",
    "Life is 10% what happens to you and 90% how you react to it. - Charles R. Swindoll",
    "The best way to predict the future is to create it. - Peter Drucker",
    "Don't let yesterday take up too much of today. - Will Rogers",
    "You miss 100% of the shots you don't take. - Wayne Gretzky",
    "The journey of a thousand miles begins with one step. - Lao Tzu",
    "Every expert was once a beginner. - Robert T. Kiyosaki"
]

def get_random_quote():
    """Returns a random motivational quote."""
    return random.choice(MOTIVATIONAL_QUOTES) 