#!/usr/bin/env python
import rospy
import std_msgs
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from object_tracking.msg import position

global ang_control
global lin_control
ang_control = 0.0
lin_control = 0.0

def callback(data):
    global ang_control
    global lin_control
    #reference = 0
    #P = 0.001
    ref_pos = rospy.get_param("/P_control/ref_pos") #needs a point and a size
    ref_size = rospy.get_param("/P_control/ref_size")
    P_ang = rospy.get_param("/P_control/P_ang") #angular proportional controller
    P_lin = rospy.get_param("/P_control/P_lin") #linear proportional controller
    #Employ hysterisis for both controllers
    err_ang = ref_pos - data.x # 100 pix deadzone +-50 each side
    err_lin = ref_size - data.radius # <50 move forward, >70 move back

    #Angular control hysterisis
    if err_ang < (-50.00):
        err_ang = err_ang + 50.00
    elif err_ang > (50.00):
        err_ang = err_ang - 50.00
    else:
        err_ang = 0

    #Linear control hysterisis
    if err_lin < (-10.00):
        err_lin = err_lin + 10.00
    elif err_lin > (10.00):
        err_lin = err_lin - 10.00
    else:
        err_lin = 0
    
    #Implement controller saturation limits if needed using ROS params

    ang_control = P_lin*err_ang
    lin_control = P_lin*err_lin
    #rospy.loginfo('Recieved data: %s Ang-Control: %s', data.x, ang_control)
    #Define PI Controller here

def position_sub():
    rospy.Subscriber('custom_chatter', position, callback) #Detect position from OpenCV

def jackal_move():
        global ang_control
        global lin_control
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        rospy.init_node('jackal_move', anonymous=True)
        rate = rospy.Rate(50) # 50hz
        position_sub()
	linear = Vector3(lin_control, 0.0, 0.0)
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
