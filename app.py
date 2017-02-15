# -*- coding: utf-8 -*- 
from kakao import analyze
from suggest import ngram, predict
import os

if not os.path.exists('lm/'):
    os.makedirs('lm/')

if not "language_model_1_gram.txt" in os.listdir("lm/"):
    analyze.generater("target/")
print "finish analyze"

suggest = predict.Suggest(ngram.generate())
suggest.run()
