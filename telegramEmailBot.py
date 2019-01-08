import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import re
userSettings = {}
URL = "https://api.telegram.org/bot"
AUTH = "788145988:AAEVAR7Y_3d-JXiZkUv8pCZfvGAI_Gu7ELU"
def addUser(uid,first_name,last_name=None):
    userSettings[uid]={}
    userSettings[uid]["fName"]=first_name
    if(last_name!=None):
        userSettings[uid]["lName"]=last_name
    #userSettings[uid]["email"]=email
    #userSettings[uid]["password"]=password
def addEmail(uid,email):
    userSettings[uid]["email"]=email
def addPassword(uid,password):
    userSettings[uid]["password"]=password
def extractJSON(offset=None):
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
def sendErrorMsg(msg,uid):
    text = "%20".join(msg.split(" "))
    url = URL+AUTH+"/sendMessage?text="+text+"&chat_id="+str(uid)
    requests.get(url)
def sendEmail(uid,msg):
    sender="abcd@def.com" #Put the sender email here
    password="xxxxxxxxxxx" #Put the sender passoword here
    sub="Telegram Message"
    portNo = "587"
    if("email" not in userSettings[uid]):
        sendErrorMsg("Can't send message since email is not set",uid)
    else:
        reciever=userSettings[uid]["email"]
        msgFormatted = MIMEMultipart()
        msgFormatted["From"]=sender
        msgFormatted["To"]=reciever
        msgFormatted["Subject"]=sub
        msgFormatted.attach(MIMEText(msg,"plain"))
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
def retName(uid):
    name = userSettings[uid]["fName"]
    if("last_name" in userSettings[uid]):
        return (name + " " + userSettings[uid]["lName"])
    else:
        return name
def onePassScan(offset=None):
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
        if(emailREGX.search(jsonDict["result"][0]["message"]["text"])!=None):
            email = emailREGX.search(jsonDict["result"][0]["message"]["text"]).group(1)
            addEmail(jsonDict["result"][0]["message"]["from"]["id"],email)     
        else:
            msg = jsonDict["result"][0]["message"]["text"]
            sendEmail(jsonDict["result"][0]["message"]["from"]["id"],msg+"\nMessage was sent by: "+retName(jsonDict["result"][0]["message"]["from"]["id"]))
    return offset
def runScrypt():
    offset = None
    timeD=1
    while(True):
        offset = onePassScan(offset)
        time.sleep(timeD)
runScrypt()
