#!/bin/env python3

import rospy
from mavros_msgs.msg import RCIn
from mavros_msgs.msg import GPSRAW

import cv2
import json

save_dir = "/home/pi/ros/saves"
count_file = save_dir + "/count"

trigger_channel = 6

class sub:

    def __init__(self):

        rospy.init_node("geotag_node")
        
        self.rcsub = rospy.Subscriber("/mavros/rc/in", RCIn, self.rccb)
        self.gpssub = rospy.Subscriber("/mavros/gpsstatus/gps1/raw", GPSRAW, self.gpscb)

        self.gpsmsg = None

        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        
        print("started node")

    def rccb(self, msg):
        if(msg.channels[trigger_channel - 1] > 1500):
            self.take_pic()
            print("Detected trigger")

    def gpscb(self, msg):
        self.gpsmsg = msg

    def take_pic(self):

        cap = cv2.VideoCapture(0)
        _, frame = cap.read()

        f = open(count_file, "r")
        count = int(f.read())
        f.close()

        count += 1

        f = open(count_file, "w")
        f.write(str(count))
        f.close()

        if _ and frame is not None:
            cv2.imwrite(save_dir + "/img_" + str(count) + ".jpg", frame)

            f = open(save_dir + "/data_" + str(count) + ".txt", "x")
            f.write(str(self.gpsmsg))
            f.close()

            print("Took pic ", count)

	cap.release()
	
if __name__ == "__main__":

    s = sub()
    rospy.spin()
