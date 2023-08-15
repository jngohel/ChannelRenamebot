import pymongo 
import os
from helper.date import add_date
DB_NAME = os.environ.get("DB_NAME","")
DB_URL = os.environ.get("DB_URL","")
mongo = pymongo.MongoClient(DB_URL)
db = mongo[DB_NAME]
dbcol = db["user"]
channel_col = db["channel"]

#Total User 

def total_user():
      user = dbcol.count_documents({})
      return user
      
#insert bot Data 
def botdata(chat_id):
	bot_id = int(chat_id)
	try:
		bot_data = {"_id":bot_id,"total_rename":0,"total_size":0}
		dbcol.insert_one(bot_data)
	except:
		pass


def total_rename(chat_id,renamed_file):
	now = int(renamed_file) + 1
	dbcol.update_one({"_id":chat_id},{"$set":{"total_rename":str(now)}})
	
def total_size(chat_id,total_size,now_file_size):
	now = int(total_size) + now_file_size
	dbcol.update_one({"_id":chat_id},{"$set":{"total_size":str(now)}})

	
#insert user data 
def insert(chat_id):
            user_id = int(chat_id)
            user_det = {"_id":user_id,"file_id":None ,"caption":None ,"daily":0 ,"date":0 , "uploadlimit" :2147483648,"used_limit":0,"usertype":"Free","prexdate" : None}
            try:
            	dbcol.insert_one(user_det)
            except:
            	return True
            	pass

def addthumb(chat_id, file_id):
	dbcol.update_one({"_id":chat_id},{"$set":{"file_id":file_id}})
	
def delthumb(chat_id):
	dbcol.update_one({"_id":chat_id},{"$set":{"file_id":None}})

def addcaption(chat_id, caption):
       dbcol.update_one({"_id": chat_id},{"$set":{"caption": caption}})
	
def delcaption(chat_id): 
        dbcol.update_one({"_id": chat_id},{"$set":{"caption":None}})
	
def dateupdate(chat_id,date):
	dbcol.update_one({"_id":chat_id},{"$set":{"date":date}})

def used_limit(chat_id,used):
	dbcol.update_one({"_id":chat_id},{"$set":{"used_limit":used}})
	
def usertype(chat_id,type):
	dbcol.update_one({"_id":chat_id},{"$set":{"usertype":type}})
	
def uploadlimit(chat_id,limit):
	dbcol.update_one({"_id":chat_id},{"$set":{"uploadlimit":limit}})

def addpre(chat_id):
    date = add_date()
    dbcol.update_one({"_id":chat_id},{"$set":{"prexdate":date[0]}})

def addpredata(chat_id):
    dbcol.update_one({"_id":chat_id},{"$set":{"prexdate":None}})
    
def get_thumbnail(chat_id):
    document = dbcol.find_one({"_id": chat_id})
    if document and "file_id" in document:
        return document["file_id"]
    else:
        return None

def daily(chat_id,date):
	  dbcol.update_one({"_id":chat_id},{"$set":{"daily":date}})
	  
def find(chat_id):
	id =  {"_id":chat_id}
	x = dbcol.find(id)
	for i in x:
             file = i["file_id"]
             try:
                 caption = i["caption"]
             except:
                 caption = None
                 
             return [file, caption]

def getid():
    values = []
    for key  in dbcol.find():
         id = key["_id"]
         values.append((id)) 
    return values

def delete(id):
	dbcol.delete_one(id)
	
def find_one(id):
	return dbcol.find_one({"_id":id})

def insert_channel(chat_id, channel_name):
    channel_id = int(chat_id)
    channel_data = {"_id": channel_id, "channel_name": channel_name, "thumbnail": None}
    try:
        channel_col.insert_one(channel_data)
    except:
        pass

def set_channel_thumbnail(chat_id, file_id):
    channel_id = int(chat_id)
    channel_col.update_one({"_id": channel_id}, {"$set": {"file_id": file_id}})

def get_channel_thumbnail(chat_id):
    document = channel_col.find_one({"_id": chat_id})
    if document and "thumbnail" in document:
        return document["thumbnail"]
    else:
        return None

def delete_channel(chat_id):
    channel_col.delete_one({"_id": chat_id})

def get_channel_thumbnail(chat_id):
    document = channel_col.find_one({"_id": chat_id})
    return document.get('file_id', None)
    
