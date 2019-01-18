import cv2
capture = cv2.VideoCapture(0)
frameCascadeClassifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
while(True):
    ret,frame = capture.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = frameCascadeClassifier.detectMultiScale(frame_gray,scaleFactor=1.05,minNeighbors=5)
    for x,y,z,w in faces:
        frame=cv2.rectangle(frame,(x,y),(x+z,y+w),(0,0,255),2)
        cv2.imshow("Frame",frame)
        cv2.waitKey(1)
cv2.destroyAllWindows()
    
    
