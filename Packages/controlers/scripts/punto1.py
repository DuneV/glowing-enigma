#!/usr/bin/env python3
import rospy

from pynput import keyboard as kb
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class control:

    def __init__(self) -> None:
        #Publisher
        self.cmdPublisher = rospy.Publisher('/turtlebot_cmdVel', Twist, queue_size=10)
        
        print('Ingrese el valor de la velocidad: ')
        self.vel_linear = float(input())
        print('Submarisco listo! ')

    def pressKey(self, key):
        """
        Callback for kb.LIstener: It is called when a key is pressed and depending on the key that is pressed
        a Twist message is published in the cmd_vel topic.
        """
        twistMessage = Twist()
        if key == kb.KeyCode.from_char('w'):
            twistMessage.linear.y = self.vel_linear
        elif key == kb.KeyCode.from_char('s'):
            twistMessage.linear.y =  -self.vel_linear
        elif key == kb.KeyCode.from_char('a'):
            twistMessage.linear.x = self.vel_linear
        elif key == kb.KeyCode.from_char('d'):
            twistMessage.linear.x = -self.vel_linear
        elif key == kb.KeyCode.from_char('z'):
            twistMessage.linear.z = self.vel_linear
        elif key == kb.KeyCode.from_char('x'):
            twistMessage.linear.z = -self.vel_linear
        self.cmdPublisher.publish(twistMessage)
    
    def releaseKey(self, key):
        """
        Callback for kb.Listener: It is called when a key is released and a Twist message with all the parameters
        in 0 is published.
        """
        twistMessage = Twist()
        self.cmdPublisher.publish(twistMessage)

if __name__ == '__main__':
    rospy.init_node('punto1')
    punto1 = control()
    with kb.Listener(punto1.pressKey, punto1.releaseKey) as escuchador:
        escuchador.join()
    rospy.spin()