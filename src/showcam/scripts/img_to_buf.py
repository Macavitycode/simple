#!/bin/env python3

import cv2

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class sub:

    def __init__(self, debug = False):

        rospy.init_node("display_node")
        
        self.imgsub = rospy.Subscriber("/campub", Image, self.imgcb)

        self.img = None
        self.debug = debug

        self.count = 0
        print("started node")

    def imgcb(self, msg):
        self.img = msg
        self.write_to_buf()

    def write_to_buf(self):

        if self.img is not None:

            pic = CvBridge().imgmsg_to_cv2(self.img, desired_encoding="passthrough")
            frame = cv2.cvtColor(pic, cv2.COLOR_BGR2BGRA)
            fb = cv2.resize(frame, (1600, 900))

            with open("/dev/fb0", "rb+") as buf:
                buf.write(fb)
                buf.close()

            self.count = (self.count + 1) % 10

            if self.debug: print("wrote_pic ", count)

        if self.debug: print("no pic", count)


if __name__ == "__main__":

    s = sub()
    rospy.spin()
