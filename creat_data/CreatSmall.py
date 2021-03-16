# -*- coding: utf-8 -*-
r""" Read the first few lines of the wmt2018 and write to data/raw_small  """

import re, os


def wmt2018_to_rawsmall(file_name: str, cnt: int):
    data_path = os.getcwd() + '/data'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    small = open('data/raw_small', 'w', encoding='utf-8')
    remove_tail_com = re.compile(r'\twmt2018[\s\S]+$')
    sum_len = 0
    with open(file_name, 'r', encoding='utf-8') as file:
        for word in file:
            if cnt == 0:
                break
            cnt = cnt - 1
            new_word = remove_tail_com.sub('', word)
            small.writelines(new_word + '\n')
    small.close()


if __name__ == '__main__':
    wmt2018_to_rawsmall(100)