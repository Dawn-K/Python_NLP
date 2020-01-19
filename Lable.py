import re, random

out_test = ''


class Lable:
    def __init__(self, name: str):
        self.name = name
        pass

    def getStartName(self) -> str:
        return '<' + self.name + '>'

    def getEndName(self) -> str:
        return '</' + self.name + '>'


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


class Sentence:
    def __init__(self, str_: str):
        self.arr = str_.split(' ')
        self.len = str_.__len__()

    def getStr(self):
        return ''.join(self.arr)

    def add(self, pos_s: int, pos_e: int, lable: Lable):
        assert (0 <= pos_s <= pos_e < self.len)
        self.arr[pos_s] = lable.getStartName() + self.arr[pos_s]
        self.arr[pos_e] = self.arr[pos_e] + lable.getStartName()


class SentencePool:
    def __init__(self):
        pass

    def genSen(self) -> Lable:
        with open('cn_token', 'r', encoding='utf-8') as f:
            for l in f:
                yield Sentence(l)


class ControlCore:
    def __init__(self):
        self.LP1 = LablePool('L1')
        self.LP2 = LablePool('L2')
        self.SP = SentencePool()

    def test(self):
        cnt = 10
        for word in self.SP.genSen():
            p1 = 1
            p2 = 3
            word.add(p1, p2, self.LP2.getLable())
            out_test.write(word.getStr() + '\n')
            cnt = cnt - 1
            if cnt == 0:
                break


if __name__ == '__main__':
    out_test = open('out_test.tmp', 'w', encoding='utf-8')
    CTR = ControlCore()
    CTR.test()
    out_test.close()