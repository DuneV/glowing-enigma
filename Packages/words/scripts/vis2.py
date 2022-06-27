#!/usr/bin/env python3

# libraries

import rospy
import cv2
from words.srv import image2string, image2stringResponse
import pytesseract


# parameters (adjust for raspberry to improve the capacity)

start_point = (150, 150)
end_point =(500,300)
color = (0, 0,0 )
thickness = 2

#cap.set(3,ancho)
#cap.set(4,alto)

# callback service

def text(request):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    #cv2.putText(frame,'Ubique el texto a leer',(200,100),cv2.FONT_HERSHEY_SIMPLEX,0.70,(0,0,0),2)
    #cv2.rectangle(frame,start_point,end_point,color,thickness)
    doc = frame[start_point[1]:end_point[1], start_point[0]:end_point[0]]
    #cv2.imshow('Lector Inteligente',frame)
    cv2.imwrite('prueba.jpg',doc)
    if request.input == True:
        gray = cv2.cvtColor(doc, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        #wordPublisher.publisher(word)
        #print(text[:-1])
        return image2stringResponse(text)
    # rospy.sleep(1)
    cap.release()
    cv2.destroyAllWindows()
        # reproduction voice code
        #dir = open('Info.txt','w')
        #dir.write(text)
        #dir.close()
        #voice('Info.txt','es','Voz.mp3')
        #audio = 'Voz.mp3'
        #playsound(audio)


class letras:
    rospy.init_node("i2s_service", anonymous=True)
    service = rospy.Service("image2string",image2string, text)
    rate = rospy.Rate(10)
    rospy.spin()

# init code
 
if __name__ == '__main__':
    try:
        lett = letras()
    except rospy.ROSInterruptException:
            pass 