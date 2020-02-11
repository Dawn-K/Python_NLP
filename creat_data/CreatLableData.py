import random
import re
import copy

out_test_cn = None
out_test_en = None
out_generalization_cn = None
out_generalization_en = None
c_tag_pattern = r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]'
c_tag_com = re.compile(c_tag_pattern)


# 最基础的标签类
class Lable:
    def __init__(self, name: str, fix=False, start_name='', end_name=''):
        self.name = name
        if fix is False:
            self.start_name = '<' + self.name + '>'
            self.end_name = '</' + self.name + '>'
        else:
            self.start_name = start_name
            self.end_name = end_name

    def getStartName(self) -> str:
        return self.start_name

    def getEndName(self) -> str:
        return self.end_name


# 标签池
class LablePool:
    def __init__(self, typ: str):
        self.pos = 0
        self.lable = []
        file_name = 'tags/midTag'
        if typ == 'L1':
            file_name = 'tags/endTag'
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n>').lstrip('<')
                self.lable.append(Lable(line))

    def getLable(self) -> Lable:
        res = self.lable[self.pos]
        self.pos = (self.pos + 1) % self.lable.__len__()
        return res


# 句子类
class Sentence:
    def __init__(self, str_: str):
        self.arr = str_.split(' ')
        self.len = self.arr.__len__()

    def getStr(self):
        return ''.join(self.arr)

    def getTokenStr(self):
        return ' '.join(self.arr)

    def add(self, pos_s: int, pos_e: int, lable: Lable):
        assert (0 <= pos_s <= pos_e < self.len)
        self.arr[pos_s] = lable.getStartName() + ' ' + self.arr[pos_s]
        self.arr[pos_e] = self.arr[pos_e] + ' ' + lable.getEndName()

    def hasCnTag(self, pos_s: int, pos_e: int) -> bool:
        for pos in range(pos_s, pos_e + 1):
            if c_tag_com.search(self.arr[pos]) is not None:
                return True
        return False


# 句子池
class SentencePool:
    def __init__(self):
        pass

    def genSenCn(self):
        with open('data/cn_token', 'r', encoding='utf-8') as f:
            for l in f:
                l = l.rstrip('\n')
                yield Sentence(l)

    def genSenEn(self):
        with open('data/en_token', 'r', encoding='utf-8') as f:
            for l in f:
                l = l.rstrip('\n')
                yield Sentence(l)

    def genAlign(self):
        with open('data/final.align', 'r', encoding='utf-8') as f:
            for l in f:
                res_dict = {}
                arr = l.rstrip('\n').split(' ')
                for elem in arr:
                    tmp_arr = elem.split('-')
                    assert (len(tmp_arr) == 2)
                    pair_first = int(tmp_arr[0])
                    pair_second = int(tmp_arr[1])
                    if pair_first not in res_dict.keys():
                        res_dict[pair_first] = []
                    res_dict[pair_first].append(pair_second)
                yield res_dict


# 插入信息记录 类
class Insert_Record:
    def __init__(self, cn_l_pos: int, cn_r_pos: int, en_l_pos: int,
                 en_r_pos: int, lable: Lable):
        self.cn_l_pos = cn_l_pos
        self.cn_r_pos = cn_r_pos
        self.en_l_pos = en_l_pos
        self.en_r_pos = en_r_pos
        self.lable = lable

    # 以中文标签左端点最小值排序
    def __lt__(self, other):
        if self.cn_l_pos != other.cn_l_pos:
            return self.cn_l_pos < other.cn_l_pos
        else:
            return self.cn_r_pos > other.cn_r_pos 


# 控制核心
class ControlCore:
    def __init__(self):
        self.LP1 = LablePool('L1')
        self.LP2 = LablePool('L2')
        self.SP = SentencePool()
        self.record = []

    # 检查和其他标签的交错
    def conflict_with_pre_tags(self, pos_s: int, pos_e: int) -> bool:
        for pair in self.record:
            if not (pair[0] == pos_s and pair[1] == pos_e) and (
                    pos_s <= pair[0] <= pos_e <= pair[1]
                    or pair[0] <= pos_s <= pair[1] <= pos_e):
                return True
        return False

    def insert_lable(self, record_num: int):
        line_cnt = 0
        for word_cn, word_en, align in zip(self.SP.genSenCn(),
                                           self.SP.genSenEn(),
                                           self.SP.genAlign()):

            # 此处要用深拷贝,否则会将标签插入同一Sentence中
            word_gen_cn = copy.deepcopy(word_cn)
            word_gen_en = copy.deepcopy(word_en)
            self.record = []
            line_cnt = line_cnt + 1
            # todo: 控制标签密度
            up = word_cn.len // 10 + 2
            insert_num = random.randint(1, up)

            # 为防止出现L2标签未插入的情况
            no_l2 = True
            lable_dict = {}
            lable_dict['lable'] = []
            ins_record = []
            for loop in range(insert_num):
                # 生成 中文插入的范围 p1 p2 都是闭区间
                p1 = 0
                p2 = 0
                flag = True
                while flag:
                    p1 = random.randint(0, word_cn.len - 1)
                    p2 = random.randint(p1, word_cn.len - 1)
                    # 如果[p1,p2]范围内有中文标点或是和之前的标签范围发生交错,则继续循环,直到随机到合适的数值
                    flag = word_cn.hasCnTag(
                        p1, p2) or self.conflict_with_pre_tags(p1, p2)

                # 找到 p1 p2 对应的英文的范围
                minn = 10000
                maxx = -1
                for num in range(p1, p2 + 1):
                    if num not in align.keys():
                        continue
                    arr = align[num]
                    for elem in arr:
                        minn = min(minn, elem)
                        maxx = max(maxx, elem)
                if minn > maxx:
                    insert_num = insert_num + 1
                    continue

                # 添加标签
                no_l2 = False
                self.record.append((p1, p2))
                ins_record.append(
                    Insert_Record(p1, p2, minn, maxx, self.LP2.getLable()))
            l1_probability = random.randint(0, 1)
            tmp_lable = Lable('')
            if l1_probability == 1 or no_l2:
                self.record.append((0, word_cn.len - 1))
                ins_record.append(
                    Insert_Record(0, word_cn.len - 1, 0, word_en.len - 1,
                                  self.LP1.getLable()))

            # 排序后生成标签和泛化标签
            # 倒序排序能够保证外层标签编号一定小于内层标签
            ins_record.sort()
            ins_record = list(reversed(ins_record))
            lable_idx = len(ins_record)
            for elem in ins_record:
                word_cn.add(elem.cn_l_pos, elem.cn_r_pos, elem.lable)
                word_en.add(elem.en_l_pos, elem.en_r_pos, elem.lable)
                # 生成泛化标签
                gen_lable = None
                if lable_idx <= record_num:
                    gen_lable = Lable(elem.lable.name,
                                      fix=True,
                                      start_name='$lable_l' + str(lable_idx),
                                      end_name='$lable_r' + str(lable_idx))
                    lable_dict[lable_idx] = tmp_lable.name
                else:
                    gen_lable = Lable(tmp_lable.name,
                                      fix=True,
                                      start_name='$lable',
                                      end_name='$lable')
                    lable_dict['lable'].append(gen_lable.name)
                lable_idx = lable_idx - 1
                word_gen_cn.add(elem.cn_l_pos, elem.cn_r_pos, gen_lable)
                word_gen_en.add(elem.en_l_pos, elem.en_r_pos, gen_lable)
            out_test_cn.write(word_cn.getTokenStr() + '\n')
            out_test_en.write(word_en.getTokenStr() + '\n')
            out_generalization_cn.write(word_gen_cn.getTokenStr() + '\n')
            out_generalization_en.write(word_gen_en.getTokenStr() + '\n')


def CreatLableData():
    r""" 主函数,用以产生带标签语料
"""
    global out_test_cn
    global out_test_en
    global out_generalization_cn, out_generalization_en
    out_test_cn = open('data/out_test.cn', 'w', encoding='utf-8')
    out_test_en = open('data/out_test.en', 'w', encoding='utf-8')
    out_generalization_cn = open('data/out_generalization.cn',
                                 'w',
                                 encoding='utf-8')
    out_generalization_en = open('data/out_generalization.en',
                                 'w',
                                 encoding='utf-8')
    ctr = ControlCore()
    ctr.insert_lable(6)
    out_test_cn.close()
    out_test_en.close()
    out_generalization_cn.close()
    out_generalization_en.close()


if __name__ == '__main__':
    CreatLableData()
