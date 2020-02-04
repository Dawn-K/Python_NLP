import re, random

out_test_cn = ''
out_test_en = ''
c_tag_pattern = r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]'
c_tag_com = re.compile(c_tag_pattern)


# 最基础的标签类
class Lable:
    def __init__(self, name: str):
        self.name = name
        pass

    def getStartName(self) -> str:
        return '<' + self.name + '>'

    def getEndName(self) -> str:
        return '</' + self.name + '>'


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
        self.arr[pos_s] = lable.getStartName() + self.arr[pos_s]
        self.arr[pos_e] = self.arr[pos_e] + lable.getEndName()

    def hasTag(self, pos_s: int, pos_e: int) -> bool:
        for pos in range(pos_s, pos_e + 1):
            if c_tag_com.search(self.arr[pos]) is not None:
                return True
        return False


# 句子池
class SentencePool:
    def __init__(self):
        pass

    def genSenCn(self) -> Lable:
        with open('data/cn_token', 'r', encoding='utf-8') as f:
            for l in f:
                l = l.rstrip('\n')
                yield Sentence(l)

    def genSenEn(self) -> Lable:
        with open('data/en_token', 'r', encoding='utf-8') as f:
            for l in f:
                l = l.rstrip('\n')
                yield Sentence(l)

    def genAlign(self) -> dict:
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


# 控制核心
class ControlCore:
    def __init__(self):
        self.LP1 = LablePool('L1')
        self.LP2 = LablePool('L2')
        self.SP = SentencePool()
        self.record = []

    # 检查和其他标签的交错
    def check(self, pos_s: int, pos_e: int) -> bool:
        for pair in self.record:
            if not (pair[0] == pos_s and pair[1] == pos_e) and (
                    pos_s <= pair[0] <= pos_e <= pair[1]
                    or pair[0] <= pos_s <= pair[1] <= pos_e):
                return True
        return False

    def insert_lable(self):
        for word_cn, word_en, align in zip(self.SP.genSenCn(),
                                           self.SP.genSenEn(),
                                           self.SP.genAlign()):
            self.record = []

            # todo: 控制标签密度
            up = word_cn.len // 10 + 2
            insert_num = random.randint(1, up)

            # 为防止出现L2标签未插入的情况
            no_L2 = True
            for loop in range(insert_num):
                # p1 p2 都是闭区间
                p1 = 0
                p2 = 0
                flag = True
                while flag:
                    p1 = random.randint(0, word_cn.len - 1)
                    p2 = random.randint(p1, word_cn.len - 1)
                    # 如果[p1,p2]范围内有中文标点或是和之前的标签范围发生交错,则继续循环,直到随机到合适的数值
                    flag = word_cn.hasTag(p1, p2) or self.check(p1, p2)
                self.record.append((p1, p2))

                # 找到 p1 p2 对应的范围
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
                no_L2 = False
                new_lable = self.LP2.getLable()
                word_cn.add(p1, p2, new_lable)
                word_en.add(minn, maxx, new_lable)

            L1_probability = random.randint(0, 1)
            if L1_probability == 1 or no_L2:
                tmp_lable = self.LP1.getLable()
                word_cn.add(0, word_cn.len - 1, tmp_lable)
                word_en.add(0, word_en.len - 1, tmp_lable)

            out_test_cn.write(word_cn.getStr() + '\n')
            out_test_en.write(word_en.getTokenStr() + '\n')


def CreatLableData():
    r""" 主函数,用以产生带标签语料
    """
    global out_test_cn
    global out_test_en
    out_test_cn = open('data/out_test.cn', 'w', encoding='utf-8')
    out_test_en = open('data/out_test.en', 'w', encoding='utf-8')
    CTR = ControlCore()
    CTR.insert_lable()
    out_test_cn.close()
    out_test_en.close()


if __name__ == '__main__':
    CreatLableData()
