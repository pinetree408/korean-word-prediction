# -*- coding: utf-8 -*-
from flask import render_template, session
from flask_socketio import emit

from interface import app, socketio, suggest

import os
import json
import time


@app.before_request
def before_request():
    global user_no
    if 'session' in session and 'user-id' in session:
        pass
    else:
        session['session'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/mynamespace')
def connect():
    emit("response", {
        'type': 'System',
        'data': 'Connected'
    })

@socketio.on('disconnet', namespace='/mynamespace')
def disconnect():
    session.clear()
    print "Disconnect"

@socketio.on("request", namespace='/mynamespace')
def request(message):

    start_time = time.time()
    if (message['type'] == "word"):
        predicted = json.dumps(suggest.suggestion(message['data']), ensure_ascii=False)
        input_str = suggest.input_str
    else:
        predicted = json.dumps(suggest.correction(message['data']), ensure_ascii=False)
        input_str = suggest.input_str

    print time.time() - start_time
    emit("response", {
        'type': 'Suggestion',
        'data': predicted,
        'input': input_str,
        'type': message['type']
    }, broadcast=True)
