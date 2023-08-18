import re
import os
import asyncio
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters
from pyrogram.types import ( InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
import humanize
from helper.progress import humanbytes

from helper.database import  insert ,find_one,used_limit,usertype,uploadlimit,addpredata,total_rename,total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.database import addthumb
from helper.date import add_date ,check_expi
from plugins.cb_data import video, confirm_data
CHANNEL = os.environ.get('CHANNEL',"")
import datetime
from datetime import date as date_
STRING = os.environ.get("STRING","")
log_channel = int(os.environ.get("LOG_CHANNEL",""))
token = os.environ.get('TOKEN','')
botid = token.split(':')[0]
DB_CHANNEL_ID = -1001862896786  # Replace with your channel ID

message_queue = asyncio.Queue()
continue_processing = True
batch_data = {}
batch_confirmations = {}
# Define a function to extract message ID from a link
def extract_post_id(link):
    match = re.search(r"/(\d+)/?$", link)
    if match:
        return int(match.group(1))
    return None

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client,message):
	old = insert(int(message.chat.id))
	try:
	    id = message.text.split(' ')[1]
	except:
	    await message.reply_text(text =f"""Hello 👋 {message.from_user.first_name},\n\nI'm File Rename Bot, Please Sent Me Any Telegram Document Or Video And Enter New Filename To Rename It.""",
	reply_to_message_id = message.id ,  
	reply_markup=InlineKeyboardMarkup([[
	   InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Rk_botowner") 
           ],[
           InlineKeyboardButton("🔗 Support", url="https://t.me/Rkbotzsupport"),
           InlineKeyboardButton("📢 Updates", url="https://t.me/Rk_botz")]]))
	    return
	if id:
	    if old == True:
	        try:
	            await client.send_message(id,"Your Friend Already Using Our Bot")
	            await message.reply_text(text =f"""Hello 👋 {message.from_user.first_name},\n\nI'm File Rename Bot, Please Sent Me Any Telegram Document Or Video And Enter New Filename To Rename It.""",    
        reply_to_message_id = message.id ,  
	reply_markup=InlineKeyboardMarkup([[
	   InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Rk_botowner") 
           ],[
           InlineKeyboardButton("🔗 Support", url="https://t.me/Rkbotzsupport"),
           InlineKeyboardButton("📢 Updates", url="https://t.me/Rk_botz")]]))
	        except:
	             return
	    else:
	         await client.send_message(id,"Congrats! You Won 100MB Upload limit")
	         _user_= find_one(int(id))
	         limit = _user_["uploadlimit"]
	         new_limit = limit + 104857600
	         uploadlimit(int(id),new_limit)
	         await message.reply_text(text =f"""Hello 👋 {message.from_user.first_name},\n\nI'm File Rename Bot, Please Sent Me Any Telegram Document Or Video And Enter New Filename To Rename It.""",
	reply_to_message_id = message.id ,  
	reply_markup=InlineKeyboardMarkup([[
	   InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Rk_botowner") 
           ],[
           InlineKeyboardButton("🔗 Support", url="https://t.me/Rkbotzsupport"),
           InlineKeyboardButton("📢 Updates", url="https://t.me/Rk_botz")]]))



@Client.on_message(filters.private &( filters.document | filters.audio | filters.video ))
async def send_doc(client,message):
       update_channel = CHANNEL
       user_id = message.from_user.id
       if update_channel :
       	try:
       		await client.get_chat_member(update_channel, user_id)
       	except UserNotParticipant:
       		await message.reply_text("**You Are Not Subscribed My Updates Channel**",
       		reply_to_message_id = message.id,
       		reply_markup = InlineKeyboardMarkup(
       		[ [ InlineKeyboardButton("🔔 SUBSCRIBE 🔔" ,url=f"https://t.me/{update_channel}") ]   ]))
       		return
       try:
           bot_data = find_one(int(botid))
           prrename = bot_data['total_rename']
           prsize = bot_data['total_size']
           user_deta = find_one(user_id)
       except:
           await message.reply_text("Use About Command First /about")
       try:
       	used_date = user_deta["date"]
       	buy_date= user_deta["prexdate"]
       	daily = user_deta["daily"]
       	user_type = user_deta["usertype"]
       except:
           await message.reply_text("DataBase Has Been Cleared Click On /start And Send Me Document/Video Again")
           return
           
           
       c_time = time.time()
       
       if user_type=="Free":
           LIMIT = 600
       else:
           LIMIT = 50
       then = used_date+ LIMIT
       left = round(then - c_time)
       conversion = datetime.timedelta(seconds=left)
       ltime = str(conversion)
       if left > 0:       	    
       	await message.reply_text(f"```Sorry Dude I Am Not Only For YOU 🤗\nFlood Control Is Active ☑️ So Please Wait For ⏰ {ltime}```",reply_to_message_id = message.id)
       else:
       		# Forward a single message
           		
       		media = await client.get_messages(message.chat.id,message.id)
       		file = media.document or media.video or media.audio 
       		dcid = FileId.decode(file.file_id).dc_id
       		filename = file.file_name
       		value = 2147483648
       		used_ = find_one(message.from_user.id)
       		used = used_["used_limit"]
       		limit = used_["uploadlimit"]
       		expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
       		if expi != 0:
       			today = date_.today()
       			pattern = '%Y-%m-%d'
       			epcho = int(time.mktime(time.strptime(str(today), pattern)))
       			daily_(message.from_user.id,epcho)
       			used_limit(message.from_user.id,0)			     		
       		remain = limit- used
       		if remain < int(file.file_size):
       		    await message.reply_text(f"Sorry! I Can't Upload Files That Are Larger Than {humanbytes(limit)}. File Size Detected {humanbytes(file.file_size)}\nUsed Daly Limit {humanbytes(used)} If U Want To Rename Large File Upgrade Your Plan",reply_markup = InlineKeyboardMarkup([[ InlineKeyboardButton("Upgrade 💰",callback_data = "upgrade") ]]))
       		    return
       		if value < file.file_size:
       		    if STRING:
       		        if buy_date==None:
       		            await message.reply_text(f"You Can't Upload More Then {humanbytes(limit)} Used Daly Limit {humanbytes(used)} ",reply_markup = InlineKeyboardMarkup([[ InlineKeyboardButton("Upgrade 💰",callback_data = "upgrade") ]]))
       		            return
       		        pre_check = check_expi(buy_date)
       		        if pre_check == True:
       		            await message.reply_text(f"""What Do You Want Me To Do With This File ?\n**File Name**: {filename}\n**File Size**: {humanize.naturalsize(file.file_size)}\n**Dc ID**: {dcid}""",reply_to_message_id = message.id,reply_markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📝 Rename",callback_data = "rename"),InlineKeyboardButton("✖️ Cancel",callback_data = "cancel")  ]]))
       		            total_rename(int(botid),prrename)
       		            total_size(int(botid),prsize,file.file_size)
       		        else:
       		            uploadlimit(message.from_user.id,2147483648)
       		            usertype(message.from_user.id,"Free")
	
       		            await message.reply_text(f'Your Plane Expired On 📅 {buy_date}',quote=True)
       		            return
       		    else:
       		          	await message.reply_text("You Can't Upload File Bigger Than 2GB")
       		          	return
       		else:
       		    if buy_date:
       		        pre_check = check_expi(buy_date)
       		        if pre_check == False:
       		            uploadlimit(message.from_user.id,2147483648)
       		            usertype(message.from_user.id,"Free")
       		        
       		    filesize = humanize.naturalsize(file.file_size)
       		    fileid = file.file_id
       		    total_rename(int(botid),prrename)
       		    total_size(int(botid),prsize,file.file_size)
       		    await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name** :- {filename}\n**File Size** :- {filesize}\n**Dc ID** :- {dcid}""",reply_to_message_id = message.id,reply_markup = InlineKeyboardMarkup(
       		[[ InlineKeyboardButton("📝 Rename",callback_data = "rename"),
       		InlineKeyboardButton("Cancel ❎",callback_data = "cancel")  ]]))
       


@Client.on_message(filters.private & filters.command(["batch"]))
async def batch_rename(client, message):
    # Check if the command has the correct number of arguments
    if len(message.command) != 3:
        await message.reply("Usage: /batch start_post_link end_post_link")
        return

    # Extract command arguments (post links)
    start_post_link = message.command[1]
    end_post_link = message.command[2]

    # Extract message IDs from the links
    start_post_id = extract_post_id(start_post_link)
    end_post_id = extract_post_id(end_post_link)

    if start_post_id is None or end_post_id is None:
        await message.reply("Invalid post links provided. Usage: /batch start_post_link end_post_link")
        return

    # Get the source and destination channels
    source_channel_id = -1001514489559  # Replace with the actual source channel ID
    dest_channel_id = -1001862896786    # Replace with the actual destination channel ID

    # Ask user for a thumbnail image
    await message.reply_text("Please provide a thumbnail image for the batch. Send a photo.")

    # Store data for later use
    batch_data[message.chat.id] = {
        "start_post_id": start_post_id,
        "end_post_id": end_post_id,
        "source_channel_id": -1001514489559,  # Replace with the actual source channel ID
        "dest_channel_id": -1001862896786,   # Replace with the actual destination channel ID
    }


# Define your handler for receiving the thumbnail image
@Client.on_message(filters.private & filters.photo)
async def thumbnail_received(client, message):
    chat_id = message.chat.id
    if chat_id not in batch_data:
        file_id = str(message.photo.file_id)
        addthumb(message.chat.id, file_id)
        await message.reply_text("**Your Custom Thumbnail Saved Successfully ☑️**")
        return

    data = batch_data.pop(chat_id)

    start_post_id = data["start_post_id"]
    end_post_id = data["end_post_id"]
    source_channel_id = data["source_channel_id"]
    dest_channel_id = data["dest_channel_id"]
    
    thumbnail_file_id = str(message.photo.file_id)

    await message.reply_text("Please provide /confirm or /unconfirm")

    # Wait for user input (confirmation or unconfirmation)
    while True:
        response = await client.listen(filters=filters.text & filters.private & filters.user(message.from_user.id))
    
        if "/confirm" in response.text:
            await message.reply_text("You confirmed...")
            break  # Exit the loop when confirmation is received
        elif "/unconfirm" in response.text:
            await message.reply_text("You unconfirmed. Process terminated.")
            return 

    await message.reply_text("Renaming started...")

    try:
        # Enqueue messages for processing
        for post_id in range(start_post_id, end_post_id + 1):
            await message_queue.put((source_channel_id, dest_channel_id, post_id, thumbnail_file_id))

        # Process messages from the queue
        while not message_queue.empty():
            source_id, dest_id, post_id, thumbnail_file_id = await message_queue.get()

            try:
                # Copy the message from the source channel
                Rkbotz = await client.copy_message(
                    chat_id=dest_id,
                    from_chat_id=source_id,
                    message_id=post_id
                )

                # Determine media type and invoke appropriate callback
                await video(client, Rkbotz, thumbnail_file_id)
                
                # Delete the original message from the destination channel
                await client.delete_messages(dest_id, [Rkbotz.id, Rkbotz.id + 1])

            except Exception as e:
                await message.reply_text(f"Error processing post {post_id}: {str(e)}")

        await message.reply_text("Renaming completed...")

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")


# Rename all by Rk_botz search on telegram, or telegram.me/Rk_botz
@Client.on_message(filters.private & filters.command(["rename_all"]))
async def all_rename(bot, message):
    # Check if the command has the correct number of arguments
    if len(message.command) != 3:
        await message.reply("Usage: /rename_all last_post_link")
        return
	    
    
    end_post_link = message.command[1]

    # Extract message IDs from the links
    start_post_id = 1
    end_post_id = extract_post_id(end_post_link)
	
    # Get the source and destination channels
    source_channel_id = -1001900711105  # Replace with the actual source channel ID
    dest_channel_id = -1001835537776    # Replace with the actual destination channel ID
    await message.reply_text("Please provide a thumbnail image for the Renameing. Send a photo.")

    # Store data for later use
    batch_data[message.chat.id] = {
        "start_post_id": start_post_id,
        "end_post_id": end_post_id,
        "source_channel_id": -1001900711105,  # Replace with the actual source channel ID
        "dest_channel_id": -1001835537776,   # Replace with the actual destination channel ID
	}
	
@Client.on_message(filters.command(["help"]))
async def help_command(bot, message):
    await message.reply("This bot is only for private use by owner.\n\ncommands list \n\n1./addpremium userid\n2. /batch link1 link2\n3. /rename_all ")
        
	     
