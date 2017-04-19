# -*- coding: utf-8 -*-
from flask import Flask
from flask_socketio import SocketIO
from suggest import ngram, predict
from corpus import analyze

import os

app = Flask(__name__)
app.debug = True
app.secret_key = "secret"

socketio = SocketIO(app)

if not os.path.exists('lm/'):
    os.makedirs('lm/')

#if not "language_model_1_gram.txt" in os.listdir("lm/"):
analyze.generater_parallel("target/", 'wiki')
print "finish analyze"

suggest = predict.Suggest(ngram.generate())
print "initialized"

from interface import controllers 
