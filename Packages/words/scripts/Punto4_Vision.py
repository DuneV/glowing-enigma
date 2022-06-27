#!/usr/bin/env python3

import rospkg
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
import time


class ShapeDetect:
    bool = False
    frameWidth = 640
    frameHeight = 480

    desf = 75
    maxy = int(frameHeight/2) + desf
    miny = int(frameHeight/2) - desf 
    maxx = int(frameWidth/2) + desf
    minx = int(frameWidth/2) - desf 

    blue_th_min = 100 #* 255/360
    blue_th_max = 130 #* 255/360

    yellow_th_min =20 #35 * 255/360
    yellow_th_max =50 #65 * 255/360

    red_th_min = 160
    red_th_max = 180
    

    print(f"({minx},{miny}),({maxx},{maxy})")                    
    str_color = ""
    cap = cv2.VideoCapture(-1)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight) 
    #Constructor de la clase
    def __init__(self):
        rospy.Subscriber('/colorVision', String, self.callback_colorSelected)
        self.catchPublisher = rospy.Publisher('/catch', String, queue_size=10)
        rospy.spin() 

    def callback_colorSelected(self, msg):
        str_color = msg.data
        if str_color != "" and not self.bool:
            self.bool = True
            if(str_color=="yellow"):self.th_min,self.th_max=self.yellow_th_min,self.yellow_th_max
            elif(str_color=="blue"): self.th_min, self.th_max=self.blue_th_min,self.blue_th_max
            elif(str_color=="red"): self.th_min, self.th_max=self.red_th_min,self.red_th_max

            while True :
            
                success, img = self.cap.read()
                #cv2.imshow("Result", img)
                imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                imgBlur = cv2.GaussianBlur(imgGray, (17,17),1)
                img = cv2.rectangle(img, (self.minx,self.miny), (self.maxx,self.maxy), (50,122,255), 2)
                        
                circles = cv2.HoughCircles(imgBlur,cv2.HOUGH_GRADIENT,1.2 , 500,
                           param1=100,param2=30,minRadius=75,maxRadius=400)
                try: 
                    circles = np.uint16(np.around(circles))
                    for i in circles[0,:]:
                        x, y, r = i.astype(np.int32)
                        roi = img[y - r: y + r, x - r: x + r]
                        width, height = roi.shape[:2]
                        width, height = roi.shape[:2]
                        mask = np.zeros((width, height, 3), roi.dtype)
                        cv2.circle(mask, (int(width / 2), int(height / 2)), r, (255, 255, 255), -1)
                        dst = cv2.bitwise_and(roi, mask) 
                        colorProm = []

                        for i in range(3):
                            channel = dst[:, :, i]
                            indices = np.where(channel != 0)[0]
                            color = np.mean(channel[indices])
                            colorProm.append(int(color))
                                               
                        imgColor = np.ones((1,1,3), np.uint8)
                        imgColor[:,:,0] = colorProm[0] 
                        imgColor[:,:,1] = colorProm[1] 
                        imgColor[:,:,2] = colorProm[2] 
                        imgColor = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
                        colorProm = imgColor[0,0,:]

                        if (x < self.maxx and x> self.minx) and ( y>self.miny and y<self.maxy and (colorProm[0]<self.th_max and colorProm[0]>self.th_min)):
                            self.catchPublisher.publish("1")
                except:
                    pass
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        


# Main del programa, lanza el despliegue de la interfaz en el hilo principal.
if __name__ == '__main__':
    rospy.init_node('shapeDetector', anonymous=True)
    try:   
            sd = ShapeDetect() 
    except rospy.ROSInterruptException:
            pass
    
