import re


def normal(cn_file: str, en_file: str):
    r"""直接对比原文和译文的所有标签,统计出现的频率
    """
    tag_com = re.compile(r'<([\s\S]+?)>')
    with open(cn_file, 'r', encoding='utf-8') as f1:
        with open(en_file, 'r', encoding='utf-8') as f2:
            for lc, le in zip(f1.readlines(), f2.readlines()):
                print('lc ', lc)
                print('le ', le)
                lc = lc.rstrip('\n ')
                le = le.rstrip('\n ')
                dict_cn = {}
                dict_en = {}
                arr_c = tag_com.findall(lc)
                arr_e = tag_com.findall(le)

                print(arr_c)
                print(arr_e)
                for elem in arr_c:
                    if elem not in dict_cn.keys():
                        dict_cn[elem] = 0
                    dict_cn[elem] = dict_cn[elem] + 1
                for elem in arr_e:
                    if elem not in dict_en.keys():
                        dict_en[elem] = 0
                    dict_en[elem] = dict_en[elem] + 1

                # 总标签数量上的保留比率
                A = 0
                sum_elem_cn = dict_cn.__len__()  # 测试样例总数
                sum_elem_en = dict_en.__len__()  # 召回率(测试覆盖面积)

                for elem in dict_cn.keys():
                    if elem in dict_en.keys():
                        A = A + dict_en[elem]

                precision = A / sum_elem_cn
                recall = A / sum_elem_en
                f1 = 2 * precision * recall / (precision + recall)
                print('P: ', precision)
                print('R: ', recall)
                print('F1: %.3f' % (f1 * 100))
