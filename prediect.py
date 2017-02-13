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

print "set lanaguae model bigram"
language_model_2_gram = {}
with open("language_model_2_gram.txt", 'r') as file_read:
    for line in file_read:
        keys = line.split(':')[0]
        if len(keys.split(' ')) != 2:
            continue

        prev_word = keys.split(' ')[0]
        next_word = keys.split(' ')[1]
	value = line.split(':')[1]

        if prev_word in language_model_2_gram.keys():
            language_model_2_gram[prev_word][next_word] = value
        else:
            language_model_2_gram[prev_word] = {next_word : value}

print "set lanaguae model trigram"
language_model_3_gram = {}
with open("language_model_3_gram.txt", 'r') as file_read:
    for line in file_read:
        keys = line.split(':')[0]
        if len(keys.split(' ')) != 3:
            continue

        prev_word = keys.split(' ')[0]
        middle_word = keys.split(' ')[1]
        next_word = keys.split(' ')[2]
	value = line.split(':')[1]

        if prev_word in language_model_3_gram.keys():
            if middle_word in language_model_3_gram[prev_word].keys():
                language_model_3_gram[prev_word][middle_word][next_word] = value
            else:
                language_model_3_gram[prev_word][middle_word] = {next_word : value}
        else:
            language_model_3_gram[prev_word] = {middle_word : {next_word : value}}

while True:
    print "--now--" + input_str
    i = raw_input("Enter text (or Enter to quit): ")
    if not i:
        break
    input_word = kkma.morphs(i.decode("utf-8"))
    prev_word = input_word[-1].encode("utf-8")

    pp_word = ''
    if len(input_str) != 0:
        if len(input_word) == 1:
            pp_word = kkma.morphs(input_str.split(' ')[-1].decode("utf-8"))[-1].encode("utf-8")
        else:
            pp_word = input_word[-2].encode("utf-8")

    print pp_word

    if pp_word == '':
        result = language_model_2_gram[prev_word]
        sorted_result = sorted(result.items(), key=operator.itemgetter(1))
    else:
        try:
            result = language_model_3_gram[pp_word][prev_word]
            sorted_result = sorted(result.items(), key=operator.itemgetter(1))
        except KeyError as e:
            result = language_model_2_gram[prev_word]
            sorted_result = sorted(result.items(), key=operator.itemgetter(1))

    print "--result--"
    count = 0
    for key, value in dict(sorted_result).iteritems():
        if count == 3:
            break
        print key
        count += 1
    input_str = input_str + ' ' + i
