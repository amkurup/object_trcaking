#!/usr/bin/env python

import rospy
import cv2
import cv_bridge
import argparse
import numpy as np
from   sensor_msgs.msg import Image
from   collections     import deque
from object_tracking.msg import position

def talker():
    pub = rospy.Publisher('custom_chatter', position, queue_size=10)
    #rospy.init_node('custom_talker', anonymous=True)
    #r = rospy.Rate(10) 
    msg = position()
    msg.x = x
    msg.y = y
    msg.radius = radius
    #while not rospy.is_shutdown():
    rospy.loginfo(msg)
    pub.publish(msg)
	#r.sleep()

counter = 0
(dX, dY) = (0, 0)
direction = ""
pts = deque(maxlen=32)
radius = 0
x = 0
y = 0

class Tracker:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        cv2.namedWindow("window1", 1)
        cv2.namedWindow("window2", 1)
        self.image_sb = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_callback)

    def image_callback(self, msg):
	global counter
	global dX
	global dY
	global direction
	global pts
	global radius
	global x
	global y
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        yellowLower = np.array([20, 100, 100], np.uint8)
        yellowUpper = np.array([30, 255, 255], np.uint8)
        mask = cv2.inRange(hsv, yellowLower, yellowUpper)
        mask = cv2.erode(mask, None, iterations=3)
        mask = cv2.dilate(mask, None, iterations=6)
        masked = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("window1", image)
        #cv2.imshow("window2", masked)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
	    cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
	    c = max(cnts, key=cv2.contourArea)
	    ((x, y), radius) = cv2.minEnclosingCircle(c)
	    M = cv2.moments(c)
	    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
	    
	    if radius > 10:
		cv2.circle(image, (int(x), int(y)), int(radius), 
                    (0, 255, 255), 2)
		cv2.circle(image, center, 5, (0, 0, 255), -1)
		pts.appendleft(center)
		talker()
       	for i in np.arange(1, len(pts)):
	    if pts[i - 1] is None or pts[i] is None:
	        continue

	    if counter >= 10 and i == 1 and pts[-10] is not None:
	        dX = pts[-10][0] - pts[i][0]
	        dY = pts[-10][1] - pts[i][1]
		#talker()
	        (dirX, dirY) = ("", "")
	        if np.abs(dX) > 20:
	            dirX = "East" if np.sign(dX) == 1 else "West"
	        if np.abs(dY) > 20:
	            dirY = "North" if np.sign(dY) == 1 else "South"
	        if dirX != "" and dirY != "":
	            direction = "{}-{}".format(dirY, dirX)
	        else:
    	            direction = dirX if dirX != "" else dirY

	    thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
	    cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)

	cv2.putText(image, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
	    0.65, (0, 0, 255), 3)
	cv2.putText(image, "x: {}, y: {}, rad: {}".format(int(x), int(y), int(radius)), 
            (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 
            0.35, (0, 0, 255), 1)

	cv2.imshow("window2", image)

        cv2.waitKey(3)
	counter += 1


rospy.init_node('Track_Marker')
Track_Marker = Tracker()
rospy.spin()


