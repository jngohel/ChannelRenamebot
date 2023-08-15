from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

#DB_CHANNEL = -1001862896786

@Client.on_message(filters.private & filters.command(['viewthumb']))
async def viewthumb(client,message):
		print(message.chat.id)
		thumb = find(int(message.chat.id))[0]
		if thumb :
			await client.send_photo(message.chat.id,photo =f"{thumb}")
		else:
			await message.reply_text("**Your Don't Have Any Custom Thumbnail ✖️**")
	
	
@Client.on_message(filters.private & filters.command(['delthumb']))
async def removethumb(client,message):
	delthumb(int(message.chat.id))
	await message.reply_text("**Your Custom Thumbnail Deleted Successfully ☑️**")

