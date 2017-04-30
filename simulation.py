# -*- coding: utf-8 -*-
from suggest import ngram, predict
from corpus import analyze

def pretty_print(dic):
    for key, value in dic.iteritems():
        print key
        for item in value:
            print "---" + item.encode('utf-8')

if __name__ == "__main__":
    suggest = predict.Suggest(ngram.generate())
    test_set = '내 시계가 물에 빠졌어'.decode('utf-8')
    test_set = test_set.replace(' ', '')
    for i in range(len(test_set)):
        print test_set[:i+1].encode('utf-8')
        pretty_print(suggest.suggestion(test_set[:i+1]))
