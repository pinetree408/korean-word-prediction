# -*- coding: utf-8 -*- 
from kakao import analyze
from konlpy.tag import Kkma
import operator
import os
from collections import OrderedDict

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
        if len(keys.split(' ')) != 1:
            continue

	prev_word = keys.split('/')[0]
        prev_tag = keys.split('/')[1]
        try:
	    value = int(line.split(':')[1][:-2])
        except ValueError as e:
            continue

	language_model_1_gram[prev_word] = {'tag': prev_tag, 'value': value}

sorted_value = sorted(language_model_1_gram.items(), key=lambda x: x[1]['value'])
sorted_value.reverse()
language_model_1_gram = OrderedDict(sorted_value)

print "set lanaguae model bigram"
language_model_2_gram = {}
with open("language_model_2_gram.txt", 'r') as file_read:
    for line in file_read:
        keys = line.split(':')[0]
        if len(keys.split(' ')) != 2:
            continue

        prev_word = keys.split(' ')[0].split('/')[0]
        prev_tag = keys.split(' ')[0].split('/')[1]
        next_word = keys.split(' ')[1].split('/')[0]
        next_tag = keys.split(' ')[1].split('/')[1]
	value = int(line.split(':')[1][-2])

        if prev_word in language_model_2_gram.keys():
            language_model_2_gram[prev_word][next_word] = {'tag': prev_tag + '_' + next_tag, 'value': value}
        else:
            language_model_2_gram[prev_word] = {next_word : {'tag': prev_tag + '_' + next_tag, 'value': value}}

for key, value in language_model_2_gram.iteritems():
    sorted_value = sorted(value.items(), key=lambda x: x[1]['value'])
    sorted_value.reverse()
    del language_model_2_gram[key]
    language_model_2_gram[key] = OrderedDict(sorted_value)

print "set lanaguae model trigram"
language_model_3_gram = {}
with open("language_model_3_gram.txt", 'r') as file_read:
    for line in file_read:
        keys = line.split(':')[0]
        if len(keys.split(' ')) != 3:
            continue

        prev_word = keys.split(' ')[0].split('/')[0]
        prev_tag = keys.split(' ')[0].split('/')[1]
        middle_word = keys.split(' ')[1].split('/')[0]
        middle_tag = keys.split(' ')[1].split('/')[1]
        next_word = keys.split(' ')[2].split('/')[0]
        next_tag = keys.split(' ')[2].split('/')[1]
	value = int(line.split(':')[1][-2])

        if prev_word in language_model_3_gram.keys():
            if middle_word in language_model_3_gram[prev_word].keys():
                language_model_3_gram[prev_word][middle_word][next_word] = {'tag': prev_tag + '_' + middle_tag + '_' + next_tag, 'value': value}
            else:
                language_model_3_gram[prev_word][middle_word] = {next_word : {'tag': prev_tag + '_' + middle_tag + '_' + next_tag, 'value': value}}
        else:
            language_model_3_gram[prev_word] = {middle_word : {next_word : {'tag': prev_tag + '_' + middle_tag + '_' + next_tag, 'value': value}}}

for key, value in language_model_3_gram.iteritems():
    for key1, value1 in language_model_3_gram[key].iteritems():
        sorted_value = sorted(value1.items(), key=lambda x: x[1]['value'])
        sorted_value.reverse()
        del language_model_3_gram[key][key1]
        language_model_3_gram[key][key1] = OrderedDict(sorted_value)

while True:
    i = raw_input("Enter text (or Enter to quit): ")

    if not i:
        print "--quit--"
        break

    if input_str != '':
        input_str = input_str + ' ' + i
    else:
        input_str = i

    if i == 'reset':
        input_str = ''
        print "--reset--"
	continue

    print "--now-- : " + input_str

    input_word = kkma.morphs(i.decode("utf-8"))
    prev_word = input_word[-1].encode("utf-8") 

    prevprev_word = ''
    if len(input_str) != 0:
        if len(input_word) == 1:
            prevprev_word = kkma.morphs(input_str.split(' ')[-1].decode("utf-8"))[-1].encode("utf-8")
        else:
            prevprev_word = input_word[-2].encode("utf-8")

    if prevprev_word == '':
        try:
            result = language_model_2_gram[prev_word]
        except KeyError as e1:
            result = language_model_1_gram
    else:
        try:
            result = language_model_3_gram[prevprev_word][prev_word]
        except KeyError as e1:
            try:
                result = language_model_2_gram[prev_word]
            except KeyError as e2:
                result = language_model_1_gram

    print "--result--"
    count = 0
    for key, value in result.iteritems():
        if count == 10:
            break
        print str(count) + ":" + key + '-' + str(value)
        count += 1
