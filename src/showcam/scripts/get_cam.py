#!/bin/env python3

"""
Captures camerastream and uploads to ros
"""

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np
import rospy
import cv2

from config import config

class cameraPub:

    def __init__(self, debug = False):

        self.camera_loc = -1
        self.publisher_name = "/campub"
        self.debug = debug
        self.cam = cv2.VideoCapture(self.camera_loc)

        rospy.init_node("get_cam_node")
        self.duration = rospy.Duration(0, round(1/config().fps * 10e8))

        self.pub = rospy.Publisher(self.publisher_name, Image, queue_size = 5)
        self.bridge = CvBridge()

        self.timer = rospy.Timer(self.duration, self.timer_cb)

        self.count = 0


    def timer_cb(self, event):
        # Take image and publish here

        status, src = self.cam.read()

        if status is not False:

            img = cv2.flip(src, 0)

            img_msg = self.bridge.cv2_to_imgmsg(img, encoding="passthrough")
            self.pub.publish(img_msg)

            self.count = (self.count + 1)%10
            if self.debug: print("Debug >> published img ", self.count)
        
        else:
            if self.debug: print("Debug >> turing cam on")


if __name__ == "__main__":
    c = cameraPub()
    rospy.spin()
