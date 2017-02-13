import os
from konlpy.tag import Kkma

def generater(target_path):
    target_list = [f for f in os.listdir(target_path) if ".csv" in f or ".txt" in f]
    print target_list
    kkma = Kkma()
    file_write_1 = open("language_model_1_gram.txt", 'w')
    file_write_2 = open("language_model_2_gram.txt", 'w')

    language_model_1_gram = {}
    language_model_2_gram = {}
    for target in target_list:
        with open(target_path+target, 'r') as file_read:
            for line in file_read:
                if line[0] == '-':
                    continue
                else:
                    splitted = line.split(']')
                    if len(splitted) != 3:
                        continue
                    else:
                        if '(' in splitted[2] or ')' in splitted[2]:
                            continue
                line = splitted[2].strip()
                try:
                    item_list = kkma.pos(line.decode('utf-8'))
                except Exception as e:
                    continue
                for i, item in enumerate(item_list):
                    # 1 gram
                    uni_item = item[0].encode('utf-8')
                    if uni_item in language_model_1_gram.keys():
                        updated = language_model_1_gram[uni_item]
                        del language_model_1_gram[uni_item]
                        language_model_1_gram[uni_item] = updated + 1
                    else:
                        language_model_1_gram[uni_item] = 1

                    # 2 gram
                    if i != len(item_list) - 1:
                        bi_item = item[0].encode('utf-8') + ' ' + item_list[i+1][0].encode('utf-8')
                        if bi_item in language_model_2_gram.keys():
                            updated = language_model_2_gram[bi_item]
                            del language_model_2_gram[bi_item]
                            language_model_2_gram[bi_item] = updated + 1
                        else:
                            language_model_2_gram[bi_item] = 1

    for key, value in language_model_1_gram.iteritems():
        file_write_1.write(key + ':' + str(value) + "\n")
    for key, value in language_model_2_gram.iteritems():
        file_write_2.write(key + ':' + str(value) + "\n")

    file_write_1.close()
    file_write_2.close()
