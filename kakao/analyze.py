# -*- coding: utf-8 -*-
import os
from konlpy.tag import Kkma, Hannanum
import re

def tag_word_pair(item_list):
    result = []
    for item in item_list:
        result.append(item[0].encode('utf-8') + '/' + item[1].encode('utf-8'))
    return ' '.join(result)

def update_dict(dictionary, item):
    if item in dictionary.keys():
        updated = dictionary[item]
        del dictionary[item]
        dictionary[item] = updated + 1
    else:
        dictionary[item] = 1

def generater(target_path):
    target_list = [f for f in os.listdir(target_path) if ".csv" in f or ".txt" in f]
    print target_list
    kkma = Kkma()
    #hannanum = Hannanum()

    file_write_1 = open("lm/language_model_1_gram.txt", 'w')
    file_write_2 = open("lm/language_model_2_gram.txt", 'w')
    file_write_3 = open("lm/language_model_3_gram.txt", 'w')

    language_model_1_gram = {}
    language_model_2_gram = {}
    language_model_3_gram = {}

    for target in target_list:
        with open(target_path+target, 'r') as file_read:
            for line in file_read:
                if line[0] == '-':
                    continue
                else:
                    splitted = line.split(']')
                    if len(splitted) != 3:
                        continue

                line = splitted[2].strip()

                reg = re.compile(r"[ 가-힣]+")
                subed = reg.sub('', line)
                if len(subed) != 0:
                    continue

                try:
                    item_list = kkma.pos(line.decode('utf-8'))
                    #item_list = hannanum.pos(line.decode('utf-8'), ntags=22)
                except Exception as e:
                    continue
                for i, item in enumerate(item_list):
                    # 1 gram
                    uni_item = tag_word_pair([item])
                    update_dict(language_model_1_gram, uni_item)

                    # 2 gram
                    if i != len(item_list) - 1:
                        bi_item = tag_word_pair([item, item_list[i+1]])
                        update_dict(language_model_2_gram, bi_item)

                    # 3 gram
                    if i < len(item_list) - 2:
                        tri_item = tag_word_pair([item, item_list[i+1], item_list[i+2]])
                        update_dict(language_model_3_gram, tri_item)

    for key, value in language_model_1_gram.iteritems():
        file_write_1.write(key + ':' + str(value) + "\n")
    for key, value in language_model_2_gram.iteritems():
        file_write_2.write(key + ':' + str(value) + "\n")
    for key, value in language_model_3_gram.iteritems():
        file_write_3.write(key + ':' + str(value) + "\n")

    file_write_1.close()
    file_write_2.close()
    file_write_3.close()
