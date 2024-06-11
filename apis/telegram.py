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
