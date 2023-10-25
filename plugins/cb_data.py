from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import (  InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import *
import re
import os
import random
from PIL import Image
import time
from datetime import date as date_
from datetime import timedelta,datetime
from helper.ffmpeg import take_screen_shot,fix_thumb
from helper.progress import humanbytes
from helper.set import escape_invalid_curly_brackets
#from helper.database import get_thumbnail

log_channel = int(os.environ.get("LOG_CHANNEL", ""))

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

STRING = os.environ.get("STRING", "")

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

# Add the URL of the default thumbnail
#default_thumbnail_url = "https://telegra.ph/file/f2b805cc65089bc72d153.jpg"
batch_confirmations = {}
batch_data = {}

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot,update):
	try:
		await update.message.delete()
	except:
		return
		
		
@Client.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
	date_fa = str(update.message.date)
	pattern = '%Y-%m-%d %H:%M:%S'
	date = int(time.mktime(time.strptime(date_fa, pattern)))
	chat_id = update.message.chat.id
	id = update.message.reply_to_message_id
	await update.message.delete()
	await update.message.reply_text(f"Please Enter The New Filename\n\n✍️ Note: Extension Not Required",reply_to_message_id = id,
	reply_markup=ForceReply(True) )
	dateupdate(chat_id,date)
	
	
	
@Client.on_callback_query(filters.regex("doc"))
async def doc(bot,update):
     new_name = update.message.text
     used_ = find_one(update.from_user.id)
     used = used_["used_limit"]
     date = used_["date"]	
     name = new_name.split(":")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
     ms = await update.message.edit("```Trying To Download...```")
     used_limit(update.from_user.id,file.file_size)
     c_time = time.time()
     total_used = used + int(file.file_size)
     used_limit(update.from_user.id,total_used)
     try:
     		path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     		
     except Exception as e:
          neg_used = used - int(file.file_size)
          used_limit(update.from_user.id,neg_used)
          await ms.edit(e)
          return
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     user_id = int(update.message.chat.id)
     data = find(user_id)
     try:
         c_caption = data[1]
     except:
         pass
     thumb = data[0]
     if c_caption:
        doc_list= ["filename","filesize"]
        new_tex = escape_invalid_curly_brackets(c_caption,doc_list)
        caption = new_tex.format(filename=new_filename,filesize=humanbytes(file.file_size))
     else:
        caption = f"**{new_filename}**"
     if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 240))
     		img.save(ph_path, "JPEG")
     		c_time = time.time()
     		
     else:
     		ph_path = None
     
     value = 2090000000
     if value < file.file_size:
         await ms.edit("```Trying To Upload...```")
         try:
             filw = await app.send_document(log_channel,document = file_path,thumb=ph_path,caption = caption,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
             from_chat = filw.chat.id
             mg_id = filw.id
             time.sleep(2)
             await bot.copy_message(update.from_user.id,from_chat,mg_id)
             await ms.delete()
             os.remove(file_path)
             try:
                 os.remove(ph_path)
             except:
                 pass
         except Exception as e:
             neg_used = used - int(file.file_size)
             used_limit(update.from_user.id,neg_used)
             await ms.edit(e)
             os.remove(file_path)
             try:
                 os.remove(ph_path)
             except:
                 return
     else:
     		await ms.edit("```Trying To Upload...```")
     		c_time = time.time()
     		try:
     			await bot.send_document(update.from_user.id,document = file_path,thumb=ph_path,caption = caption,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))			
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			neg_used = used - int(file.file_size)
     			used_limit(update.from_user.id,neg_used)
     			await ms.edit(e)
     			os.remove(file_path)
     			return 
     			     		   		
   		
     		     		     		
@Client.on_callback_query(filters.regex("vid"))
async def vid(bot,update):
     new_name = update.message.text
     used_ = find_one(update.from_user.id)
     used = used_["used_limit"]
     date = used_["date"]
     name = new_name.split(":")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
     ms = await update.message.edit("```Trying To Download...```")
     used_limit(update.from_user.id,file.file_size)
     c_time = time.time()
     total_used = used + int(file.file_size)
     used_limit(update.from_user.id,total_used)
     try:
     		path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     		
     except Exception as e:
          neg_used = used - int(file.file_size)
          used_limit(update.from_user.id,neg_used)
          await ms.edit(e)
          return
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     user_id = int(update.message.chat.id)
     data = find(user_id)
     try:
         c_caption = data[1]
     except:
         pass
     thumb = data[0]
     
     duration = 0     
     metadata = extractMetadata(createParser(file_path))
     if metadata.has("duration"):
         duration = metadata.get('duration').seconds
     if c_caption:
        vid_list = ["filename","filesize","duration"]
        new_tex = escape_invalid_curly_brackets(c_caption,vid_list)
        caption = new_tex.format(filename=new_filename,filesize=humanbytes(file.file_size),duration=timedelta(seconds=duration))
     else:
        caption = f"**{new_filename}**"
     if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 320))
     		img.save(ph_path, "JPEG")
     		c_time = time.time()
     		
     else:
     		try:
     		    ph_path_ = await take_screen_shot(file_path,os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
     		    width, height, ph_path = await fix_thumb(ph_path_)
     		except Exception as e:
     		    ph_path = None
     		    print(e)
     		
     
     value = 2090000000
     if value < file.file_size:
         await ms.edit("```Trying To Upload...```")
         try:
	     
             filw = await app.send_video(log_channel,video= file_path,thumb=ph_path,duration=duration ,caption = caption,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
             from_chat = filw.chat.id
             mg_id = filw.id
             time.sleep(2)
             await bot.copy_message(update.from_user.id,from_chat,mg_id)
             await ms.delete()
             os.remove(file_path)
             try:
                 os.remove(ph_path)
             except:
                 pass
         except Exception as e:
             neg_used = used - int(file.file_size)
             used_limit(update.from_user.id,neg_used)
             await ms.edit(e)
             os.remove(file_path)
             try:
                 os.remove(ph_path)
             except:
                 return
     else:
     		await ms.edit("```Trying To Upload...```")
     		c_time = time.time()
     		try:
     			await bot.send_video(update.from_user.id,video = file_path,thumb=ph_path,duration=duration,caption = caption,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))			
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			neg_used = used - int(file.file_size)
     			used_limit(update.from_user.id,neg_used)
     			await ms.edit(e)
     			os.remove(file_path)
     			return 
     
   
   
     			     		     		
@Client.on_callback_query(filters.regex("aud"))
async def aud(bot,update):
     new_name = update.message.text
     used_ = find_one(update.from_user.id)
     used = used_["used_limit"]
     name = new_name.split(":-")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
     total_used = used + int(file.file_size)
     used_limit(update.from_user.id,total_used)
     ms = await update.message.edit("```Trying To Download...```")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file , progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     except Exception as e:
     	neg_used = used - int(file.file_size)
     	used_limit(update.from_user.id,neg_used)
     	await ms.edit(e)
     	return
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     metadata = extractMetadata(createParser(file_path))
     if metadata.has("duration"):
     	duration = metadata.get('duration').seconds
     user_id = int(update.message.chat.id)
     data = find(user_id)
     c_caption = data[1] 
     thumb = data[0]
     if c_caption:
        aud_list = ["filename","filesize","duration"]
        new_tex = escape_invalid_curly_brackets(c_caption,aud_list)
        caption = new_tex.format(filename=new_filename,filesize=humanbytes(file.file_size),duration=timedelta(seconds=duration))
     else:
        caption = f"**{new_filename}**"
        
     if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 320))
     		img.save(ph_path, "JPEG")
     		await ms.edit("```Trying To Upload...```")
     		c_time = time.time()
     		try:
     			await bot.send_audio(update.message.chat.id,audio = file_path,caption = caption,thumb=ph_path,duration =duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     			os.remove(ph_path)
     		except Exception as e:
     			neg_used = used - int(file.file_size)
     			used_limit(update.from_user.id,neg_used)
     			await ms.edit(e)
     			os.remove(file_path)
     			os.remove(ph_path)
     else:
     		await ms.edit("```Trying To Upload...```")
     		c_time = time.time()
     		try:
     			await bot.send_audio(update.message.chat.id,audio = file_path,caption = caption,duration = duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			neg_used = used - int(file.file_size)
     			used_limit(update.from_user.id,neg_used)
     			os.remove(file_path)

def clean_caption(caption):
    # Remove @username mentions
    caption = re.sub(r'@\w+\b', '', caption)
    
    # Remove links (http/https)
    caption = re.sub(r'http[s]?:\/\/\S+', '', caption)
    
    return caption.strip()
# For channel 
async def video(bot, update, file_id):
    new_filename = clean_caption(update.caption)
    file_path = f"downloads/{new_filename}"
    message = update.reply_to_message
    c_thumb = file_id
    file = update.document or update.video or update.audio
    Rkbotz = await update.reply_text("renaming this file....")
    ms = await Rkbotz.edit("```Trying To Upload...```")
    time.sleep(2)
    c_time = time.time()

    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("``` Trying To Download...```", ms, c_time))
    except Exception as e:
        await ms.edit(str(e))
        return

    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)

    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds

    caption = f"<b>{new_filename}</b>"
    thumb_path = await bot.download_media(c_thumb) 
    try:
       with Image.open(thumb_path) as img:
	       img = img.convert("RGB")
	       #img = img.resize((320, 180))
	       img.save(thumb_path, "JPEG")
            
            
 #   if file.thumbs or c_thumb:
      #  if c_thumb:
         #   thumb_path = await bot.download_media(c_thumb)
      #  else:
           # thumb_id = file.thumbs[0].file_id
           # thumb_path = await bot.download_media(thumb_id)

        
            #with Image.open(thumb_path) as img:
               # img = img.convert("RGB")
            #    img = img.resize((320, 240))
             #   img.save(thumb_path, "JPEG")
    except Exception as e:
        await ms.edit(f"Thumbnail processing error: {str(e)}")

    value = 2090000000
    if value < file.file_size:
        await ms.edit("```Trying To Upload...```")
        try:
            c_time = time.time()
            filw = await app.send_video(log_channel, video=file_path, thumb=thumb_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```", ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            try:
                os.remove(thumb_path)
            except:
                pass
        except Exception as e:
            await ms.edit(str(e))
            os.remove(file_path)
            try:
                os.remove(thumb_path)
            except:
                return
    else:
        await ms.edit("```Trying To Upload...```")
        try:
            c_time = time.time()
            await bot.send_video(update.chat.id, video=file_path, thumb=thumb_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("```Trying To Uploading```", ms, c_time))
            os.remove(file_path)
        except Exception as e:
            await ms.edit(str(e))
            os.remove(file_path)
            return
		
@Client.on_callback_query(filters.regex('confirm'))
async def confirm_data(bot, callback_query):
	
        chat_id = int(callback_query.message.chat.id)
       
        data = batch_data.pop(chat_id)

        start_post_id = data["start_post_id"]
        end_post_id = data["end_post_id"]
        source_channel_id = data["source_channel_id"]
        dest_channel_id = data["dest_channel_id"]

        
        thumbnail_file_id = str(callback_query.message.photo[-1].file_id)

        await callback_query.message.reply_text("Renaming started...")

        try:
                # Enqueue messages for processing
            for post_id in range(start_post_id, end_post_id + 1):
                await message_queue.put((source_channel_id, dest_channel_id, post_id, thumbnail_file_id))

                # Process messages from the queue
            while not message_queue.empty():
                source_id, dest_id, post_id, thumbnail_file_id = await message_queue.get()

                try:
                        # Copy the message from the source channel
                    Rkbotz = await bot.copy_message(
                        chat_id=dest_id,
                        from_chat_id=source_id,
                        message_id=post_id
                    )

                        # Determine media type and invoke appropriate callback
                    await video(bot, Rkbotz, thumbnail_file_id)

                        # Delete the original message from the destination channel
                    await bot.delete_messages(dest_id, Rkbotz.id)
                    await bot.delete_messages(dest_id, Rkbotz.id + 1)

                except Exception as e:
                    await callback_query.message.reply_text(f"Error processing post {post_id}: {str(e)}")

            await callback_query.message.reply_text("Renaming completed...")

        except Exception as e:
            await callback_query.message.reply_text(f"Error: {str(e)}")


    
