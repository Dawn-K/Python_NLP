import sys, re

# 0 不处理
# 1 在两端加$copy
# 2 完全泛化
ltag_com = re.compile(r'<')
rtag_com = re.compile(r'>')


def add_copy(line: str):
    newline = ''
    newline = ltag_com.sub(r' $copy<', line)
    newline = rtag_com.sub(r'>$copy ', newline)
    return newline


def generalized(line: str):
    stk = []
    idx = 0
    in_lable = False
    len = line.__len__()
    newline = ''
    lable_buff = ''
    for i in range(len):
        if line[i] == '<':
            in_lable = True
        elif line[i] == '>':
            now_idx = ''
            if lable_buff[0] == '/':  # start lable
                lable_buff = lable_buff[1:]
                now_idx = '_r' + str(stk.pop()[1]) + ' '
            else:  # end lable
                idx = idx + 1
                now_idx = '_l' + str(idx) + ' '
                stk.append((lable_buff, idx))
            newline = newline + '$lable' + str(now_idx) + ' '
            lable_buff = ''
            in_lable = False
        else:
            if in_lable:
                if line[i] == ' ':
                    continue
                else:
                    lable_buff = lable_buff + line[i]
            else:
                newline = newline + line[i]
    return newline


def pro_line(line: str, model: int):
    if model == 0:
        return line
    elif model == 1:
        return add_copy(line)
    elif model == 2:
        return generalized(line)


def lable_process(model: int, file_name: str):
    assert (model in [0, 1, 2])
    with open(file_name, 'r', encoding='utf-8') as f:
        for l in f.readlines():
            print(pro_line(l, model))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(
            'ERROR! lable_process needs 2 parms\n such as "python lable_process.py model file  " '
        )
    lable_process(int(sys.argv[1]), sys.argv[2])
