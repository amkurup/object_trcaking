#!/usr/bin/env python

# Use joystick input to launch object-tracking nodes in jackal
# 
# Intro to Robotics - EE5900 - Spring 2017
#          Assignment #6
#
#       Project #6 Group #2
#             Prithvi
#              Aswin
#         Akhil (Team Lead)
#

# define imports
import rospy
import roslaunch
import sys
import time
import os
# import tracker_proto

from   sensor_msgs.msg import Joy

# class to read joystick messages and launch node
class joy_control(object):
    # define self routine
    def __init__(self):
        # define subscriber
        rospy.Subscriber("/bluetooth_teleop/joy", Joy, self.joy_callback)
        rate = rospy.Rate(5)

        # define and init variables
        self.trigger     = False
        self.track_mode  = 0
        tracking_process = None

        while not rospy.is_shutdown():
            # execute if triggered
            if (self.trigger == True):
                if (self.track_mode == 1):
                    # "load" the tracking routine
                    package = 'object_tracking'
                    executable = 'tracker_proto.py'
                    
                    # run the tracking routine
                    node = roslaunch.core.Node(package, executable)
                    launch = roslaunch.scriptapi.ROSLaunch()
                    launch.start()
                    tracking_process = launch.launch(node)

            # else:
            # some code here..
            # some code here..

            # self.trigger = False
            #rate.sleep()

    def joy_callback(self, data):
        # define joystick buttons
        x, circ, sq, tri, L1, R1, share, options, p4, L3, R3, DL, DR, DU, DD = data.buttons
        llr, lud, L2, rlr, rud, R2 = data.axes
        
        # Start object tracking
        if (circ == 1) and (self.track_mode == 0):
            rospy.loginfo("Starting the object tracking routine...")
            self.trigger = True
            self.track_mode = 1

        # Stop tracking
        if (x == 1) and (self.trigger == True):
            rospy.loginfo("Terminating the routine...")
            self.trigger = False
        

if __name__ == "__main__":
    try:
        rospy.init_node("joy_start", anonymous=False)
        #read in joystick input
        run = joy_control()
    except rospy.ROSInterruptException:
        rospy.loginfo("joy_start node terminated.")

