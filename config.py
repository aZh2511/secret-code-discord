from dotenv import load_dotenv
import os

load_dotenv()

settings = {
    'token': os.getenv('TOKEN'),
    'bot': os.getenv('BOT'),
    'id': int(os.getenv('ID')),
    'prefix': '$'
}
host = os.getenv("PGHOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
ADMIN_ID = int(os.getenv('ADMIN_ID'))
DAVID_ID = int(os.getenv('DAVID_ID'))
ADMIN_IDS = [ADMIN_ID, DAVID_ID]
DISCORD_LINK = os.getenv('DISCORD_LINK')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
