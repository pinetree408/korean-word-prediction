# -*- coding: utf-8 -*-
from suggest import ngram, predict
from corpus import analyze

import os

if not os.path.exists('lm/'):
    os.makedirs('lm/')

if not "language_model_1_gram.txt" in os.listdir("lm/"):
    analyze.generater("target/", 'kakao')
print "finish analyze"

suggest = predict.Suggest(ngram.generate())
print "initialized"

#print suggest.suggestion('교수님이'.decode('utf-8'))
print suggest.correction('ㄱ'.decode('utf-8'))
