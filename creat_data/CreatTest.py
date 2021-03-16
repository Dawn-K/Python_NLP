r""" 将cslx中的中英文分隔开,放入data/test.splitce.* 中
"""
import sys, re


def splitce(test_file: str):
    c_pattern_com = re.compile(r'[\u4e00-\u9fa5]')
    with open(test_file, 'r', encoding='utf-8') as f:
        with open('data/test_splitce.cn', 'w', encoding='utf-8') as w_cn:
            with open('data/test_splitce.en', 'w', encoding='utf-8') as w_en:
                cnt = 0
                for l in f.readlines():
                    arr = l.rstrip('\n').split('\t')
                    if len(c_pattern_com.findall(arr[1])) == 0:
                        if len(arr[1]) > 1000:
                            continue
                        w_cn.write(arr[0] + '\n')
                        w_en.write(arr[1] + '\n')
