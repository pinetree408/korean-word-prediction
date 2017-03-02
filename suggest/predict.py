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
        self.ke = hangul.KE()
        self.input_str = ''
        self.end_tag_list = ['JK', 'JX', 'JC', 'EF', 'EC', 'ET', 'EM', 'UN', 'MA', 'MD']

    def tag_compare(self, pre_tag_list, now_tag_list):
        if len(pre_tag_list) == len(now_tag_list):
            if pre_tag_list[1:] != now_tag_list[:-1]:
                return False
        else:
            if len(pre_tag_list) > len(now_tag_list):
                if pre_tag_list[2:] != now_tag_list[:-1]:
                    return False
            else:
                if pre_tag_list != now_tag_list[:-1]:
                    return False
        return True

    def stupid_backoff(self, prevprev, prev):
        try:
            result = [self.language_model_3_gram[prevprev][prev], 3]
        except KeyError as e1:
            try:
                result = [self.language_model_2_gram[prev], 2]
            except KeyError as e2:
                result = [self.language_model_1_gram, 1]

        return result

    def stupid_backoff_iter(self, prevprev, prev, pre_tag_list, result_list, merge_list):

        result = self.stupid_backoff(prevprev, prev)

        for key, value in result[0].iteritems():
            now_tag_list = value['tag'].split('_')
            if self.tag_compare(pre_tag_list, now_tag_list) == False:
                continue

            if key in result_list:
                continue

            result_list.append(key)

            if now_tag_list[-1][:2] in self.end_tag_list:
                if len(merge_list) < 3:
                    merge_list.append(''.join(result_list))
		    del result_list[-1]
                else:
                    return
            else:
                self.stupid_backoff_iter(prev, key, now_tag_list, result_list, merge_list)

    def suggestion(self, i):

	if not i:
	    return {}

        if i.lower() == 'reset':
            self.input_str = ''
            return {}

        final_list = []

	input_word = self.kkma.morphs(i)
	prev_word = self.ke.change_complete_korean(input_word[-1].encode("utf-8"))

	prevprev_word = ''
        if len(input_word) > 1:
            prevprev_word = self.ke.change_complete_korean(input_word[-2].encode("utf-8"))
        else:
	    if len(self.input_str.split(' ')) != 0:
		prevprev_word = self.ke.change_complete_korean(self.kkma.morphs(self.input_str.split(' ')[-1])[-1].encode("utf-8"))

        seed_morphemes = self.stupid_backoff(prevprev_word, prev_word)[0]

        for key, value in seed_morphemes.iteritems():
            now_tag_list = value['tag'].split('_')
	    result_list = [key]
            merge_list = []
            self.stupid_backoff_iter(prev_word, key, now_tag_list, result_list, merge_list)
            final_list.append(merge_list)

        final_result = {}
	for index, item_list in enumerate(final_list):
            if len(final_result.keys()) == 3:
                break
	    for item in item_list:
		try:
		    changed = self.ke.change_english_to_korean(item)
		    if index in final_result.keys():
                        final_result[index].append(changed)
                    else:
                        final_result[index] = [changed]
		except ValueError as e:
		    continue

        self.input_str += ' ' + i
	return final_result
