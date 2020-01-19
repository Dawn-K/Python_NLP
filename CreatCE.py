import re
import numpy as np

cn = open('cn', 'w', encoding='utf-8')
en = open('en', 'w', encoding='utf-8')
c_pattern = r'\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b'
pattern = r'([\s\S]+?)([^' + c_pattern + r']+)$'
process_com = re.compile(pattern)
math_head = r'[\d\-]+.?\s'
math_head_com = re.compile(math_head)
ans_arr_c = []
ans_arr_e = []
dict_ = {}
if __name__ == '__main__':
    with open('raw_small', 'r', encoding='utf-8') as file:
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

    # print('for cn : avg  %6.2f ,max %d, min %d, std %6.2f' %
    #       (ans_arr_c.mean(0), max(ans_arr_c), min(ans_arr_c),
    #        np.std(ans_arr_c, axis=0)))
    # print('for en : avg  %6.2f ,max %d, min %d, std %6.2f' %
    #       (ans_arr_e.mean(0), max(ans_arr_e), min(ans_arr_e),
    #        np.std(ans_arr_e, axis=0)))
    a = sorted(dict_.items(), key=lambda x: x[1], reverse=True)
    # print(a)
    cnt = 0
    for i in a:
        if i[0] <= 80:
            cnt = cnt + i[1]
    print(cnt / 10000)
    # plt.errorbar(1, ans_arr_c.mean(0), np.std(ans_arr_c, axis=0), fmt="o")
    # plt.show()