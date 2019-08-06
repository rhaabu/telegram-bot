'''
Created on 10 Apr 2019
@author: rain
'''

import json
import time
from requests import post
from requests import get

class User:
    def __init__(self, email, location, chatid):
        self.email = email
        self.location = location
        self.chatID = chatid

def sendImage(chatId, path):
	post('https://api.telegram.org/bot' + botToken + '/sendPhoto', 
	data={'chat_id': chatId}, 
	files={'photo': (path, open(path, "rb"))})

def sendMsg(chatId, msg):
	post('https://api.telegram.org/bot' + botToken + '/sendMessage', 
	data={'chat_id': chatId, 'text': msg})

def addNewUser(newUser):
	usersList.append(newUser)
	usersFile = open(usersFileName, 'a+')
	usersFile.write(newUser.email + "," + newUser.location + "," + newUser.chatID + '\n')
	usersFile.close()
	sendMsg(newUser.chatID, 'Email: ' + newUser.email + ' location: ' + newUser.location + ', has been successfully added to the list!')
		
#constants
botToken = '' #telegram bot token is declared here
joinCmd = 'join'
takePhotoCmd = 'takephoto'	
usersFileName = 'users.txt'
#create file which contains users chat id, email and location if it does not exist
usersFile = open(usersFileName, 'a+')
usersFile.close()
#read user string from users file with removed new line symbols and convert to User object
usersList = []
for userString in open(usersFileName):
	userParams = userString.rstrip('\n').split(',')
	usersList.append(User(userParams[0], userParams[1], userParams[2]))
# get most recent update_id
lastUpdateResult = get('https://api.telegram.org/bot' + botToken + '/getUpdates',  data={'offset':-1}).json().get('result')
lastUpdateId = lastUpdateResult[0]['update_id'] if len(lastUpdateResult) != 0 else -2

while True:
	# polling for a new update
	time.sleep(2)
	lastUpdateResult = get('https://api.telegram.org/bot' + botToken + '/getUpdates',  data={'offset':lastUpdateId + 1}).json().get('result')
	if (len(lastUpdateResult) != 0):
		lastUpdateId = lastUpdateResult[0]['update_id']
		lastUpdateChatId = str(lastUpdateResult[0]['message']['chat']['id'])
		lastUpdateMsg = lastUpdateResult[0]['message']['text'].split()
		#HANDLE COMMANDS FROM USER HERE
		if lastUpdateMsg[0] == joinCmd:
			if len(lastUpdateMsg) == 3:
				addNewUser(User(lastUpdateMsg[1], lastUpdateMsg[2], lastUpdateChatId))
			else:
				sendMsg(lastUpdateChatId, "Invalid parameters count: " + str(len(lastUpdateMsg)) + " (3 parameters required)")
		elif lastUpdateMsg == takePhotoCmd:
			for chatId in usersList:
				if chatId == lastUpdateChatId:
					#SEND PHOTO TO USER HERE
					sendImage(lastUpdateChatId, 'image.jpg')
