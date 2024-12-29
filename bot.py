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
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        if not items:
            message_text = "📝 רשימת הקניות ריקה"
        else:
            message_text = "🛒 רשימת קניות:\n"
            for i, item in enumerate(items, 1):
                message_text += f"{i}. {item.get('item_name', 'פריט לא ידוע')}\n"
    except requests.exceptions.RequestException as e:
        message_text = f"❌ שגיאה: {str(e)}"
    
    context.bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')

def add_item(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        item_name = ' '.join(context.args)
        if not item_name:
            context.bot.send_message(chat_id=chat_id, text="⚠️ נא להזין שם פריט")
            return

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        body = {'item_name': item_name}
        
        session = requests.Session()
        adapter = MyAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.post(
            API_URL, 
            headers=headers, 
            data=json.dumps(body, ensure_ascii=False).encode('utf-8')
        )
        
        if response.status_code == 409:
            message_text = f"⚠️ '{item_name}' כבר קיים ברשימה"
        elif response.status_code == 201:
            message_text = f"✅ '{item_name}' נוסף לרשימה"
        else:
            message_text = f"❌ נכשל להוסיף '{item_name}'"
            
    except requests.exceptions.RequestException as e:
        message_text = f"❌ שגיאה: {str(e)}"
    
    context.bot.send_message(chat_id=chat_id, text=message_text)

def remove_item(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    try:
        item_name = ' '.join(context.args)
        if not item_name:
            context.bot.send_message(chat_id=chat_id, text="⚠️ נא להזין שם פריט למחיקה")
            return

        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        body = {'item_name': item_name}
        
        session = requests.Session()
        adapter = MyAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.delete(
            API_URL, 
            headers=headers, 
            data=json.dumps(body, ensure_ascii=False).encode('utf-8')
        )
        
        if response.status_code == 200:
            message_text = f"✅ '{item_name}' הוסר מהרשימה"
        elif response.status_code == 404:
            message_text = f"⚠️ '{item_name}' לא נמצא ברשימה"
        else:
            message_text = f"❌ נכשל להסיר '{item_name}'"
            
    except requests.exceptions.RequestException as e:
        message_text = f"❌ שגיאה: {str(e)}"
    
    context.bot.send_message(chat_id=chat_id, text=message_text)

def main():
    bot = telegram.Bot(token=BOT_TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CommandHandler("add", add_item))
    dp.add_handler(CommandHandler("remove", remove_item))

    # Start the bot
    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()