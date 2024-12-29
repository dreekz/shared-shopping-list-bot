import telegram
import requests
import os
import json
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackContext
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
ADMIN_ID = os.getenv("ADMIN_ID")  # Your Telegram ID

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block)

def list_items(update: telegram.Update, context: CallbackContext):
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
        message_text = f"❌ שגיאה בקבלת הרשימה: {str(e)}"
    
    context.bot.send_message(chat_id=chat_id, text=message_text)

def add_user(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    
    if user_id != ADMIN_ID:
        context.bot.send_message(chat_id=chat_id, text="❌ רק מנהל יכול להוסיף משתמשים חדשים")
        return

    if not context.args:
        context.bot.send_message(chat_id=chat_id, text="⚠️ נא לספק מזהה משתמש")
        return

    new_user_id = context.args[0]
    
    try:
        response = requests.post(
            API_URL,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            data=json.dumps({
                'action': 'add_user',
                'user_id': user_id,
                'new_user_id': new_user_id
            }, ensure_ascii=False).encode('utf-8')
        )
        
        if response.status_code == 201:
            message_text = f"✅ משתמש {new_user_id} נוסף בהצלחה"
        else:
            message_text = f"❌ שגיאה בהוספת משתמש: {response.json().get('message', 'Unknown error')}"
            
    except requests.exceptions.RequestException as e:
        message_text = f"❌ שגיאה בתקשורת: {str(e)}"
    
    context.bot.send_message(chat_id=chat_id, text=message_text)

def add_item(update: telegram.Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    
    try:
        item_name = ' '.join(context.args)
        if not item_name:
            context.bot.send_message(chat_id=chat_id, text="⚠️ נא להזין שם פריט")
            return

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        body = {
            'item_name': item_name,
            'user_id': user_id
        }
        
        session = requests.Session()
        adapter = MyAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.post(
            API_URL, 
            headers=headers, 
            data=json.dumps(body, ensure_ascii=False).encode('utf-8')
        )
        
        if response.status_code == 403:
            message_text = "❌ אין לך הרשאה להוסיף פריטים"
        elif response.status_code == 409:
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
    user_id = str(update.effective_user.id)
    
    try:
        item_name = ' '.join(context.args)
        if not item_name:
            context.bot.send_message(chat_id=chat_id, text="⚠️ נא להזין שם פריט למחיקה")
            return

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        body = {
            'item_name': item_name,
            'user_id': user_id
        }
        
        session = requests.Session()
        adapter = MyAdapter(max_retries=3)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.delete(
            API_URL, 
            headers=headers, 
            data=json.dumps(body, ensure_ascii=False).encode('utf-8')
        )
        
        if response.status_code == 403:
            message_text = "❌ אין לך הרשאה למחוק פריטים"
        elif response.status_code == 200:
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
    dp.add_handler(CommandHandler("list", list_items))
    dp.add_handler(CommandHandler("add", add_item))
    dp.add_handler(CommandHandler("remove", remove_item))
    dp.add_handler(CommandHandler("add_user", add_user))

    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()