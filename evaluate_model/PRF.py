r"""集成了 准确率 召回率 F1值的计算 """

import re


def normal(cn_file: str, en_file: str):
    r"""直接对比原文和译文的所有标签,统计出现的频率
    """
    tag_com = re.compile(r'<([\s\S]+?)>')
    with open(cn_file, 'r', encoding='utf-8') as f1:
        with open(en_file, 'r', encoding='utf-8') as f2:
            tot_lines = 0
            tot_p = 0
            tot_r = 0
            tot_f1 = 0
            for lc, le in zip(f1.readlines(), f2.readlines()):
                lc = lc.rstrip('\n ')
                le = le.rstrip('\n ')
                dict_cn = {}
                dict_en = {}
                arr_c = tag_com.findall(lc)
                arr_e = tag_com.findall(le)

                # 插入字典 方便后续查询
                for elem in arr_c:
                    if elem not in dict_cn.keys():
                        dict_cn[elem] = 0
                    dict_cn[elem] = dict_cn[elem] + 1
                for elem in arr_e:
                    if elem not in dict_en.keys():
                        dict_en[elem] = 0
                    dict_en[elem] = dict_en[elem] + 1

                # 总标签数量上的保留比率
                Hits_num = 0
                sum_elem_cn = dict_cn.__len__()  # 测试样例总数
                sum_elem_en = dict_en.__len__()  # 召回率(测试覆盖面积)

                for elem in dict_cn.keys():
                    if elem in dict_en.keys():
                        Hits_num = Hits_num + dict_en[elem]

                precision = Hits_num / sum_elem_cn
                recall = Hits_num / sum_elem_en
                f1 = 2 * precision * recall / (precision + recall)

                tot_p = tot_p + precision
                tot_r = tot_r + recall
                tot_f1 = tot_f1 + f1
                tot_lines = tot_lines + 1
            print('avg P: ', tot_p / tot_lines)
            print('avg R: ', tot_r / tot_lines)
            print('avg F1: %.3f' % (tot_f1 / tot_lines * 100))
