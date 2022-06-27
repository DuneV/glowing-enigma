#!/usr/bin/env python3  

#import roslib; roslib.load_manifest('smach_ros') 
# Authors: Daniel Alvarez and Santiago Ortiz
# Description: StateMachine robot turtlebot
# Project: robot control autonomus

#libraries
import rospy
import smach
import smach_ros


from smach import State
from std_msgs.msg import String
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist


class WaitForColor(smach.State):
    def __init__(self, outcomes=['succeeded', 'failed'], output_keys=['color']):
        self.color = None
        self.colorSubscriber = rospy.Subscriber('/color', String, self.callback_color_subscriber)

    def callback_color_subscriber(self, msg):
        self.color = msg.data

    def execute(self, userdata):
        while(self.color is None):
            rospy.sleep(0.1)
        if self.color in ['yellow', 'green', 'red']:
            userdata.color=self.color
            return 'succeeded'
        else:
            return 'failed'

class SendColor(smach.State):
    def __init__(self, outcomes=['succeeded'], input_keys=['color']):
        self.colorPublisher = rospy.Publisher('/colorVision', String, queue_size=10)

    def execute(self, userdata):
        self.colorPublisher.publish(userdata.color)
        return 'succeeded'

class WaitForRightColor(smach.State):
    def __init__(self, outcomes=['succeeded']):
        self.catch=0
        self.catchSubscriber = rospy.Subscriber('/catch', Int16, self.callback_catch_subscriber)
        self.cmd_velPublisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def callback_catch_subscriber(self, msg):
        self.catch = msg.data

    def execute(self, userdata):
        twistMessage = Twist()
        twistMessage.linear.x = 1
        while(self.catch == 0):
            self.cmd_velPublisher.publish(twistMessage)
            rospy.sleep(0.1)
        twistMessage = Twist()
        self.cmd_velPublisher.publish(twistMessage)
        return 'succeeded'

class CatchObject(smach.State):
    def __init__(self, outcomes=['succeeded']):
        self.manipulatorPublisher = rospy.Publisher('/manipulator', String, queue_size=10)

    def execute(self, userdata):
        self.manipulatorPublisher.publish("x")
        rospy.sleep(2)
        duration = rospy.Duration(2)
        beginTime = rospy.Time.now()
        endTime = beginTime + duration
        while rospy.Time.now() < endTime:
            self.manipulatorPublisher.publish("i")
            rospy.sleep(0.1)
        self.manipulatorPublisher.publish("z")
        rospy.sleep(2)
        duration = rospy.Duration(2)
        beginTime = rospy.Time.now()
        endTime = beginTime + duration
        while rospy.Time.now() < endTime:
            self.manipulatorPublisher.publish("k")
            rospy.sleep(0.1)

# main
def main():
    rospy.init_node('state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['finaloutcome'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('WAITFORCOLOR', WaitForColor(), 
                               transitions={'succeeded':'BAR', 
                                            'failed':'outcome4'})
        smach.StateMachine.add('SENDCOLOR', SendColor(), 
                               transitions={'succeeded':'WAITFORRIGHTCOLOR'})

        smach.StateMachine.add('WAITFORRIGHTCOLOR', WaitForRightColor(), 
                               transitions={'succeeded':'CATCHOBJECT'})

        smach.StateMachine.add('CATCHOBJECT', CatchObject(), 
                               transitions={'succeeded':'finaloutcome'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()
