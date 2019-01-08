import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
sender = input("Enter the Email of the Sender: ")
password = input("Enter the Password of the Sender: ")
reciever = input("Enter the Email of the Reciever: ")
sub = input("Enter the subject: ")
content = input("Enter the Email Content: ")
repeat = input("Enter the number of Emails to Sent: ")
portNo = input("Enter the SMPTP Port: ")
msg = MIMEMultipart()
msg['From']=sender
msg['To']=reciever
msg['Subject']=sub
msg.attach(MIMEText(content,'plain'))
server = smtplib.SMTP('smtp.gmail.com',int(portNo))
server.ehlo()
server.starttls()
server.ehlo()
try:
    server.login(sender,password)
    for i in range(0,int(repeat)):
        server.sendmail(sender,reciever,msg.as_string())
    server.quit()
except:
    print("Some Error has Occurred!! Please retry the process")
