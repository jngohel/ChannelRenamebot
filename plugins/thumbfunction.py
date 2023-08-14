from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

DB_CHANNEL = -1001862896786

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

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client,message):
	file_id = str(message.photo.file_id)
	addthumb(message.chat.id , file_id)
	await message.reply_text("**Your Custom Thumbnail Saved Successfully ☑️**")
	
@Client.on_message(DB_CHANNEL & filters.command(['view_thumb']))
async def view_thumb(client,message):
    print(message.chat.id)
    thumb = find(int(message.chat.id))[0]
    if thumb:
        await client.send_photo(message.chat.id, photo=f"{thumb}")
    else:
        await message.reply_text("**You Don't Have Any Custom Thumbnail ✖️**")

@Client.on_message(DB_CHANNEL & filters.command(['del_thumb']))
async def remove_thumb(client,message):
    delthumb(int(message.chat.id))
    await message.reply_text("**Your Custom Thumbnail Was Deleted Successfully ☑️**")

@Client.on_message(DB_CHANNEL & filters.photo)
async def add_thumbs(client,message):
    file_id = str(message.photo.file_id)
    addthumb(message.chat.id, file_id)
    await message.reply_text("**Your Custom Thumbnail Was Saved Successfully ☑️**")
