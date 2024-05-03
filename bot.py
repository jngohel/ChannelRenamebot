import asyncio
from pyrogram import Client, compose,idle
import os
from plugins.cb_data import app as Client2

API_ID = int(os.environ.get("API_ID", "24998279"))
API_HASH = os.environ.get("API_HASH", "b2ec3ab8ed156e7a6782f3d7d1acbaf6")
TOKEN = os.environ.get("TOKEN", "6525627371:AAEPgQ_2jxzzrEv4VHrfRAc1IhBrBNbKH7I")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))
STRING = os.environ.get("STRING", "")

bot = Client(

           "Rename",
           bot_token=TOKEN,
           api_id=API_ID,
           api_hash=API_HASH,
           plugins=dict(root='plugins'))
           

if STRING:
    apps = [Client2,bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    bot.run()
