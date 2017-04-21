# -*- coding: utf-8 -*- 
from konlpy.tag import Kkma
from korean import hangul
from collections import OrderedDict


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
            if len(result[0]) < 3:
                try:
                    result[0].update(self.language_model_2_gram[prev])
                    if len(result[0]) < 3:
                        result[0].update(self.language_model_1_gram)
                except KeyError as e2:
                    result[0].update(self.language_model_1_gram)
        except KeyError as e1:
            try:
                result = [self.language_model_2_gram[prev], 2]
                if len(result[0]) < 3:
                    result[0].update(self.language_model_1_gram)
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
        self.input_str = i
        final_list = []

	input_word = self.kkma.morphs(i)
	prev_word = self.ke.decompose(input_word[-1].encode("utf-8"))

	prevprev_word = ''
        if len(input_word) > 1:
            prevprev_word = self.ke.decompose(input_word[-2].encode("utf-8"))
        else:
	    if len(self.input_str.split(' ')) != 0:
		prevprev_word = self.ke.decompose(self.kkma.morphs(self.input_str.split(' ')[-1])[-1].encode("utf-8"))

        seed_morphemes = self.stupid_backoff(prevprev_word, prev_word)[0]

        for key, value in seed_morphemes.iteritems():
            now_tag_list = value['tag'].split('_')
	    result_list = [key]
            merge_list = []
            if not now_tag_list[-1][:2] in self.end_tag_list:
                self.stupid_backoff_iter(prev_word, key, now_tag_list, result_list, merge_list)
            final_list.append(merge_list)

        final_result = {}
	for index, item_list in enumerate(final_list):
            if len(final_result.keys()) == 3:
                break
	    for item in item_list:
		try:
		    changed = self.ke.compose(item)
		    if index in final_result.keys():
                        final_result[index].append(changed)
                    else:
                        final_result[index] = [changed]
		except ValueError as e:
		    continue

	return final_result

    def correction(self, i):

        if not i:
            return {}

        final_list = []

        start = self.ke.decompose(i.encode('utf-8'))

        self.input_str = i
        space_divided = self.input_str.split(' ')

        prev_word = ''
        prevprev_word = ''
        if len(space_divided) > 0:
            morphs_list = self.kkma.morphs(space_divided[-1])
            if len(morphs_list) > 1:
                prev_word = self.ke.decompose(morphs_list[-1].encode("utf-8"))
                prevprev_word = self.ke.decompose(morphs_list[-2].encode("utf-8"))
            elif len(morphs_list) == 1:
                prev_word = self.ke.decompose(morphs_list[-1].encode("utf-8"))

        seed_morphemes = self.stupid_backoff(prevprev_word, prev_word)[0]

        for key, value in seed_morphemes.iteritems():
            if not key.startswith(start):
                continue
            now_tag_list = value['tag'].split('_')
	    result_list = [key]
            merge_list = []
            if not now_tag_list[-1][:2] in self.end_tag_list:
                self.stupid_backoff_iter(prev_word, key, now_tag_list, result_list, merge_list)
            final_list.append(merge_list)

        final_result = {}
	for index, item_list in enumerate(final_list):
            if len(final_result.keys()) == 3:
                break
	    for item in item_list:
		try:
		    changed = self.ke.compose(item)
		    if index in final_result.keys():
                        final_result[index].append(changed)
                    else:
                        final_result[index] = [changed]
		except ValueError as e:
		    continue

	return final_result
