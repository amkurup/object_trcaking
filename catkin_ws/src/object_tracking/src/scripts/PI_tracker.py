import rospy
import std_msgs
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

def callback(data):
    global
    #Define PI Controller here

def position_sub():
    rospy.Subscriber('tracked_pos', Int32, callback) #Detect position from OpenCV

def jackal_move():
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        rospy.init_node('jackal_move', anonymous=True)
        rate = rospy.Rate(50) # 1hz
        position_sub()
