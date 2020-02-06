r"""集成了 准确率 召回率 F1值的计算 """

import re


def calculate_F1(cn_file: str, en_file: str):
    r"""直接对比原文和译文的所有标签,统计出现的频率
    """
    tag_com = re.compile(r'<([\s\S]+?)>')
    with open(cn_file, 'r', encoding='utf-8') as f1:
        with open(en_file, 'r', encoding='utf-8') as f2:
            dict_cn = {}
            dict_en = {}
            for lc, le in zip(f1.readlines(), f2.readlines()):
                lc = lc.rstrip('\n ')
                le = le.rstrip('\n ')
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
            sum_elem_cn = 0  # 测试样例总数
            sum_elem_en = 0  # 召回率(测试覆盖面积)
            for elem in dict_cn.keys():
                sum_elem_cn = sum_elem_cn + dict_cn[elem] 

            for elem in dict_en.keys():
                sum_elem_en = sum_elem_en + dict_en[elem]

            for elem in dict_cn.keys():
                if elem in dict_en.keys():
                    Hits_num = Hits_num + min(dict_en[elem],dict_cn[elem])

            precision = Hits_num / sum_elem_cn
            recall = Hits_num / sum_elem_en
            f1 = 2 * precision * recall / (precision + recall)

            print('precision : ', precision)
            print('recall : ', recall)
            print('F1 value :  %.3f' % (f1))
