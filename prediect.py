# -*- coding: utf-8 -*- 
from kakao import analyze
from konlpy.tag import Kkma
import operator
import os


if not "language_model_1_gram.txt" in os.listdir("./"):
    analyze.generater("kakao/")
print "finish analyze"

input_str = ""
kkma = Kkma()

print "set lanaguae model"
language_model_2_gram = {}
with open("language_model_2_gram.txt", 'r') as file_read:
    for line in file_read:
        keys = line.split(':')[0]
        if len(keys.split(' ')) != 2:
            continue
        prev_word = keys.split(' ')[0]
        next_word = keys.split(' ')[1]
	value = line.split(':')[1]
        if not prev_word in language_model_2_gram.keys():
            language_model_2_gram[prev_word] = {next_word : value}
        else:
            language_model_2_gram[prev_word][next_word] = value

while True:
    print "--now--" + input_str
    i = raw_input("Enter text (or Enter to quit): ")
    if not i:
        break

    result = language_model_2_gram[kkma.morphs(i.decode("utf-8"))[-1].encode("utf-8")]
    sorted_result = sorted(result.items(), key=operator.itemgetter(1))

    print "--result--"
    count = 0
    for key, value in dict(sorted_result).iteritems():
        if count == 3:
            break
        print key
        count += 1
    input_str = input_str + ' ' + i
