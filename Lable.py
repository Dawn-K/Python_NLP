import re, random

out_test = ''
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
        file_name = 'midTag'
        if typ == 'L1':
            file_name = 'endTag'
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

    def genSen(self) -> Lable:
        with open('cn_token', 'r', encoding='utf-8') as f:
            for l in f:
                l = l.rstrip('\n')
                yield Sentence(l)


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

    def test(self):
        for word in self.SP.genSen():
            self.record = []
            up = word.len // 5 + 2
            insert_num = random.randint(1, up)
            for loop in range(insert_num):
                flag = True
                p1 = 0
                p2 = 0
                while flag:
                    p1 = random.randint(0, word.len - 1)
                    p2 = random.randint(p1, word.len - 1)
                    # 如果[p1,p2]范围内有中文标点或是和之前的标签范围发生交错,则继续循环,直到随机到合适的数值
                    flag = word.hasTag(p1, p2) or self.check(p1, p2)
                self.record.append((p1, p2))
                word.add(p1, p2, self.LP2.getLable())
            out_test.write(word.getStr() + '\n')


if __name__ == '__main__':
    out_test = open('out_test.tmp', 'w', encoding='utf-8')
    CTR = ControlCore()
    CTR.test()
    out_test.close()