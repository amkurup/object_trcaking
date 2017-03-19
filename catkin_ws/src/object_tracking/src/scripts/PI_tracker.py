#!/usr/bin/env python
import rospy
import std_msgs
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from object_tracking.msg import location

global ang_control
ang_control = 0.0

def callback(data):
    global ang_control
    #reference = 0
    #P = 0.001
    reference = rospy.get_param("/P_control/reference") #needs a point and a size
    P = rospy.get_param("/P_control/P_ang") #angular proportional controller
    ang_control = P*(reference - data.x)
    #rospy.loginfo('Recieved data: %s Ang-Control: %s', data.x, ang_control)
    #Define PI Controller here

def position_sub():
    rospy.Subscriber('custom_chatter', location, callback) #Detect position from OpenCV

def jackal_move():
        global ang_control
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        rospy.init_node('jackal_move', anonymous=True)
        rate = rospy.Rate(50) # 50hz
        position_sub()
	linear = Vector3(0.0, 0.0, 0.0)
	angular = Vector3(0.0, 0.0, ang_control)
        message = Twist(linear, angular)
	pub.publish(message)
        #rospy.loginfo(message)
        rate.sleep()

if __name__ == '__main__':
    while not rospy.is_shutdown():
        try:
            jackal_move()
        except rospy.ROSInterruptException:
            pass
