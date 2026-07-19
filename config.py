import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN", "8934389081:AAETw7VsVh30HYnHraB1e9wdMxDCM69gG2I")
DB_NAME = "tracker.db"