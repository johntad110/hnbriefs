import requests
import os
from dotenv import load_dotenv
import json


load_dotenv()

prod_mode = False

TELEGRAM_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TG_CHAT_ID')


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


def get_last_hundred_messages():
    """Fetch the last hundred messages from the Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {
        "limit": 100,
        "offset": -100  # Fetches the last 100 messages.
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        updates = response.json().get('result', [])
        messages = [update['message'] for update in updates if 'message' in update]
        for message in messages:
            print(message)
        return messages
    except Exception as e:
        print(f"Error fetching messages from Telegram: {e}")
    return []
