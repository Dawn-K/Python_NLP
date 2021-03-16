r""" 泛化已经被插入标签的文本
"""
import re, sys, json

tag_com = re.compile(r'<[\s\S]+?>')
lable_com = re.compile(r'$$$LABLE$$$')
start_com = re.compile(r'^<([^/][\S]*)[\s\S]*?>$')
end_com = re.compile(r'^<[/]([\S]*)[\s\S]*?>$')
alone_com = re.compile(r'^<[\s\S]*?[/]>$')
gen_file = None


def start(s: str) -> bool:
    return start_com.match(s) is not None


def alone(s: str) -> bool:
    return alone_com.match(s) is not None


def end(s: str) -> bool:
    return end_com.match(s) is not None


def lable_match(s1: str, s2: str) -> bool:
    if start(s1) is False or end(s2) is False:
        return False
    return start_com.match(s1).group(1) == end_com.match(s2).group(1)


def process(line: str, record_num: int):
    stk = []
    idx2pair = {}
    tag_arr = tag_com.findall(line)
    cnt = 1
    idx = 1
    for elem in tag_arr:
        if alone(elem):
            idx2pair[idx] = ('', cnt, elem)
            cnt = cnt + 1
        elif start(elem):
            stk.append((elem, cnt))
            idx2pair[idx] = ('l', cnt, elem)
            cnt = cnt + 1
        else:
            assert (lable_match(stk[-1][0], elem))
            idx2pair[idx] = ('r', stk[-1][1], elem)
            stk.pop()
        idx = idx + 1

    newline = tag_com.sub(r'#$%MYLABLE#$%', line)
    arr = list(filter(None, newline.split('#$%')))
    lable_idx = 1
    lenth = len(arr)
    record_lable = {}
    record_lable['$lable'] = []
    for i in range(lenth):
        if arr[i] == 'MYLABLE':
            assert (lable_idx in idx2pair.keys())
            cur = idx2pair[lable_idx]
            tmp_str = '$lable'
            if record_num > 0:
                tmp_idx = cur[1]
                if cur[1] <= record_num:
                    tmp_str = tmp_str + '_' + cur[0] + str(cur[1])
            arr[i] = tmp_str
            if tmp_str == '$lable':
                record_lable[tmp_str].append(cur[2])
            else:
                record_lable[tmp_str] = cur[2]
            lable_idx = lable_idx + 1
    global gen_file
    gen_file.write(json.dumps(record_lable) + '\n')
    return ' '.join(arr)


def process_model3(line: str, record_num: int):
    tag_arr = tag_com.findall(line)
    newline = tag_com.sub(r'#$%MYLABLE#$%', line)
    arr = list(filter(None, newline.split('#$%')))
    lenth = len(arr)
    lable_idx = 1
    record_lable = {}
    record_lable['$lable'] = []
    for i in range(lenth):
        if arr[i] == 'MYLABLE':
            if lable_idx <= record_num:
                arr[i] = '$lable_' + str(lable_idx)
                record_lable[arr[i]] = tag_arr[lable_idx - 1]
            else:
                arr[i] = '$lable'
                record_lable[arr[i]].append(tag_arr[lable_idx - 1])
            lable_idx = lable_idx + 1
    global gen_file
    gen_file.write(json.dumps(record_lable) + '\n')
    return ' '.join(arr)


def gen(file_name: str, record_num: int, model: int):
    with open(file_name, 'r', encoding='utf-8') as f:
        for l in f.readlines():
            if model == '2':
                print(process(l.rstrip('\n'), record_num))
            else:
                print(process_model3(l.rstrip('\n'), record_num))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(
            'ERROR! generalize_file needs 3 parms\n such as "python generalize_file.py file_name record_num model" '
        )
    gen_file = open('gen_record', 'w', encoding='utf-8')
    file_name = sys.argv[1]
    record_num = int(sys.argv[2])
    model = int(sys.argv[3])
    gen(file_name, record_num, model)
