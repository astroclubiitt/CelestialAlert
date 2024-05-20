from threading import Thread
import os

# Function to run the Flask server with gunicorn
def run_flask():
    os.system("gunicorn app:app --workers 4 --bind 0.0.0.0:8000")

# Function to run the Discord bot
def run_discord_bot():
    os.system("python bot.py")

if __name__ == "__main__":
    # Start the Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start the Discord bot in the main thread
    run_discord_bot()
