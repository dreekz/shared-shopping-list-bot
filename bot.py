import telegram
import requests
import os
import json
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager


# Load environment variables from .env file
load_dotenv()

# Get variables from the environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block)


def handle_message(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        message_text = f"API Response (GET): {data}"

    except requests.exceptions.RequestException as e:
        message_text = f"Error calling API: {e}"

    context.bot.send_message(chat_id=chat_id, text=message_text)


def add_item(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        item_name = ' '.join(context.args)
        if not item_name:
            context.bot.send_message(chat_id=chat_id, text="Please provide an item name")
            return

        headers = {'Content-Type': 'application/json'}
        body = {'item_name': item_name}

        session = requests.Session()
        adapter = MyAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.post(API_URL, headers=headers, data=json.dumps(body))
        response.raise_for_status()

        data = response.json()

        message_text = f"API Response (POST): {data}"


    except requests.exceptions.RequestException as e:
        message_text = f"Error calling API: {e}"

    context.bot.send_message(chat_id=chat_id, text=message_text)


def remove_item(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        if len(context.args) != 2:
           context.bot.send_message(chat_id=chat_id, text="Please provide both item_id and list_id")
           return
        item_id = context.args[0]
        list_id = context.args[1]
        headers = {'Content-Type': 'application/json'}
        body = {'item_id': item_id, 'list_id': list_id}

        session = requests.Session()
        adapter = MyAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.delete(API_URL, headers=headers, data=json.dumps(body))
        response.raise_for_status()

        data = response.json()

        message_text = f"API Response (DELETE): {data}"


    except requests.exceptions.RequestException as e:
        message_text = f"Error calling API: {e}"

    context.bot.send_message(chat_id=chat_id, text=message_text)

def main():
    bot = telegram.Bot(token=BOT_TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CommandHandler("add", add_item))
    dp.add_handler(CommandHandler("remove", remove_item))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()