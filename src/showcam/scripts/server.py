#!/bin/env python3 

import flask
from cam_for_wifi import VideoCamera
import os

pi_camera = VideoCamera() # flip pi camera if upside down.

# App Globals (do not edit)
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    count = 1
    while True:
        count = (count + 1) % 10
        print("count is ", count)

        frame = camera.get_frame()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return flask.Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
