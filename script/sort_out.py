import re


class Pair:
    def __init__(self, fi: str, se: str):
        self.fi = fi
        self.se = se

    def __lt__(self, other):
        return int(self.fi) < int(other.fi)


if __name__ == '__main__':
    with open('out.tmp', 'r', encoding='utf-8') as f:
        with open('gen.out.sys', 'w', encoding='utf-8') as w:
            h_head_com = re.compile(r'H-([\d]+)')
            pair_arr = []
            for l in f.readlines():
                arr = l.rstrip('\n').split('\t')
                ans = h_head_com.match(arr[0])
                if ans is None:
                    continue
                num = ans.group(1)
                print(l)
                arr = arr[2:]
                pair_arr.append(Pair(num, '\t'.join(arr)))
            pair_arr.sort()
            for elem in pair_arr:
                w.write(elem.se + '\n')
