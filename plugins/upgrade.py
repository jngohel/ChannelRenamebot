from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from pyrogram import Client , filters

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
	text = """**Free Plan User**
	Daily Upload Limit 2GB
	Price 0
	
	**VIP 1 ** 
	Daily Upload  Limit 10GB
	Price Rs 55  🇮🇳/🌎 0.67$  per Month
	
	**VIP 2 **
	Daily Upload Limit 50GB
	Price Rs 80  🇮🇳/🌎 0.97$  per Month

	UPI 🆔 Details

        jngohel@upi
	
	After Payment Send Screenshots Of 
        Payment To Admin"""
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("👮 Admin", url = "https://t.me/JNGohell")], 
        			[InlineKeyboardButton("Cancel ✖️", callback_data = "cancel")  ]])
	await update.message.edit(text = text,reply_markup = keybord)
	

@Client.on_message(filters.private & filters.command(["plans"]))
async def upgrade_cm(bot,message):
	text = """**Free Plan User**
	Daily Upload Limit 2GB
	Price 0
	
	**VIP 1 ** 
	Daily Upload  Limit 10GB
	Price Rs 55  🇮🇳/🌎 0.67$  per Month
	
	**VIP 2 **
	Daily Upload Limit 50GB
	Price Rs 80  🇮🇳/🌎 0.97$  per Month

	UPI 🆔 Details

        jngohel@upi
	
	After Payment Send Screenshots Of 
        Payment To Admin"""
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("👮 Admin", url = "https://t.me/JNGohell")], 
        			[InlineKeyboardButton("Cancel ✖️", callback_data = "cancel")  ]])
	await update.message.edit(text = text,reply_markup = keybord)
	
