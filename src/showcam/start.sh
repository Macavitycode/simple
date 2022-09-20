#!/bin/bash

rm /home/pi/simple/saves/count
echo "0" >> /home/pi/simple/saves/count
source /home/pi/simple/source_this.sh
roslaunch showcam all.launch
