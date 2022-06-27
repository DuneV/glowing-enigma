#!/usr/bin/env python3


# Authors: Daniel Alvarez
# Description: Control through PS4 controller publisher (using twist message)
# Project: submarine control eslave

# Libraries
import rospkg
import rospy

from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32


class Ds4Control:

    buttons=[]
    axes = []

    #Constructor de la clase
    def __init__(self):
        rospy.Subscriber('/joy', Joy, self.callback_buttonSelected)
        self.cmdPublisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.controlvel = rospy.Publisher('/con_vel', Float32, queue_size=10)
        #self.rotacion = rospy.Publisher('/rot_vel',Float32, queue_size=10)
        rospy.spin() 


    def callback_buttonSelected(self, msg):
        twistMessage = Twist()
        self.buttons = msg.buttons
        self.axes = msg.axes
        control = Float32()
        #control = 0.5

        if self.axes[7]>0:
            twistMessage.linear.x = 1.0
        elif self.axes[7]<0:
            twistMessage.linear.x = -1.0
        elif self.axes[6]<0:
            twistMessage.linear.y = -1.0
        elif self.axes[6]>0:
            twistMessage.linear.y = 1.0
        elif self.buttons[4]>0:
            twistMessage.linear.z = -1.0
        elif self.buttons[5]>0:
            twistMessage.linear.z = 1.0
        elif self.buttons[0]>0:
            control = 2.5
        elif self.buttons[1]>0:
            control = -2.5
        elif self.buttons[2]>0:
            twistMessage.angular.x = 1.0
        elif self.buttons[3]>0:
            twistMessage.angular.x = -1.0
        else:
            twistMessage.linear.x = 0
            twistMessage.linear.y = 0
            twistMessage.linear.z = 0
            twistMessage.angular.x = 0
            control = 0
        self.cmdPublisher.publish(twistMessage)
        self.controlvel.publish(control)

        #print(self.buttons)
        #print(f"Ejes: {self.axes}")
        


# Main del programa, lanza el despliegue de la interfaz en el hilo principal.
if __name__ == '__main__':
    rospy.init_node('ds4control', anonymous=True)
    try:   
            sd = Ds4Control() 
    except rospy.ROSInterruptException:
            pass
    
