# Methods used
# For Getting JSON Updates (Message and Photos)
# ---------------------------------------------
# Without Offset - https://api.telegram.org/bot<AUTH-KEY>/getUpdates
# With Offset - https://api.telegram.org/bot<AUTH-KEY>/getUpdates?offset=346367962
# ---------------------------------------------

# For Sending Messages
# ---------------------------------------------
# https://api.telegram.org/bot<AUTH-KEY>/sendMessage?text=Hello%20World&chat_id=281125848
# ---------------------------------------------

# For Images
# ---------------------------------------------
# Extracting file_id: https://api.telegram.org/bot<AUTH-KEY>/getUpdates?offset=346367962
# Extracting file_path: https://api.telegram.org/bot<AUTH-KEY>/getFile?file_id=<file_id>
# Download Link: https://api.telegram.org/file/bot<AUTH-KEY>/<file_path>

import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time
import re
userSettings = {}
URL = "https://api.telegram.org/bot"
AUTH = "788145988:AAEVAR7Y_3d-JXiZkUv8pCZfvGAI_Gu7ELU"
def addUser(uid,first_name,last_name=None):    #This method adds the User Details in the Dictionary
    userSettings[uid]={}
    userSettings[uid]["fName"]=first_name
    if(last_name!=None):
        userSettings[uid]["lName"]=last_name
def addEmail(uid,email):
    userSettings[uid]["email"]=email
def addPassword(uid,password):
    userSettings[uid]["password"]=password
def extractJSON(offset=None):   #Returns the JSON Dictionary and the updated Offset Value for the getUpdates Method
    if(offset==None):
        url = URL+AUTH+"/getUpdates"
        jsonStr = requests.get(url)
        jsonDict = json.loads(jsonStr.text)
        if(len(jsonDict["result"])==0):
            pass
        elif("update_id" in jsonDict["result"][0]):
            offset = str(jsonDict["result"][0]["update_id"])
        return (jsonDict,offset)
    else:
        url = URL+AUTH+"/getUpdates?offset="+offset
        jsonStr = requests.get(url)
        jsonDict = json.loads(jsonStr.text)
        if(len(jsonDict["result"])==0):
            return (jsonDict,offset)
        else:
            return (jsonDict,str(int(offset)+1))
def sendErrorMsg(msg,uid):   #This method Sends Error Message to the User if Necessary
    text = "%20".join(msg.split(" "))
    url = URL+AUTH+"/sendMessage?text="+text+"&chat_id="+str(uid)
    requests.get(url)
def sendEmail(uid,msg,imageContent): #This Methods sends Email containing Message and Image to the Email Set by the User
    sender="telegrambot716@gmail.com"
    password="opm161.cm"
    sub="Telegram Message"
    portNo = "587"
    if("email" not in userSettings[uid]):
        sendErrorMsg("Can't send message since email is not set",uid)
        print(userSettings)
    else:
        reciever=userSettings[uid]["email"]
        msgFormatted = MIMEMultipart()
        msgFormatted["From"]=sender
        msgFormatted["To"]=reciever
        msgFormatted["Subject"]=sub
        msgFormatted.attach(MIMEText(msg,"plain"))
        if(imageContent!=None):
            msgFormatted.attach(MIMEImage(imageContent))
        server = smtplib.SMTP('smtp.gmail.com',int(portNo))
        server.ehlo()
        server.starttls()
        server.ehlo()
        try:
            server.login(sender,password)
            server.sendmail(sender,reciever,msgFormatted.as_string())
        except:
            sendErrorMsg("The Message could not be send due to some error",uid)
        server.quit()
def retName(uid):   #This Method Returns the Name of the User based on a particular User Id(uid)
    name = userSettings[uid]["fName"]
    if("last_name" in userSettings[uid]):
        return (name + " " + userSettings[uid]["lName"])
    else:
        return name
def extractFilePath(file_id):   #This Method Returns the File Path of the File by specifying the file_id
    url = URL+AUTH+"/getFile?file_id="+file_id
    filePathJson = requests.get(url)
    filePathDict = json.loads(filePathJson.text)
    return "https://api.telegram.org/file/bot"+AUTH+"/"+filePathDict["result"]["file_path"]
def onePassScan(offset=None):   #It Checks the Server once for any Updates and behaves accordingly 
    msg=""
    imageContent=None
    jsonDict,offset=extractJSON(offset)
    print("1")
    if(len(jsonDict["result"])==0):
        pass
    elif(jsonDict["result"][0]["message"]["from"]["id"] not in userSettings):
        if("last_name" in jsonDict["result"][0]["message"]["from"]):
            addUser(jsonDict["result"][0]["message"]["from"]["id"],jsonDict["result"][0]["message"]["from"]["first_name"],jsonDict["result"][0]["message"]["from"]["last_name"])
        else:
            addUser(jsonDict["result"][0]["message"]["from"]["id"],jsonDict["result"][0]["message"]["from"]["first_name"])
    else:
        emailREGX = re.compile(r"/Email[\s]*-[\s]*([\w\._+-]+@[\w\._+-]+.com)")
        if("text" in jsonDict["result"][0]["message"]):
            if(emailREGX.search(jsonDict["result"][0]["message"]["text"])!=None):
                email = emailREGX.search(jsonDict["result"][0]["message"]["text"]).group(1)
                addEmail(jsonDict["result"][0]["message"]["from"]["id"],email)
                return offset
            else:
                msg = jsonDict["result"][0]["message"]["text"]
        if("photo" in jsonDict["result"][0]["message"]):
            file_id = jsonDict["result"][0]["message"]["photo"][-1]["file_id"]
            filePath = extractFilePath(file_id)
            if("caption" in jsonDict["result"][0]["message"]):
                msg=msg+jsonDict["result"][0]["message"]["caption"]
            imageContent = requests.get(filePath,stream=True).content
        sendEmail(jsonDict["result"][0]["message"]["from"]["id"],msg+"\nMessage was sent by: "+retName(jsonDict["result"][0]["message"]["from"]["id"]),imageContent)
    return offset
def runScrypt():    #Makes the Scrypt run forever to keep the Telegram Email Bot Alive
    offset = None
    timeD=1
    while(True):
        offset = onePassScan(offset)
        time.sleep(timeD)
runScrypt() #Execution of the Bot Starts from Here
