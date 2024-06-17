import requests
import os
from dotenv import load_dotenv
import json
from telethon import TelegramClient


load_dotenv()

prod_mode = False

TELEGRAM_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_CHAT_ID')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

client = TelegramClient('session_name', api_id, api_hash)


def send_message(text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }

    if reply_markup:
        data['reply_markup'] = (None, json.dumps(reply_markup))

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # TO-DO: Handle errors correctly.
        print('Error while sending to telegram.', e)
    return None


async def get_last_hundred_messages():
    """Fetch the last hundred messages from the Telegram channel."""
    messages = []
    try:
        async for message in client.iter_messages(TELEGRAM_CHAT_ID, limit=100):
            messages.append(message)
            print(message)
    except Exception as e:
        print(f"Error fetching messages from Telegram: {e}")
    return messages
