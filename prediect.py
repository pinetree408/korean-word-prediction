# -*- coding: utf-8 -*- 
from kakao import analyze
import operator

#analyze.generater("kakao/")
print "finish analyze"
input_str = ""
while True:
    print input_str
    i = raw_input("Enter text (or Enter to quit): ")
    if not i:
        break
    result = {}
    with open("language_model_2_gram.txt", 'r') as file_read:
        for line in file_read:
            item = line.split(':')[0]
            if i == item.split(' ')[0]:
                result[item.split(' ')[1]] = line.split(':')[1]
    sorted_result = sorted(result.items(), key=operator.itemgetter(1))
    print "--result--"
    for key, value in dict(sorted_result).iteritems():
        print key
    input_str = input_str + ' ' + i
