#!/usr/bin/env python
import rospy
import std_msgs
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from object_tracking.msg import position

global ang_control
global lin_control
global val_recieved
val_recieved = False
ang_control = 0.0
lin_control = 0.0


class Controller:

    def callback(self, data):
        global ang_control
        global lin_control
        global val_recieved
        val_recieved = True
        #reference = 0
        #P = 0.001
        ref_pos = rospy.get_param("/P_control/ref_pos") #needs a point and a size
        ref_size = rospy.get_param("/P_control/ref_size")
        P_ang = rospy.get_param("/P_control/P_ang") #angular proportional controller
        P_lin = rospy.get_param("/P_control/P_lin") #linear proportional controller
        #Employ hysterisis for both controllers
        err_ang = ref_pos - data.x # 100 pix deadzone +-50 each side
        err_lin = ref_size - data.radius # <50 move forward, >70 move back
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.loginfo('ref_pos: %s ref_size: %s err_lin: %s err_ang: %s data.x: %s data.radius: %s', ref_pos, ref_size, err_lin, err_ang, data.x, data.radius)
        #Angular control hysterisis
        if err_ang < -50.00:
            err_ang = err_ang + 50.00
        elif err_ang > 50.00:
            err_ang = err_ang - 50.00
        else:
            err_ang = 0
        #Linear control hysterisis
        if err_lin < -10.00:
            err_lin = err_lin + 10.00
        elif err_lin > 10.00:
            err_lin = err_lin - 10.00
        else:
            err_lin = 0
        #Implement controller saturation limits if needed using ROS params

        ang_control = P_ang*err_ang
        lin_control = P_lin*err_lin
        rospy.loginfo('ref_pos: %s ref_size: %s err_lin: %s err_ang: %s', ref_pos, ref_size, err_lin, err_ang)
        #Publish Velocities
        linear = Vector3(lin_control, 0.0, 0.0)
        angular = Vector3(0.0, 0.0, ang_control)
        message = Twist(linear, angular)
        pub.publish(message)
        rospy.loginfo('Publishing Velocities')

    def __init__(self):
            rospy.Subscriber('custom_chatter', position, self.callback) #Detect position from OpenCV
            rospy.spin()

if __name__ == '__main__':
    while not rospy.is_shutdown():
        rospy.init_node('jackal_move', anonymous=True)
        try:
            c = Controller()
        except rospy.ROSInterruptException:
            pass
