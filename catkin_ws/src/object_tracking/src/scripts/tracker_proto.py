#!/usr/bin/env python

import rospy
import cv2
import cv_bridge
import argparse
import numpy as np
from   sensor_msgs.msg import Image
from   collections     import deque


class Tracker:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv2.namedWindow("window1", 1)
        cv2.namedWindow("window2", 1)
        self.image_sb = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_callback)

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        yellowLower = np.array([20, 100, 100], np.uint8)
        yellowUpper = np.array([30, 255, 255], np.uint8)
        mask = cv2.inRange(hsv, yellowLower, yellowUpper)
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=6)
        masked = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("window1", image)
        cv2.imshow("window2", masked)
        cv2.waitKey(3)


rospy.init_node('Track_Marker')
Track_Marker = Tracker()
rospy.spin()


