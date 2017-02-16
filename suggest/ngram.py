# -*- coding: utf-8 -*- 
import operator
from collections import OrderedDict
from korean import hangul

def generate():
    ke = hangul.KE()

    print "set lanaguae model unigram"
    language_model_1_gram = {}
    
    with open("lm/language_model_1_gram.txt", 'r') as file_read:
        for line in file_read:
            keys = line.split(':')[0]
            if len(keys.split(' ')) != 1:
                continue
            try:
                prev_word = ke.change_complete_korean(keys.split('/')[0])
                prev_tag = keys.split('/')[1]
            except IndexError as e:
                continue

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
    with open("lm/language_model_2_gram.txt", 'r') as file_read:
	for line in file_read:
	    keys = line.split(':')[0]
	    if len(keys.split(' ')) != 2:
		continue

            try:
                prev_word = ke.change_complete_korean(keys.split(' ')[0].split('/')[0])
	        prev_tag = keys.split(' ')[0].split('/')[1]
	        next_word = ke.change_complete_korean(keys.split(' ')[1].split('/')[0])
	        next_tag = keys.split(' ')[1].split('/')[1]
            except IndexError as e:
                continue

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
    with open("lm/language_model_3_gram.txt", 'r') as file_read:
	for line in file_read:
	    keys = line.split(':')[0]
	    if len(keys.split(' ')) != 3:
		continue
            try:
	        prev_word = ke.change_complete_korean(keys.split(' ')[0].split('/')[0])
	        prev_tag = keys.split(' ')[0].split('/')[1]
	        middle_word = ke.change_complete_korean(keys.split(' ')[1].split('/')[0])
	        middle_tag = keys.split(' ')[1].split('/')[1]
	        next_word = ke.change_complete_korean(keys.split(' ')[2].split('/')[0])
	        next_tag = keys.split(' ')[2].split('/')[1]
            except IndexError as e:
                continue

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
    return [language_model_1_gram, language_model_2_gram, language_model_3_gram]

