r"""creat cn and en
"""
import re
import numpy as np


def creat_cn_en():
    cn = open('data/cn.haserr', 'w', encoding='utf-8')
    en = open('data/en.haserr', 'w', encoding='utf-8')
    c_pattern = r'\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b'
    pattern = r'([\s\S]+?)([^' + c_pattern + r']+)$'
    process_com = re.compile(pattern)
    math_head = r'[\d\-]+.?\s'
    math_head_com = re.compile(math_head)
    ans_arr_c = []
    ans_arr_e = []
    dict_ = {}
    with open('data/raw_small', 'r', encoding='utf-8') as file:
        for word in file:
            arr = word.split('\t')
            word_c = arr[0].rstrip('\n \t').lstrip(' \t')
            word_e = arr[1].rstrip('\n \t').lstrip(' \t')
            if word_e[0] == '.':  # 发现有的英文句子以.开头
                word_e = word_e[1:]
                word_e = word_e.lstrip(' \t')
            ans_arr_c.append(len(word_c))
            if len(word_c) not in dict_.keys():
                dict_[len(word_c)] = 0
            dict_[len(word_c)] = dict_[len(word_c)] + 1
            ans_arr_e.append(len(word_e))
            cn.write(word_c + '\n')
            en.write(word_e + '\n')
    cn.close()
    en.close()
    ans_arr_c = np.array(ans_arr_c)
    ans_arr_e = np.array(ans_arr_e)


if __name__ == '__main__':
    creat_cn_en()
