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
kkma.morphs(u"initialize")


print "set lanaguae model unigram"
language_model_1_gram = {}
with open("language_model_1_gram.txt", 'r') as file_read:
    for line in file_read:
	keys = line.split(':')[0]
	if len(keys.split(' ')) != 2:
	    continue

	prev_word = keys
	value = line.split(':')[1]

	language_model_1_gram[prev_word] = value

sorted_value = sorted(language_model_1_gram.items(), key=operator.itemgetter(1))
language_model_1_gram = dict(sorted_value)

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

for key, value in language_model_2_gram.iteritems():
    sorted_value = sorted(value.items(), key=operator.itemgetter(1))
    del language_model_2_gram[key]
    language_model_2_gram[key] = dict(sorted_value)

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

for key, value in language_model_3_gram.iteritems():
    for key1, value1 in language_model_3_gram[key].iteritems():
        sorted_value = sorted(value1.items(), key=operator.itemgetter(1))
        del language_model_3_gram[key][key1]
        language_model_3_gram[key][key1] = dict(sorted_value)

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

    if pp_word == '':
        result = language_model_2_gram[prev_word]
    else:
        try:
            result = language_model_3_gram[pp_word][prev_word]
        except KeyError as e1:
            try:
                result = language_model_2_gram[prev_word]
            except KeyError as e2:
                result = language_model_1_gram

    print "--result--"
    for key, value in result.iteritems():
        print key
    input_str = input_str + ' ' + i
