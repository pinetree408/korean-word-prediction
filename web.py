# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from suggest import ngram, predict
from corpus import analyze

import json

app = Flask(__name__)
app.debug = True
app.secret_key = "secret"
socketio = SocketIO(app)

if not os.path.exists('lm/'):
    os.makedirs('lm/')

if not "language_model_1_gram.txt" in os.listdir("lm/"):
    analyze.generater("target/", 'kakao')
print "finish analyze"


suggest = predict.Suggest(ngram.generate())
print "initialized"

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
    
    emit("response", {
        'type': 'Suggestion',
        'data': json.dumps(suggest.suggestion(message['data']), ensure_ascii=False),
        'input': suggest.input_str,
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
