#!/usr/bin/env python3

# libraries
#from winsound import PlaySound
from std_msgs.msg import String
import cv2
from PIL import Image
import pytesseract
from gtts import gTTS
from playsound import playsound
import rospkg
import rospy
# parameters
square = 100
ancho, alto = 720, 1280
# video capture
cap = cv2.VideoCapture(0)
#cap.set(3,ancho)
#cap.set(4,alto)
while True:
    _,image = cap.read()
    cv2.imshow('Text detection',image)
    if cv2.waitKey(1) & 0xFF==ord('s'):
        cv2.imwrite('test1.jpg',image)
        break
cap.release()
cv2.destroyAllWindows()

def tesseract():
    Imagepath = 'test1.jpg'
    text = pytesseract.image_to_string(Image.open(Imagepath))
    print(text[:-1])
tesseract()