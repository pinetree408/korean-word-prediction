# -*- coding: utf-8 -*-
from suggest import ngram, predict
from corpus import analyze

import os

if __name__ == "__main__":
    if not os.path.exists('lm/'):
        os.makedirs('lm/')

    #if not "language_model_1_gram.txt" in os.listdir("lm/"):
    analyze.generater_parallel("target/", 'wiki')
    print "finish analyze"
    suggest = predict.Suggest(ngram.generate())
    print "initialized"

    def pretty_print(dic):
        for key, value in dic.iteritems():
            print key
            for item in value:
                print "---" + item.encode('utf-8')

    pretty_print(suggest.suggestion('교수님이'.decode('utf-8')))
