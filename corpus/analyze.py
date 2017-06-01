# -*- coding: utf-8 -*-
import os
from konlpy.tag import Kkma
import re
from multiprocessing import Process

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

def generater(target_path, option):
    target_list = [f for f in os.listdir(target_path) if ".csv" in f or ".txt" in f]
    print target_list
    kkma = Kkma()

    file_write_1 = open("lm/language_model_1_gram.txt", 'w')
    file_write_2 = open("lm/language_model_2_gram.txt", 'w')
    file_write_3 = open("lm/language_model_3_gram.txt", 'w')

    language_model_1_gram = {}
    language_model_2_gram = {}
    language_model_3_gram = {}

    for target in target_list:
        with open(target_path+target, 'r') as file_read:
            for line in file_read:

                if option == 'kakao':
                    if line[0] == '-':
                        continue
                
                    splitted = line.split(']')
                    if len(splitted) != 3:
                        continue

                    line = splitted[2].strip()
                elif option == 'wiki':
                    line = line[:-2]

                reg = re.compile(r"[ 가-힣]+")
                subed = reg.sub('', line)
                if len(subed) != 0:
                    continue

                try:
                    item_list = kkma.pos(line.decode('utf-8'))
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

def generater_unit(index, lines, option):

    print "start : " + str(index) 
    kkma = Kkma()

    with open("lm_raw/uni/unigram_raw_" + str(index) + ".txt", "w") as unigram_file,\
        open("lm_raw/bi/bigram_raw_" + str(index) + ".txt", "w") as bigram_file,\
        open("lm_raw/tri/trigram_raw_" + str(index) + ".txt", "w") as trigram_file:

        for line in lines:
            if option == 'kakao':
                if line[0] == '-':
                    continue
            
                splitted = line.split(']')
                if len(splitted) != 3:
                    continue

                line = splitted[2].strip()
            elif option == 'wiki':
                line = line[:-2]

            reg = re.compile(r"[ 가-힣]+")
            subed = reg.sub('', line)
            if len(subed) != 0:
                continue

            try:
                item_list = kkma.pos(line.decode('utf-8'))
            except Exception as e:
                continue

            for i, item in enumerate(item_list):
                # 1 gram
                uni_item = tag_word_pair([item])
                unigram_file.write(uni_item + "\n")

                # 2 gram
                if i != len(item_list) - 1:
                    bi_item = tag_word_pair([item, item_list[i+1]])
                    bigram_file.write(bi_item + "\n")

                # 3 gram
                if i < len(item_list) - 2:
                    tri_item = tag_word_pair([item, item_list[i+1], item_list[i+2]])
                    trigram_file.write(tri_item + "\n")

def generater_parallel(target_path, option):
    target_list = [f for f in os.listdir(target_path) if ".csv" in f or ".txt" in f]
    print target_list

    language_model_1_gram = {}
    language_model_2_gram = {}
    language_model_3_gram = {}
    lm_list = [language_model_1_gram, language_model_2_gram, language_model_3_gram]

    '''
    for target in target_list:
        with open(target_path+target, 'r') as file_read:
            lines = file_read.readlines()
            lines_length = len(lines)
            print lines_length

            processes = []
            for i in range(8):
                start = i * (lines_length / 8)
                end = (i + 1) * (lines_length / 8)
                processes.append(Process(target=generater_unit, args=(i, lines[start:end], option))) 
                processes[-1].start()
            for p in processes:
                p.join()
    '''

    raw_target_path = "lm_raw/"
    #raw_target_path_list = ["uni", "bi", "tri"]
    raw_target_path_list = ["uni"]

    for i, raw_target in enumerate(raw_target_path_list):
        print raw_target
        for target in os.listdir(raw_target_path + raw_target):
            print target
            with open(raw_target_path + raw_target + '/' + target, 'r') as raw_file:
                for item in raw_file:
                    update_dict(lm_list[i], item[:-1])

    print "start make lm"
    with open("lm/language_model_1_gram.txt", 'w') as file_write_1:

        for key, value in language_model_1_gram.iteritems():
            file_write_1.write(key + ':' + str(value) + "\n")
    print "end make lm"

    '''
    with open("lm/language_model_1_gram.txt", 'w') as file_write_1,\
        open("lm/language_model_2_gram.txt", 'w') as file_write_2,\
        open("lm/language_model_3_gram.txt", 'w') as file_write_3:

        for key, value in language_model_1_gram.iteritems():
            file_write_1.write(key + ':' + str(value) + "\n")
        for key, value in language_model_2_gram.iteritems():
            file_write_2.write(key + ':' + str(value) + "\n")
        for key, value in language_model_3_gram.iteritems():
            file_write_3.write(key + ':' + str(value) + "\n")
    '''
