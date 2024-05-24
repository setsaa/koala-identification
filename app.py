""" Koala Identification App

This app is designed to connect a live feed from a drone to an AI model that
can identify koalas in the feed. The app will then display the feed with
bounding boxes around the koalas.
"""
from flask import Flask, render_template, Response, jsonify, session

from camera_feed import generate_frames, set_tracking

app = Flask(__name__, static_url_path='/static')
app.secret_key = '1234'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_tracking', methods=['POST'])
def start_tracking_route():
    print('Received package to start tracking')
    set_tracking(True)
    session['tracking'] = True
    return jsonify({'status': 'Tracking started'})


@app.route('/stop_tracking', methods=['POST'])
def stop_tracking_route():
    print('Received package to stop tracking')
    set_tracking(False)
    session['tracking'] = False
    return jsonify({'status': 'Tracking stopped'})


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True) 
