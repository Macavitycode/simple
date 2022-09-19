#!/bin/env python3

import cv2
import time

from cv_bridge import CvBridge
import numpy as np

import rospy
from sensor_msgs.msg import Image

class VideoCamera:

    def __init__(self, debug = False):

        rospy.init_node("wificam")
        
        self.imgsub = rospy.Subscriber("/campub", Image, self.imgcb)

        self.img = None
        self.debug = debug

        self.count = 0
        print("started node")

    def imgcb(self, msg):
        self.img = CvBridge().imgmsg_to_cv2(msg)

    def get_frame(self):
        ret, jpeg = cv.imencode(".jpg", self.img)
        self.previous_frame = jpeg
        return jpeg.tobytes()
