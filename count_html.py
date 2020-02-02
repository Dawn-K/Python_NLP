r""" 统计 htmlsrc/* 的标签的分布情况
"""

import re, os
dict = {}
care = []
remove = r'<[/\s\\]'  # 去除闭合括号和注释和其他奇葩标签
remove_com = re.compile(remove)
first_word = r'^<([\w\-!]+)[\s\S]+'  # 选中尖括号开头的连续字母,连续字母以空格或者>为分隔
first_word_com = re.compile(first_word)
word_in_bkt = r'(<[\S\s]+?>)'  # 其实就是选取带尖括号的内容(含尖括号)
word_in_bkt_com = re.compile(word_in_bkt)
comment = r'^<![\S\s]*>$'
comment_com = re.compile(comment)
company_tags = []
comment_sign = '!--...--'
only_company = False

def updateDict(arr: list):
    for w in arr:
        if len(remove_com.findall(w)) != 0:
            continue
        if comment_com.match(w) is not None:  # 是注释
            dict[comment_sign] = dict[comment_sign] + 1
            continue
        vec = first_word_com.findall(w)
        # assert (len(vec) is not 0)
        if len(vec) is 0:
            # print('err!!! ',end=' ')
            # print(w)
            continue
        if vec[0] not in dict.keys():
            dict[vec[0]] = 0
        dict[vec[0]] = dict[vec[0]] + 1


def process_file(file_name: str):
    page = open(file_name, 'r', encoding='utf-8')
    word = page.read()
    page.close()
    arr = word_in_bkt_com.findall(word)
    updateDict(arr)


def read_company_tags():
    with open('companyTags', 'r') as file:
        for line in file:
            line = line.rstrip('\n>')
            line = line.lstrip('<')
            # print(line)
            company_tags.append(line)


def print_res():
    d_order = sorted(dict.items(), key=lambda x: x[1],
                     reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。
    # d_order相当于字典集合中遍历出来的一个元组。
    sum = 0
    sum_com_tags = 0
    for item in d_order:
        sum = sum + item[1]
        if item[0] in company_tags:
            sum_com_tags = sum_com_tags + item[1]
    print('total tags : ' + str(sum) + '  total type ' + str(len(d_order)))
    for item in d_order:
        # if item[0] == 'legend' or item[0] == 'summary':
        #     print('Attention!!!', end='  ')
        if only_company is False or item[0] in company_tags:
            print(str(item[0]).ljust(10, ' '), end=' ')
            if only_company is True:
                # print('inner radio: ', end=' ')
                print('%.2f%%   ' % (item[1] / sum_com_tags * 100), end=' ')
            print('%.2f%%' % (item[1] / sum * 100))

def print_diff():
    print('only in dict   ----->')
    for w in dict.keys():
        if w not in company_tags:
            print(w)
    print('only in company -----<')
    for w in company_tags:
        if w not in dict.keys():
            print(w)
    
if __name__ == '__main__':
    dict[comment_sign] = 0
    for files in os.listdir('./htmlsrc'):
        process_file('./htmlsrc/' + files)
    only_company = True
    if only_company:
        read_company_tags()
    print_res()
    if only_company:
        print_diff()
