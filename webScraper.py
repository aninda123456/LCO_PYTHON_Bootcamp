import requests
import bs4
from PIL import Image
import matplotlib.pyplot as plot
url = input("Enter the Website URL: ")
webCode = requests.get(url)
soup = bs4.BeautifulSoup(webCode.text,'lxml')
imgTags = soup.find_all('img')
j=0
for i in imgTags:
    try:
       imgRAW = requests.get(i['src'],stream=True)
       imgfile = Image.open(imgRAW.raw)
       imgfile.save(str(j)+".jpg")
       j+=1
    except:
        print("Error")
   
   




