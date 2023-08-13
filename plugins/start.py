import os
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters
from pyrogram.types import ( InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
import humanize
from helper.progress import humanbytes

from helper.database import  insert ,find_one,used_limit,usertype,uploadlimit,addpredata,total_rename,total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import add_date ,check_expi
CHANNEL = os.environ.get('CHANNEL',"")
import datetime
from datetime import date as date_
STRING = os.environ.get("STRING","")
log_channel = int(os.environ.get("LOG_CHANNEL",""))
token = os.environ.get('TOKEN','')
botid = token.split(':')[0]


@Client.on_message(filters.private & filters.command(["start"]))
async def start(client,message):
	old = insert(int(message.chat.id))
	try:
	    id = message.text.split(' ')[1]
	except:
	    await message.reply_text(text =f"""Hello 👋 {message.from_user.first_name},\n\nI'm File Rename Bot, Please Sent Me Any Telegram Document Or Video And Enter New Filename To Rename It.""",
	reply_to_message_id = message.id ,  
	reply_markup=InlineKeyboardMarkup([[
	   InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/pr0fess0r99") 
           ],[
           InlineKeyboardButton("🔗 Support", url="https://t.me/TechProjectsChats"),
           InlineKeyboardButton("📢 Updates", url="https://t.me/TechProjectsUpdates")]]))
	    return
	if id:
	    if old == True:
	        try:
	            await client.send_message(id,"Your Friend Already Using Our Bot")
	            await message.reply_text(text =f"""Hello 👋 {message.from_user.first_name},\n\nI'm File Rename Bot, Please Sent Me Any Telegram Document Or Video And Enter New Filename To Rename It.""",    
        reply_to_message_id = message.id ,  
	reply_markup=InlineKeyboardMarkup([[
	   InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/pr0fess0r99") 
           ],[
           InlineKeyboardButton("🔗 Support", url="https://t.me/TechProjectsChats"),
           InlineKeyboardButton("📢 Updates", url="https://t.me/TechProjectsUpdates")]]))
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
	   InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/pr0fess0r99") 
           ],[
           InlineKeyboardButton("🔗 Support", url="https://t.me/TechProjectsChats"),
           InlineKeyboardButton("📢 Updates", url="https://t.me/TechProjectsUpdates")]]))
	         



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
       		
# Command handler for /file_rename
@Client.on_message(filters.command("file_rename") & filters.reply)
async def file_rename_command(client, message):
    try:
        await message.edit("```Processing...```")
        user_id = message.from_user.id
        replied_message = message.reply_to_message

        if replied_message.document or replied_message.video or replied_message.audio:
            new_name = message.caption or "Untitled"  # Use caption as new filename
            used_ = find_one(user_id)
            used = used_["used_limit"]
            date = used_["date"]

            file = replied_message.document or replied_message.video or replied_message.audio
            file_size = file.file_size
            c_time = time.time()
            
            # Download and process the file
            try:
                path = await bot.download_media(
                    message=file,
                    progress=progress_for_pyrogram,
                    progress_args=("```Trying To Download...```", message, c_time)
                )
            except Exception as e:
                await message.edit(str(e))
                return
            
            # Rename and move the file
            splitpath = path.split("/downloads/")
            dow_file_name = splitpath[1]
            new_filename = new_name + os.path.splitext(dow_file_name)[1]
            file_path = f"downloads/{new_filename}"
            os.rename(path, file_path)
            
            # Process user data and caption
            used_limit(user_id, file_size)
            total_used = used + int(file_size)
            used_limit(user_id, total_used)
            data = find(user_id)
            try:
                c_caption = data[1]
            except:
                c_caption = None
            thumb = data[0]
            
            duration = 0
            metadata = extractMetadata(createParser(file_path))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds

            if c_caption:
                vid_list = ["filename", "filesize", "duration"]
                new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
                caption = new_tex.format(
                    filename=new_filename,
                    filesize=humanbytes(file.file_size),
                    duration=timedelta(seconds=duration)
                )
            else:
                caption = f"**{new_filename}**"

            # Resize and process the thumbnail image
            if thumb:
                ph_path = await bot.download_media(thumb)
                Image.open(ph_path).convert("RGB").save(ph_path)
                img = Image.open(ph_path)
                img.resize((320, 320))
                img.save(ph_path, "JPEG")
                c_time = time.time()
            else:
                try:
                    ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
                    width, height, ph_path = await fix_thumb(ph_path_)
                except Exception as e:
                    ph_path = None
                    print(e)
            
            # Upload the processed file
            try:
                await message.edit("```Trying To Upload...```")
                if file_size > 2090000000:
                    await bot.send_video(
                        user_id,
                        video=file_path,
                        thumb=ph_path,
                        duration=duration,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=("```Trying To Uploading```", message, c_time)
                    )
                else:
                    await app.send_video(
                        user_id,
                        video=file_path,
                        thumb=ph_path,
                        duration=duration,
                        caption=caption,
                        progress=progress_for_pyrogram,
                        progress_args=("```Trying To Uploading```", message, c_time)
                    )
            except Exception as e:
                neg_used = used - int(file_size)
                used_limit(user_id, neg_used)
                await message.edit(str(e))
                return

            # Clean up
            os.remove(file_path)
            if ph_path:
                try:
                    os.remove(ph_path)
                except:
                    pass

            await message.edit("File renamed and uploaded successfully!")
        else:
            await message.edit("Please reply to a media file.")

    except Exception as ex:
        await message.edit(f"An error occurred: {ex}")
