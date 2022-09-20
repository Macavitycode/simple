#!/bin/env python3 

import flask
from cam_for_wifi import VideoCamera
import os
import time
from config import config

pi_camera = VideoCamera()

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

def gen(camera):
    count = 1
    while True:
        time.sleep(1/config().streamfps)
        count = (count + 1) % 10
        frame = camera.get_frame()
        # print("count is ", count)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return flask.Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
