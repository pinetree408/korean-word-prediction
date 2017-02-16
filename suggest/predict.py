# -*- coding: utf-8 -*- 
from konlpy.tag import Kkma
from korean import hangul

class Suggest(object):

    def __init__(self, ngram):
        self.language_model_1_gram = ngram[0]
        self.language_model_2_gram = ngram[1]
        self.language_model_3_gram = ngram[2]
        self.kkma = Kkma() 
	self.kkma.morphs(u"initialize")
        self.max_iter = 10
        self.ke = hangul.KE()

    def stupid_backoff(self, prevprev_word, prev_word):
        try:
            result = [self.language_model_3_gram[prevprev_word][prev_word], 3]
        except KeyError as e1:
            try:
                result = [self.language_model_2_gram[prev_word], 2]
            except KeyError as e2:
                result = [self.language_model_1_gram, 1]

        return result

    def stupid_backoff_iter(self, tag, prevprev, prev, indent_str, iter_count, korean_word, iter_list, final_list):
        if iter_count == self.max_iter:
            return

        result = self.stupid_backoff(prevprev, prev)

        count = 0
        #if result[1] == 1:
        #    return

        for key, value in result[0].iteritems():
            #if value['tag'].split('_')[:-1] != tag.split('_')[1:]:
	    #    continue

            if count == 5:
                break
            print indent_str + ':' + key + '-' + str(value)
            if iter_list[-1][-1] + 1 == iter_count:
	        korean_word[-1].append(korean_word[-1][-1] + key)
            else:
                if not korean_word[-1][-1] in final_list[-1]:
                    final_list[-1].append(korean_word[-1][-1])
                for index, item in reversed(list(enumerate(iter_list[-1]))):
                    if item + 1 == iter_count:
	                korean_word[-1].append(korean_word[-1][index] + key)

            iter_list[-1].append(iter_count)        

            if not value['tag'].split('_')[-1][:2] in ['JK', 'JX', 'JC', 'EF', 'EC', 'ET', 'EM', 'UN', 'MA', 'MD']:
                if not value['tag'] == 'NNG_NNG_NNG':
	            self.stupid_backoff_iter(value['tag'], prev, key, indent_str + '----', iter_count + 1, korean_word, iter_list, final_list);
                else:
                    if not korean_word[-1][-1] in final_list[-1]:
                        final_list[-1].append(korean_word[-1][-1])
            else:
                if not korean_word[-1][-1] in final_list[-1]:
                    final_list[-1].append(korean_word[-1][-1])
            count += 1

    def run(self):

	input_str = ""

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

	    input_word = self.kkma.morphs(i.decode("utf-8"))
	    prev_word = self.ke.change_complete_korean(input_word[-1].encode("utf-8"))

	    prevprev_word = ''
	    if len(input_str) != 0:
		if len(input_word) == 1:
		    prevprev_word = self.ke.change_complete_korean(self.kkma.morphs(input_str.split(' ')[-1].decode("utf-8"))[-1].encode("utf-8"))
		else:
		    prevprev_word = self.ke.change_complete_korean(input_word[-2].encode("utf-8"))

	    if prevprev_word == '':
		try:
		    result = (self.language_model_2_gram[prev_word], 2)
		except KeyError as e1:
		    result = (self.language_model_1_gram, 1)
	    else:
		result = self.stupid_backoff(prevprev_word, prev_word)

	    print "--result--"
	    count = 0
            korean_word = []
            iter_list = []
            final_list = []
	    for key, value in result[0].iteritems():
		if count == 10:
		    break
		print '\n' + str(count) + ":" + key + '-' + str(value)
                korean_word.append([key])
                iter_list.append([-1])
                final_list.append([])
                if not value['tag'].split('_')[-1][:2] in ['JK', 'JX', 'JC', 'EF', 'EC', 'ET', 'EM', 'UN', 'MA', 'MD'] and not result[1] == 1:
                    self.stupid_backoff_iter(value['tag'], prev_word, key, "----", 0, korean_word, iter_list, final_list)
                    if len(final_list[-1]) == 0:
                        final_list[-1].append(key)
                else:
                    final_list[-1].append(key)
		count += 1
            for i, item_list in enumerate(final_list):
                print "rank : " + str(i)
                for j, item in enumerate(item_list):
                    try:
                        print "    " + self.ke.change_english_to_korean(item).encode('utf-8')
                    except ValueError as e:
                        continue
