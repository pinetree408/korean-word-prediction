# -*- coding: utf-8 -*- 
from konlpy.tag import Kkma

def run(ngram):
    language_model_1_gram = ngram[0]
    language_model_2_gram = ngram[1]
    language_model_3_gram = ngram[2]

    input_str = ""
    kkma = Kkma()
    kkma.morphs(u"initialize")

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
