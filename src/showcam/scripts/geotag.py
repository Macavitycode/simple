#!/bin/env python3

import rospy
from sensor_msgs.msg import Image
from mavros_msgs.msg import RCIn
from mavros_msgs.msg import GPSRAW

import cv2
import json
from cv_bridge import CvBridge

from config import config

save_dir = "/home/pi/simple/saves"
count_file = save_dir + "/count"

trigger_channel = config().trig_channel

class sub:

    def __init__(self):

        rospy.init_node("geotag_node")
        
        self.rcsub = rospy.Subscriber("/mavros/rc/in", RCIn, self.rccb)
        self.gpssub = rospy.Subscriber("/mavros/gpsstatus/gps1/raw", GPSRAW, self.gpscb)

        self.imgsub = rospy.Subscriber("/campub", Image, self.imgcb)

        self.img = None

        self.gpsmsg = None

        print("started node")

    def rccb(self, msg):
        if(msg.channels[trigger_channel - 1] > 1500):
            self.take_pic()
            print("Detected trigger")

    def gpscb(self, msg):
        self.gpsmsg = msg

    def imgcb(self, msg):
        self.img = msg

    def take_pic(self):

        f = open(count_file, "r")
        count = int(f.read())
        f.close()

        count += 1

        f = open(count_file, "w")
        f.write(str(count))
        f.close()

        if self.img is not None:

            cv_image = CvBridge().imgmsg_to_cv2(self.img, desired_encoding='passthrough')
            cv2.imwrite(save_dir + "/img_" + str(count) + ".jpg", cv_image)

            f = open(save_dir + "/data_" + str(count) + ".txt", "x")
            f.write(str(self.gpsmsg))
            f.close()

            print("Took pic ", count)


if __name__ == "__main__":

    s = sub()
    rospy.spin()
