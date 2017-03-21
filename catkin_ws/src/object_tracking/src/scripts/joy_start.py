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

from   sensor_msgs.msg import Joy

# class to read joystick messages and launch node
class joy_control(object):

    # define self routine
    def __init__(self):

        # define subscriber
        rospy.Subscriber("/bluetooth_teleop/joy", Joy, self.joy_callback)
        rate = rospy.Rate(5)

        rospy.loginfo('started joystick routine..')

        # define and init variables
        self.start = False
        self.stop  = False

        # configure uuid as per roslaunch api
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        # declare launch file
        launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/rsestudent/object_trcaking/catkin_ws/src/object_tracking/src/launch/object_tracking.launch"])

        while not rospy.is_shutdown():
            # if start flag set: launch main launch-file
            if self.start:
                launch.start()

            # if stop flag set: shutdown main launch-file
            if self.stop:
                launch.shutdown()

            # reset trigger
            self.start = False
            self.stop  = False
            rate.sleep()


    # joystick callback routine
    def joy_callback(self, data):

        # define joystick buttons
        x, circ, sq, tri, L1, R1, share, options, p4, L3, R3, DL, DR, DU, DD = data.buttons
        llr, lud, L2, rlr, rud, R2 = data.axes

        # Start object tracking
        if (circ == 1) and (self.start == False):
            rospy.loginfo("Starting the object tracking routine...")
            self.start = True

        # Stop tracking
        if (x == 1):
            rospy.loginfo("Terminating the routine...")
            self.start = False
            self.stop  = True


# standard boilerplate
if __name__ == "__main__":
    try:
        rospy.init_node("joy_start", anonymous=False)
        #read in joystick input
        run = joy_control()
    except rospy.ROSInterruptException:
        rospy.loginfo("joy_start node terminated.")
