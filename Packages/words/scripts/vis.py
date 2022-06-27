#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import cv2
from words.srv import image2string, image2stringResponse
import pytesseract
#from gtts import gTTS
#from playsound import playsound
import rospkg


# parameters

start_point = (150, 150)
end_point =(500,300)
color = (0, 0,0 )
thickness = 2

# video capture and global variables

cap = cv2.VideoCapture(0)

#cap.set(3,ancho)
#cap.set(4,alto)

# class building 

class letras: 
    def text(image):
        #def voice(file_text, language, file_name):
        #    with open(file_text,'r') as lec:
        #        lecture = lec.read()
        #    lect = gTTS(text = lecture, lang = language, slow = False)
        #    name = file_name
        #    lect.save(name)
        #pytesseract.pytesseract.tesseract_cmd = ""  (windows)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        #return image2stringResponse(text)
        #wordPublisher.publisher(word)
        print(text[:-1])
        return image2stringResponse(text)
        # reproduction voice code
        #dir = open('Info.txt','w')
        #dir.write(text)
        #dir.close()
        #voice('Info.txt','es','Voz.mp3')
        #audio = 'Voz.mp3'
        #playsound(audio)
    def __init__(self)-> None:
        rospy.init_node('i2s_service', anonymous=True)
        #self.service = rospy.Service("image2string",image2string, text) 
    while True: 
        ret, frame = cap.read()
        if ret == False: 
            break
        #cv2.putText(frame,'Ubique el texto a leer',(150,80),cv2.FONT_HERSHEY_SIMPLEX,0.71,(255,255,0),2)
        cv2.putText(frame,'Ubique el texto a leer',(200,100),cv2.FONT_HERSHEY_SIMPLEX,0.70,(0,0,0),2)
        cv2.rectangle(frame,start_point,end_point,color,thickness)
        doc = frame[start_point[1]:end_point[1], start_point[0]:end_point[0]]
        cv2.imshow('Lector Inteligente',frame)
        cv2.imwrite('prueba.jpg',doc)
        #cv2.imwrite('Imatext.jpg',frame)
        if cv2.waitKey(1) & 0xFF==ord('s'):
            #print('g')
            break
    text(doc)
    cap.release()
    cv2.destroyAllWindows()
# init code 
if __name__ == '__main__':
    try: 
        lett = letras() 
    except rospy.ROSInterruptException:
       pass